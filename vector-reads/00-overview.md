# ◈ Vector Reads: 10-Minute LLM Paper Reads

One recent LLM paper a week, in about 10 minutes. Not a bullet-point
recap of the abstract: each post walks through the real mechanism with a
worked example, an analogy that actually made it click for me, the honest
limitations the authors admit to themselves, and where it connects back to
RAG.

::::{grid} 1 1 3 3

:::{card} Language Models Can Control Their Own Attention
:link: 01-declarative-attention.md

A model that tells the inference engine which parts of the context it can
skip, cutting attention cost by up to 52% for almost no accuracy loss.
:::

:::{card} Teaching an LLM to Write CUDA Kernels 2x Faster Than torch.compile
:link: 02-cuda-agent.md

An agent trained with large-scale RL to write CUDA kernels, beating
torch.compile's own output 96.8% of the time.
:::

:::{card} BDH-CQ: A Reasoning Model That Never Says a Word While It Thinks
:link: 03-bdh-cq.md

A 150M-parameter model that reasons silently in latent space, learns new
tasks from examples with no weight updates, and beats every prior
cost-accuracy point on ARC-AGI-1.
:::

::::
