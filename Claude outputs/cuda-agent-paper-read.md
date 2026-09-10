# Teaching an LLM to Write CUDA Kernels 2x Faster Than torch.compile

*10-min paper read · [CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation](https://arxiv.org/abs/2602.24286), Weinan Dai, Hanlin Wu, Qiying Yu, Huan-ang Gao, Jiahao Li, Chengquan Jiang, Weiqiang Lou, Yufan Song, Hongli Yu, Jiaze Chen, Wei-Ying Ma, Ya-Qin Zhang, Jingjing Liu, Mingxuan Wang, Xin Liu, Hao Zhou (ByteDance Seed)*

## TL;DR

Writing a CUDA kernel that just works is one skill. Writing one that's actually fast is a completely different, much harder skill, one that even today's best LLMs struggle with when you just ask them directly in a single prompt. This paper trains an agent specifically to get good at that second skill using large-scale reinforcement learning, instead of just asking a general-purpose LLM to write CUDA in one shot.

The result on KernelBench: a 98.8% pass rate, and the kernels it writes beat `torch.compile`'s own output 96.8% of the time, averaging a 2.11x speedup over compiled code and 2.60x over plain eager-mode PyTorch. On the hardest tier of tasks, it hits a 90% faster-than-baseline rate, compared to Claude Opus 4.5's 50%.

## Where this fits in

The paper splits prior work into two camps, and names real systems in each. One camp is training-free: systems like STARK, ReGraphT, EvoEngineer, and CudaForge that search over many candidate kernels using execution feedback, but lean entirely on whatever CUDA ability the base model already has, without ever actually improving that underlying ability. The other camp fine-tunes: systems like Kevin, CUDA-L1, and ConCuR that use supervised fine-tuning or RL, but the paper argues these stay boxed in by scarce high-quality training data, limited training scale, and hand-designed loops that don't generalize well.

CUDA Agent's own approach builds on the "Agent Skills" paradigm and PPO (Proximal Policy Optimization, a standard reinforcement learning algorithm), adapted specifically for long, multi-turn CUDA development sessions rather than a single-shot answer.

## How it actually works

Three pieces, working together.

**First, a data synthesis pipeline**, since you can't do large-scale RL without a large-scale supply of practice problems, and someone has to write those problems. It runs in three steps:

1. Crawl seed operators straight out of real PyTorch and Transformer library code, building a repository of fundamental computational building blocks. (Like a teacher first gathering real vocabulary words and basic building blocks from actual textbooks, rather than making them up.)
2. An LLM then performs combinatorial synthesis, combining those basic operators into new, fused, multi-operator tasks. (Like combining those vocabulary words into new, more complex practice sentences.)
3. A rubric-based filtering stage keeps only the problems that are executable, deterministic, non-trivial, and have a reasonable workload, tossing out anything broken, trivial, or unreliable. (Like a teacher reviewing the homemade worksheet afterward and throwing out any broken or pointless questions before handing it to the student.)

![Data synthesis pipeline: seed problem crawling from PyTorch/Transformers, combinatorial problem synthesis by an LLM, rubric-based problem filtering](./images/paper_2/Fig_01.png)

Second, a "skill-augmented" development environment. This is the part that matters most: while the agent works, it can actually compile and run its code, check whether the output is numerically correct, and profile how fast the kernel really runs, all automatically. That gives it a real, trustworthy reward signal instead of a guess.

![Skill-augmented development environment: SKILL.md and a kernels/utils workdir feed the CUDA Agent, which runs on a GPU pool and gets back generated kernel files plus correctness and performance results](./images/paper_2/Fig_02.png)

The exact reward function is worth showing directly, because it's more specific than "good" or "bad." A completed attempt scores -1 if the correctness check fails, 3 if it beats both eager-mode PyTorch and the compiled baseline by more than 5%, 2 if it beats eager mode by more than 5% but not the compiled baseline, and 1 otherwise (correct, but no meaningful speedup). So it's a graduated scale, not pass or fail: clearing a higher performance bar earns a meaningfully bigger reward than just being correct.

**Third, training happens in stages** rather than all at once, each one building on the last:

1. Single-turn warm-up: the model first practices writing one kernel per attempt, no iteration yet, just building basic ability before anything harder gets layered on.
2. Rejection fine-tuning (RFT): the system collects the model's own best, most successful attempts so far, and fine-tunes it further specifically on those, reinforcing what already worked instead of training on generic examples.
3. Value pretraining: a separate internal "critic" is trained to judge, partway through an attempt, how promising that direction actually is. This gives the model an early sense of when to keep going versus when to change approach, instead of blindly finishing every path it starts.
4. Full agentic RL: everything comes together, and the model practices the complete real loop, up to 200 turns per task with a 131,072-token context window, writing, testing, measuring, and retrying, scored by the graduated reward described above.

![Training pipeline: single-turn warm-up produces a base single-turn model, agent warm-up branches into RFT on sampled trajectories (actor model) and value pretraining (critic model), then full agentic RL with PPO produces the final CUDA Agent](./images/paper_2/Fig_03.png)

The paper's example section names three real case studies it evaluated on: a Level-1 task multiplying a diagonal matrix, a Level-2 task chaining matrix multiplication with division, summation, and scaling, and a Level-3 task optimizing a ResNet BasicBlock.

## An analogy that helped me get it

Picture a student learning to solve a genuinely hard kind of problem, working with a teacher who checks every attempt immediately and grades it properly, not just right or wrong, but how well it's done. Get it correct but sloppy, and you get a passing grade. Get it correct and genuinely well done, clearing a real standard, and you get full marks. Get it wrong, and you're told exactly that and sent back to try again right away. Over hundreds of attempts at the same kind of problem, with the teacher grading every single one in real time, the student keeps refining their approach based on actual feedback, not guesswork.

Now picture a different student who only ever reads the textbook and turns in one single attempt, with no teacher present to grade it or hand it back. They might write something that looks like a reasonable answer. Whether it's actually good, or just looks plausible on the page, they have no way of knowing.

That's the real difference this paper demonstrates. A normal LLM asked to write a fast kernel in one shot is the second student: working from what it read, with nobody checking whether its guess actually holds up. CUDA Agent is the first student: given a teacher in the room (the automated verification and profiling) and a real grading rubric (the graduated reward function), allowed hundreds of attempts at the same task, correcting course each time based on what actually happened rather than what it hoped would happen.

## The numbers that back this up

The full picture across KernelBench's three tiers: Level 1 (single operators) gets a 97% faster-than-baseline rate and a 1.87x speedup over compiled code. Level 2 (chained operators) actually does best, 100% faster-rate and a 2.80x speedup. Level 3 (complex, multi-operator models) is hardest but still strong at 90% faster-rate, well ahead of Claude Opus 4.5's 50% and Gemini 3 Pro's roughly 70% on the same tier.

For general comparison, here's the full leaderboard the paper reports on KernelBench:

| Model | Pass rate | Faster-than-baseline rate |
|---|---|---|
| CUDA Agent | 98.8% | 96.8% |
| Claude Opus 4.5 | 95.2% | 66.4% |
| Gemini 3 Pro | 91.2% | 69.6% |
| Seed 1.6 (base model, no CUDA Agent training) | 74.0% | 27.2% |

The ablations are where the real story is, though. Strip out the multi-turn agent loop, forcing a single-shot attempt instead, and the faster-rate collapses from 96.8% down to 14.1%. Strip out the graduated reward design specifically, and it drops 36 percentage points. Remove value pretraining, and the model's internal sense of "is this worth pursuing" breaks down, leading to long, inefficient trajectories that wander instead of converging. Each of these tells you which piece is actually doing the work, and it's clearly the loop and the reward design, not just a bigger or smarter base model.

One more real detail worth including: training wasn't smooth from the start. The paper mentions training collapsed after just 17 steps before the authors added their warm-up stage to stabilize it. Worth knowing, since it's easy to read a clean final result and assume the process to get there was equally clean.

## Where I'd push back

A few real gaps, not invented ones:

**No comparison against the specific systems it's positioned against, and at least one of them already claims a bigger number.** The paper names Kevin, CUDA-L1, ConCuR, STARK, ReGraphT, EvoEngineer, and CudaForge directly as prior work, but the actual benchmark table only compares CUDA Agent against general frontier models (Claude Opus 4.5, Gemini 3 Pro, GLM 4.6, Kimi K2) and its own untrained base model. That gap matters concretely here: CUDA-L1, one of the systems named directly as prior work, separately reports a 2.77x average speedup over torch.compile on the same KernelBench suite, versus CUDA Agent's own 2.11x. CUDA Agent's paper never puts these two systems side by side, so the "2x faster than torch.compile" headline is real and paper-verified, but it isn't the best number posted against torch.compile on this benchmark, just the best one this specific paper chose to report.

**Demonstrated scope is KernelBench, not "all CUDA."** Everything here is shown on a specific benchmark with three defined tiers. That's a real, broad test, but it's still a defined scope. Whether this generalizes to kernel-writing tasks well outside that distribution, a brand-new GPU architecture, or workloads structurally unlike anything in KernelBench, isn't something the paper demonstrates, and I'd be careful extrapolating past what's actually shown.

## Where this connects

This pairs naturally with last week's post. Declarative Attention made inference cheaper by changing what the model attends to at inference time, no new kernels required. CUDA Agent works a layer deeper: instead of changing how an existing kernel gets used, it writes an entirely new, purpose-built kernel for a specific situation. Different layer of the stack, same underlying goal of squeezing more speed out of the same hardware.

## My verdict

The core finding is genuinely convincing, and the ablations are what make it convincing: this isn't "we used a bigger model," it's "we built the specific loop and reward signal this skill needs," and the numbers back that claim up directly. The margin over Claude Opus 4.5 on the hardest tier (90% vs 50%) is real and substantial.

The one open question worth keeping in mind is how it stacks up against the specialized systems it names as prior work, since the published numbers only compare it to general frontier models. Worth watching for that comparison.

**Who should care:** anyone doing GPU performance work curious whether this kind of automation is getting practical; researchers in agentic RL and coding agents, since the ablation results here are a clean demonstration of exactly which design choices earn their keep.

## Sources

- [CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation (arXiv:2602.24286)](https://arxiv.org/abs/2602.24286)
- [Paper page on Hugging Face](https://huggingface.co/papers/2602.24286)
