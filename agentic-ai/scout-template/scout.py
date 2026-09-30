"""The paper scout, v1.2 at the "suggest" setting.

Run it with:  python scout.py
It needs GEMINI_API_KEY in the environment. It writes three things:
  digest.md           today's suggestions (posted as a GitHub issue)
  log/verdicts.jsonl  one line per paper judged, for measuring later
  seen.json           memory of papers already judged (Chapter 9)
It never publishes, emails or changes anything else (Chapter 5).
"""
import datetime
import json
import os
import pathlib
import sys
import time

import config
from arxiv_source import fetch_new_papers, fetch_full_text
from judge import judge_paper

HERE = pathlib.Path(__file__).parent
SEEN = HERE / "seen.json"
LOG = HERE / "log" / "verdicts.jsonl"
DIGEST = HERE / "digest.md"


def gemini_ask():
    """A function that sends a prompt to Gemini and returns the reply text."""
    from google import genai

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set. Add it as a secret (see README.md).")
    client = genai.Client(api_key=key)

    def ask(prompt):
        for attempt in range(4):
            try:
                reply = client.models.generate_content(model=config.MODEL, contents=prompt).text
                time.sleep(config.SECONDS_BETWEEN_CALLS)
                return reply or ""
            except Exception as error:
                if attempt == 3:
                    raise
                wait = 30 * (attempt + 1)
                print(f"   model call failed ({type(error).__name__}), retrying in {wait}s")
                time.sleep(wait)

    return ask


def make_digest(records, today, fetched):
    suggestions = sorted((r for r in records if r["verdict"] == "suggest"),
                         key=lambda r: -r["confidence"])
    lines = [f"# Paper scout, {today}", ""]
    if suggestions:
        lines.append(f"{len(suggestions)} suggestion(s) from {len(records)} new papers. "
                     "The scout only suggests: you decide what to read.")
    else:
        lines.append(f"Nothing relevant today ({len(records)} new papers checked).")
    for r in suggestions:
        lines += ["", f"## [{r['title']}]({r['url']})", f"confidence {r['confidence']:.2f}", ""]
        if r["grounded"]:
            lines.append(r["reason"] or "_No reason given._")
        else:                                   # the guardrail: never show a false number
            lines.append(f"_Reason withheld: it mentioned a number not found in the paper "
                         f"({', '.join(r['invented'])})._")
    screened = sum(r["stage"] == "screened_out" for r in records)
    full = sum(r["read_full"] for r in records)
    errors = sum(bool(r["error"]) for r in records)
    lines += ["", "---",
              f"Model: {config.MODEL}. Fetched {fetched}, new {len(records)}, "
              f"screened out {screened}, full text read {full}, reply errors {errors}."]
    return "\n".join(lines) + "\n"


def run(ask=None, papers=None, fetch_full=None):
    ask = ask or gemini_ask()
    fetch_full = fetch_full or fetch_full_text
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    if papers is None:
        papers = fetch_new_papers(config.CATEGORIES, config.MAX_PAPERS)
    new = [p for p in papers if p["base_id"] not in seen]
    today = datetime.date.today().isoformat()
    print(f"{len(papers)} papers fetched, {len(new)} not judged before")

    LOG.parent.mkdir(exist_ok=True)
    records = []
    for paper in new:
        record = judge_paper(paper, ask, fetch_full, config.THRESHOLD, config.FULL_TEXT_CHARS)
        record.update(date=today, model=config.MODEL)
        records.append(record)
        seen.add(paper["base_id"])
        with LOG.open("a", encoding="utf-8") as f:            # saved as we go
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        SEEN.write_text(json.dumps(sorted(seen), indent=0))
        print(f"   {record['verdict']:>7} ({record['confidence']:.2f})  {paper['title'][:70]}")

    DIGEST.write_text(make_digest(records, today, len(papers)), encoding="utf-8")
    return records


if __name__ == "__main__":
    run()
    print()
    print(DIGEST.read_text(encoding="utf-8"))
