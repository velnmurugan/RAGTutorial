Second Vector Reads post is up: a ByteDance Seed paper that trains an agent to write faster CUDA than torch.compile.

Most LLMs can write a CUDA kernel that runs correctly. Writing one that's actually fast is a different skill, and single-shot prompting doesn't get you there. This paper (CUDA Agent) trains a model specifically on that second skill with large-scale RL: it can compile, run, and profile its own kernel mid-attempt, and gets a graduated reward for how much it actually beats torch.compile by, not just "did it work."

The results: 98.8% pass rate on KernelBench, and its kernels beat torch.compile's own output 96.8% of the time, averaging a 2.11x speedup. On the hardest tier, it hits 90% faster-than-baseline vs. Claude Opus 4.5's 50%.

The ablations are what actually convinced me. Strip out the multi-turn loop and force a single-shot attempt, and the faster-rate collapses from 96.8% to 14.1%. That's the real story: it's not a bigger model, it's the loop and the reward design doing the work, and the numbers show it directly.

Same rule as always: if I can't explain it with a real worked example, I don't understand it well enough to write about it. This one also connects back to last week's post (Declarative Attention) in a way I found worth spelling out, different layer of the stack, same goal of squeezing more out of the same hardware.

Vector Reads → https://vectorspace.blog/vector-reads/00-overview

#LLM #MachineLearning #AI #CUDA #GPU #RAG
