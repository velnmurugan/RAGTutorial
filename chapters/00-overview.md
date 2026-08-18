# ◉ Grounded AI: An Interactive RAG Tutorial Series

Ten chapters, one running example (a company employee handbook), built
from scratch. Every chapter follows the same shape: something breaks,
you see exactly why, one fix gets introduced, and that fix reveals the
next problem. The series is organized into four phases, each one
building directly on the last.

## Foundations · Chapters 1-3

Word-matching retrieval, embeddings, and chunking: the minimum ideas
any RAG system needs before it can answer a single question well.

::::{grid} 1 1 3 3

:::{card} Chapter 1 · What is RAG?
:link: 01-what-is-rag.ipynb

A general-purpose model has never seen your documents, so it can only
guess at answers specific to them.
:::

:::{card} Chapter 2 · What Are Embeddings?
:link: 02-embeddings.ipynb

Word-matching retrieval misses paraphrases like "holiday" vs
"vacation" because it only compares spelling.
:::

:::{card} Chapter 3 · Chunking Long Documents
:link: 03-chunking.ipynb

Embedding an entire multi-topic document as one vector dilutes the one
fact that actually matters.
:::

::::

## Building a grounded system · Chapters 4-5

Actually calling a model, and making sure a reader can check what it
says instead of just trusting it.

::::{grid} 1 1 2 2

:::{card} Chapter 4 · Completing the Loop
:link: 04-generation.ipynb

Retrieval has been built three different ways, but nothing has
actually generated an answer with a real model yet.
:::

:::{card} Chapter 5 · Trustworthy Answers
:link: 05-citations.ipynb

A generated answer with no visible source is impossible for a reader
to check.
:::

::::

## Better retrieval · Chapters 6-8

Scaling search past a handful of chunks, and two genuinely different
ways retrieval still gets things wrong.

::::{grid} 1 1 3 3

:::{card} Chapter 6 · Scaling Retrieval
:link: 06-scaling.ipynb

Comparing a question against every chunk one at a time stops being
fast once there are millions of them.
:::

:::{card} Chapter 7 · Hybrid Search
:link: 07-hybrid-search.ipynb

Semantic retrieval understands meaning but sometimes loses exact
identifiers, like a number or a code.
:::

:::{card} Chapter 8 · Re-ranking
:link: 08-reranking.ipynb

A bi-encoder's averaged comparison can wash out the one decisive word
in a question.
:::

::::

## Evaluation & integration · Chapters 9-10

Measuring instead of arguing from examples, then assembling everything
into one system and finding its real limits.

::::{grid} 1 1 2 2

:::{card} Chapter 9 · Evaluation
:link: 09-evaluation.ipynb

Every case for "this technique is better" so far has been one
hand-picked example, not a measurement.
:::

:::{card} Chapter 10 · The Capstone
:link: 10-capstone.ipynb

Combining every technique in this series doesn't automatically combine
their strengths.
:::

::::
