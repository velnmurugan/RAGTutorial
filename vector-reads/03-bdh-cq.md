# BDH-CQ: A Reasoning Model That Never Says a Word While It Thinks

*10-min paper read · [BDH-CQ: In-Context Learning with Recurrent Latent Reasoning](https://arxiv.org/abs/2608.09888), Björn Engdahl, Adrian Kosowski, Jan Chorowski, Zuzanna Stamirowska, Przemysław Uznański, Junlin Jiang, Rohan Phadke, Remigiusz Kinas, Richard Zhong (Pathway / Bielik AI / NYU)*

## TL;DR

Most LLMs reason by writing out their thinking, token by token, then reading it back in before the next step. BDH-CQ tries a different combination. It learns a new task from examples the normal in-context way, but does all the actual reasoning silently, by transforming an internal vector over and over, never converting it to words until the final answer. Tested on the ARC-AGI-1 puzzle benchmark, a 150M-parameter version hits 29.5% pass@2 at a computed cost of $0.0007 per task, under a tenth of a cent, and cheap enough to beat every previously reported point on the benchmark's cost-accuracy frontier.

## Where this fits in

The paper positions itself between two lines of work that, until now, hadn't been combined.

Chain-of-thought models learn new tasks flexibly from examples in the prompt, but every reasoning step has to become a written token before the model can use it, which is expensive at scale. Separately, "latent reasoning" models like Coconut (Hao et al., 2024) showed a model can feed its own hidden state back into itself instead of writing words out, but those systems didn't also learn new tasks from demonstrations at inference time. And separately again, task-trained recursive solvers like HRM and TRM do strong iterative reasoning on ARC, but they cheat a little. They actually optimize on the evaluation task's own demonstration pairs before answering, meaning each new puzzle needs its own mini training run.

BDH-CQ's claim is that it does both things at once. It learns an unseen task purely from demonstrations shown at inference time, no weight updates, no per-task optimization, and it reasons about that task entirely inside a continuous latent space, never verbalizing intermediate steps.

## How it actually works

There are two separate stages, and it's worth keeping them apart because the paper does.

**Stage 1, learning the task (memory).** The model is given a handful of demonstration examples (an ARC task typically has 2-3 input to output grid pairs). Instead of stuffing all of them into a growing context window, the model updates a fixed-size internal memory state one demonstration at a time:

```
S_t = U(S_{t-1}, D_t)
```

Each new demonstration D_t nudges the memory S forward. By the time all demonstrations are seen, S_K holds whatever the model has picked up about the rule: colour mapping, symmetry, propagation, whatever the task actually is.

**Stage 2, solving the query (reasoning).** Now the model takes the new puzzle input and the memory it just built, and iterates:

```
H_0 = E(query, S_K)
H_1 = F(H_0, S_K)
H_2 = F(H_1, S_K)
...
H_R = F(H_{R-1}, S_K)
answer = G(H_R)
```

Each step from H_r to H_{r+1} is the model thinking again, but it's a direct transformation of a fixed-size vector, not a generated word getting fed back in. Only after R rounds of this does it decode a final answer. Nothing in between ever becomes text. R is a knob: more rounds means more compute and, per their results, a better answer.

That's genuinely the whole mechanism. No new vocabulary, no scratchpad, no retrieval step per round, just repeatedly reshaping one blob of numbers.

## An analogy that helped me get it

Picture a translator working a live negotiation. A chain-of-thought model is like a translator who has to say every intermediate thought out loud in the room, in the shared language, before moving to the next thought, even "let me think about the wording here" gets spoken.

BDH-CQ is a translator who reads the demonstration material, forms an understanding of it privately, then mulls the actual answer over silently, turning it over in their head a fixed number of times, and only opens their mouth once, to give the final translation. The mulling is real work, it's just never rendered into the shared language along the way.

And because the "notebook" they're mulling over is a fixed size rather than a growing transcript, mulling twice as long doesn't mean re-reading twice as much material. It's the same blob, reshaped again.

## The evaluation, in detail

This is where the paper earns real credit. It doesn't just report one headline number and stop.

**Headline result.** On the public 400-task ARC-AGI-1 evaluation set, the 150M model gets 29.5% pass@2 (118/400 tasks), at $0.00070 computed cost per task. Plotted against the official ARC Prize leaderboard, this point sits beyond every previously reported system's cost-accuracy trade-off. Nothing else scores this well this cheaply. For comparison, they estimate it's roughly 57x cheaper than GPT-5.6 Luna (Low) at similar accuracy, or about 11x cheaper after accounting for a later API price cut.

**Independent audit.** A black-box audit by co-authors outside the core team (Bielik AI, NYU) reproduced the 29.5% score without access to model weights, which is a real credibility signal. This isn't just self-reported.

**Where it's strong.** On ConceptARC (a benchmark organized into 16 labeled concept families), things like `ExtendToBoundary`, `FilledNotFilled`, and `TopBottom2D` hit 9/10 tasks. In controlled follow-up tests they built themselves, boundary propagation stayed perfect across distances 2 through 8 (48/48), and copying a motif to up to 4 anchor points stayed perfect too (48/48). Neither showed any sign of hitting a ceiling in the range tested. Dense task-specific colour remapping (learned purely from context) also held up on all 96 held-out cases, scaling from 2 to 8 simultaneous colour swaps.

**Where it breaks.** Two areas fall off a cliff. Ordering: sorting bars by height stays near-perfect through 5 objects, then collapses. 8/24 correct at 7 objects, 1/24 at 8. Nesting: staying accurate through depth 4, then dropping to 29/36 at depth 5. Composition of operations is patchy too. Rotation-plus-relocation works on all 72 held-out cases, reflection-plus-relocation works on only 47/72, and colour-swap-plus-relocation works on literally none of 72.

**The important twist.** When they gave the model one demonstration at the same difficulty level as the failing test case, depth-5 nesting jumped from 19/24 to 24/24, and length-8 ordering recovered from 0/24 to 13/24. So a good chunk of the "failure" isn't a hard capability ceiling, it's that the model hadn't been shown anything that hard before being asked to do it. Ordering did keep a partial bottleneck even with support, so it's not a total explanation, but it reframes the failures as partly a lack of coverage rather than pure incapacity.

**Consistency check.** 52 of 160 ConceptARC tasks got 1 or 2 of their 3 test inputs right, but not all 3, meaning the model doesn't always apply the same inferred rule consistently across similar inputs within one task.

**Confound-hunting.** They reran ConceptARC with semantic task labels replaced by opaque cryptographic ones, and mixed the concept-grouped batches up. Aggregate score barely moved (374/480 vs. 374/480 test pairs), which rules out the model just exploiting label leakage rather than actually reading the grids.

**Effort scaling.** They trained the model at three internal reasoning depths (LOW/MEDIUM/HIGH). Pass@2 rises from 21% to 27% to 29.5% as depth increases, with roughly matching cost increases: a clean, if unsurprising, "more silent thinking, better answer" curve.

## Where I'd push back

The paper is upfront about a lot of this itself, which helps:

- Everything is ARC-only. No language or math reasoning is demonstrated, just claimed as future work.
- "Dimensions, exact update rules, and implementation details remain proprietary," so the field can't fully reconstruct or verify the architecture from this paper alone.
- No visibility into why it got something wrong. A correctly-inferred rule applied incompletely looks identical, from the outside, to an incorrectly-inferred narrower rule. You only ever see grids in and grids out.
- 29.5% is a strong cost-efficiency point, but it's well below frontier LLMs with heavy test-time compute on the same leaderboard. This is a win on the cost axis, not the raw-capability axis.

## My verdict

This is a genuinely new combination, in-context task learning plus fully non-verbal iterative reasoning, evaluated as one complete costed system, independently audited. The cost result is real and the failure analysis is unusually honest and specific rather than hand-wavy. But it's a narrow, single-domain result (ARC-style visual puzzles) from a specialized startup lab, with core implementation details kept proprietary, and clear architectural limits on anything needing long sequential construction. Worth watching as a direction, not yet something to build production systems on.
