# Your LLM Can Now Tell the Inference Engine What to Ignore

*10-min paper read · [Language Models Can Control Their Own Attention](https://arxiv.org/abs/2609.02737), Namgyu Ho, Huzama Ahmad, Woosung Koh, Se-Young Yun, Tal Schuster, Cicero Nogueira dos Santos (KAIST AI)*

## TL;DR

Every time an LLM generates a token, the inference engine has to scan the entire KV cache, even though the model usually only cares about a small part of it. This paper's fix is called Declarative Attention (DA), and the idea is simple: let the model say, as part of its own reasoning, how much context it actually needs for the next bit of its answer. The engine reads that and skips the rest.

They tested this zero-shot (no retraining) on two large open models and got 52.0% lower decoding attention cost on Gemma-4-31B and 31.1% on Qwen-3.6-27B. Accuracy dropped by 1.27 and 2.75 percentage points, and that gap actually shrinks as the models get bigger. On long documents the savings get huge, up to 21 million tokens in a single response, and when projected onto real hardware, decode time drops to around 71-77% of normal.

## Where this fits in

Older sparse-attention methods work "extrinsically": some separate lightweight mechanism scores the cache at every step and guesses which tokens to keep, based on the model's internal activations (Zhang et al., 2023; Tang et al., 2024). DA does the opposite. It's "intrinsic," meaning the same model that's generating the answer makes the call itself, out loud, as part of its own reasoning. No separate scorer needed.

A few pieces of this build directly on older work, and it's worth naming them since none of this came out of nowhere. The block-sparse masking follows the same idea as Native Sparse Attention (Yuan et al., 2025). The system prompt is placed where it is specifically to fill the model's "attention sink" (Xiao et al., 2024), so the long context never has to do that job. And the actual engine work sits on top of FlashAttention (Dao et al., 2022) and vLLM (Kwon et al., 2023), DA just changes which KV blocks get read, not how they're read once selected. The authors even call this a "system-2" style of attention, borrowing that framing from System 2 Attention (Weston & Sukhbaatar, 2023): selection through explicit reasoning in plain language instead of something buried invisibly inside the network.

## How it actually works

The prompt is built from two parts. A scaffold (the system instructions, the user's question, and a block explaining the three modes) stays visible the whole time. The context, meaning the actual long document or documents, gets split into roughly 2,000-token segments, and the splitting tries to land on natural breaks: paragraphs first, then sentences, then clauses, never in the middle of a word.

Here's the clever bit. Each segment gets handed to the model disguised as the output of a fake tool call, like the model had called a `get_magic_chunk` tool and gotten back "Magic Chunk 3," "Magic Chunk 7," and so on. Models are already good at tracking tool-call and turn boundaries because of how they're post-trained, so this reuses something they're already comfortable with instead of teaching them a totally new syntax.

There are three modes and each one has a job:

- `global`: navigation mode. The model looks across everything to decide which chunk to check next, and briefly says why.
- `focus`: extraction mode. It only attends to the chunk it named, and pulls out a value from it, word for word.
- `local`: reasoning mode. No context at all, just the model's own output so far. This is for doing math or synthesis with values it already pulled out.

While the model generates, a state machine is watching the output live. It starts in global mode by default, and the moment it sees the closing `>` on an opening `<focus>` or `<local>` tag, it flips modes. When it sees the closing tag, it flips back. On the inference engine side, vLLM keeps its KV cache in fixed blocks (16 to 32 tokens), and it can only skip whole blocks at a time, so whatever span the model asked for gets rounded out to the nearest block edges, and those blocks just get hidden from the attention kernel for that step. FlashAttention itself doesn't need to change at all. This only applies to the model's full-attention layers too. Models that mix in cheaper layers, like sliding window attention or Gated DeltaNet, already have a fixed cost that doesn't grow with context length, so DA doesn't touch those.

Here's the actual example from the paper, for the question "How long after its founding did Acme Corp go public?":

```
[global] I need the founding year and the IPO year. The company
history in Magic Chunk 2 should state the founding.
[focus: Magic Chunk 2] "Acme Corp was founded in 2003 in San Jose."
[global] The IPO year is still missing. Magic Chunk 7 covers
Acme's financial milestones.
[focus: Magic Chunk 7] "Acme Corp went public on the NYSE in 2011."
[local] 2011 − 2003 = 8 years.
Answer: 8 years
```

Notice that finding the right chunk still means actually looking around first. That's what global mode does, and it's not free. DA isn't skipping that step, it's just keeping it short, and letting the rest of the answer happen in cheaper modes.

## An analogy that helped me get it

Picture an open-book exam with a 1,000-page textbook sitting next to you. Normally, every single sentence you write means flipping through that whole book again, even for something as pointless as writing "in conclusion." That's basically what a normal LLM does. Full re-scan, every word.

DA is like telling your exam proctor, before you write each part of your answer, exactly how much of the book you need right now. "I don't need it" is local mode. "I need this one page" is focus. "I need the whole book" is global. And the proctor only hands you what you actually asked for.

So how do you point at "one page" without knowing page numbers? You don't get the raw book at all. Before the exam even starts, it's already been cut into labeled chunks, Chunk 1, Chunk 2, and so on, handed to you one at a time as if you'd asked a librarian for each one. So instead of saying "page 47," you say "give me Chunk 2," pointing at something you were already handed earlier. The proctor is watching you write in real time, and the second you write `<focus>`, it notes which chunk you want and hides everything else until you close the tag.

Mapping this onto the real example: global mode is skimming the table of contents and going "founding is probably chapter 2, IPO is probably chapter 7." It's cheap because it's brief, not because it skips actually looking. Focus mode is flipping to just those two chapters. Local mode is doing the subtraction with what you already copied down, book closed. The waste in a normal exam was never that first skim. It was rereading the whole book cover to cover before every single sentence, long after you already knew where the answer was.

One small detail worth keeping in the analogy: the proctor's photocopier can't hand you exactly one page, it only copies in bundles, say 20 pages at a time. Ask for page 47 and you get pages 41 to 60. A bit wasteful, but nowhere close to as wasteful as copying all 1,000 pages for every sentence you write.

## The numbers that back this up

A few results here made me trust this more than a typical "we made attention sparse" paper. They ran an ablation where they kept the exact same prompt format but turned off the actual masking, and confirmed the masking itself is responsible for up to 71.1% of the attended-token reduction. So this isn't just an artifact of the model writing shorter or differently shaped answers because of the new prompt style.

Breaking it down by mode on Gemma-4-31B: global mode is only about 27% of generated tokens, but since it attends to everything, it eats up over 80% of the tokens that actually get attended to. Focus and local together make up the other 73% of tokens and only attend to about 12% and 6% of what a normal step would, which works out to 76 to 99% savings per token depending on the mode.

The wall-clock numbers (that 71-77% of normal decode time) come from a roofline model on a single B200 GPU. Worth being clear that this is a theoretical ceiling at a stated hardware utilization, not something they actually benchmarked end to end, and it also excludes prefill (the one-time read of the whole context before generation starts), since that runs on a separate pool in the disaggregated serving setup they're modeling.

## Where I'd push back

The paper is refreshingly upfront about its own weak points, and I think these are worth taking seriously instead of glossing over:

It falls apart on small models, which is annoying because that's exactly where you'd want the cost savings most. DA depends on the model correctly naming a real chunk whenever it writes `<focus>`. That success rate is 99% on the biggest models tested, but only 58% on the smallest Gemma (E4B) and 89% on the smallest Qwen (3.5-4B). The paper is honest that the small model's accuracy collapse is mostly the model failing to follow the protocol, not a reasoning failure.

It doesn't work with thinking mode yet. Models failed to follow the DA protocol inside extended reasoning traces during early testing, so every result in this paper is non-thinking mode only. Given how much current usage leans on reasoning models, that's a real gap right now.

The savings don't scale as cleanly with context length as the headline numbers suggest. Global mode's share of tokens actually rises at longer contexts, up to about 45% in the longest bucket they tested, which caps how much the total saving can grow. The authors chalk this up to how the zero-shot prompt behaves rather than a hard limit of the method itself.

There's still no direct comparison against the "extrinsic" scoring-based methods DA is positioned against. What's shown is DA against a plain vanilla prompting baseline, not against the proxy-scoring sparse-attention approaches already used in production.

And there's a small inconsistency worth flagging: the paper itself reports a 1.27 percentage point accuracy drop on Gemma-4-31B, but the lead author's own comment on the Hugging Face paper page cites 1.52 for what looks like the same result.

## Why I think this matters for RAG

Two things here come straight from the paper, not from me reading between the lines. First, their roughly 2K-token chunking is only needed because the benchmark text has no real structure. In actual deployments, they point out that natural boundaries like user and assistant turns, or tool responses that contain retrieved context, could serve as segments directly. A RAG pipeline's retrieved chunks are basically already a good fit for this, no extra chunking logic needed.

Second, and this is the part I found more interesting: the paper argues retrieval and DA aren't solving the same problem, they're solving problems that stack. Retrieval decides what gets into the context in the first place. DA decides how much of what's already there the model bothers to attend to. In an agent's session, a retrieved chunk or tool result usually stays in context for the rest of that session even though it was probably only relevant to the one turn that fetched it. So the longer an agentic RAG pipeline runs and the more it retrieves, the more dead weight piles up, and that's exactly the kind of dead weight DA is built to skip.

| | RAG | Declarative Attention |
|---|---|---|
| Solves | What content enters the context | How much of it gets re-read per step |
| Runs | Before generation, during search | During generation, at decode time |
| Fails when | Wrong or irrelevant chunks get retrieved | Model can't name a valid chunk |
| Maturity | Standard in production today | Zero-shot research result |

Neither one replaces the other. RAG decides what's on your desk, DA decides how much of the desk you actually reread for each sentence you write.

## My verdict

I think this is a genuinely interesting reframing of sparse attention, self-declared instead of externally scored, and it's backed by a real systems implementation (block-aligned vLLM integration), not just an idea on paper. The authors are also unusually honest about where it breaks, which I appreciated. That said, I wouldn't build on this yet. It fails too often on small, cheap models, doesn't support thinking-mode models, and the headline wall-clock numbers are a projected ceiling that leaves out prefill entirely. What I do think is worth watching closely is the direction, especially the paper's own argument that agentic and RAG-heavy setups are exactly where this should matter most. By the authors' own framing, these numbers are a floor, not a ceiling. The accuracy gap keeps closing as models scale, and none of this has even been trained for the task yet.

Who should actually care about this: if you're an engineer thinking about long-context or agentic RAG inference costs, keep an eye on it but don't build on it yet, especially not with small models or reasoning models. If you're a researcher in efficient attention, this is a genuinely new axis worth digging into, and the paper's discussion of synergy with speculative decoding and non-destructive KV-cache offloading is worth a full read beyond just this summary.

## Sources

- [Language Models Can Control Their Own Attention (arXiv:2609.02737)](https://arxiv.org/abs/2609.02737)
- [Paper page and author discussion on Hugging Face](https://huggingface.co/papers/2609.02737)
