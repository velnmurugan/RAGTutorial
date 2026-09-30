"""Settings for the paper scout. Edit these to make the scout yours."""
import os

# What you care about, in one sentence (Chapter 2).
INTEREST = ("papers about retrieval-augmented generation (RAG), or about "
            "making language models answer from documents they are given")

# The labeling guideline from Chapter 4, including the code rule from Chapter 9.
# The model gets these word for word, and you use the same rules when you label.
GUIDELINE = [
    "RELEVANT: a language model answers or writes using documents that are retrieved or given to it at run time.",
    "RELEVANT: the paper improves one part of such a system (chunking, retrieval for RAG, reranking, citations, evaluating RAG).",
    "RELEVANT: code documentation and code files count as documents when the model writes from them.",
    "NOT RELEVANT: retrieval with no language model writing from the results (for example, ranking products).",
    "NOT RELEVANT: 'retrieval' in another sense (for example, recalling facts from memory in psychology).",
    "NOT RELEVANT: work on language models that doesn't involve documents (for example, hallucination checks without sources).",
]

# Which arXiv categories to watch, and how many of the newest papers to check per run.
CATEGORIES = ["cs.CL", "cs.IR"]
MAX_PAPERS = 25

# Suggest a paper when the model's confidence is at least this (Chapter 6).
THRESHOLD = 0.5

# The model. Override it without editing code by setting SCOUT_MODEL.
MODEL = os.environ.get("SCOUT_MODEL", "gemini-3.5-flash")

# Pause after every model call, to stay inside free-tier rate limits.
SECONDS_BETWEEN_CALLS = 6

# How much of a paper's full text the model gets (characters).
FULL_TEXT_CHARS = 6000
