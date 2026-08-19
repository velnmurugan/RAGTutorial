I just finished building something I wish existed when I was learning this myself: an interactive RAG tutorial where you build every piece from scratch instead of just reading about it.

It's called Grounded AI. Ten chapters, runs in the browser, no setup.

You start with the simplest retriever possible (word matching), watch it fail on a paraphrase like "holiday" vs "vacation," then build real embeddings from nothing but word co-occurrence counts and a bit of linear algebra to fix it. From there: chunking long documents, actually calling a language model and grounding its answers, citations, scaling retrieval to millions of documents, hybrid search, re-ranking, and a real evaluation chapter that found something I hadn't designed in advance (re-ranking made results worse in one case, and I had to trace exactly why before I believed it myself).

The capstone assembles everything into one system, and you discover hands-on that no single combination of techniques passes every test. That's the point.

Every chapter follows the same shape: build something, break it on purpose, understand why, fix exactly one thing. I research AI and technical education for a living, and this is the tutorial I'd want a student to actually learn from, not just watch.

Grounded AI → https://vectorspace.blog/chapters/00-overview

If you build something with it, or find a bug, I'd genuinely like to hear about it.

#RAG #MachineLearning #AI #TechnicalEducation
