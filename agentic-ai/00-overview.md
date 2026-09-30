# ◎ Agentic AI: An Interactive Course

Eleven chapters, one running example (a paper scout that reads new AI
papers and suggests which ones to read), built from scratch. Every
chapter follows the same shape: something breaks, you see exactly why,
one fix gets introduced, and that fix reveals the next problem.

The course is organized around one idea: an agent isn't finished when
it runs. After three chapters of foundations, the rest follows a
build-then-calibrate loop: build the narrowest useful version, measure
it, watch it on real use, find the patterns in its mistakes, fix them,
and only then let it do more on its own.

## Foundations · Chapters 1-3

The loop, the model, and the tools: the minimum an agent needs before
it can do anything useful, and the first question about how much it
should do without you.

::::{grid} 1 1 3 3

:::{card} Chapter 1 · What is an Agent?
:link: 01-what-is-an-agent.ipynb

A script with fixed steps summarizes the wrong paper when its results
surprise it, because it never looks before taking the next step.
:::

:::{card} Chapter 2 · Letting a Model Decide
:link: 02-letting-a-model-decide.ipynb

Hand-written rules match words, not topics, and every new kind of paper
needs another rule.
:::

:::{card} Chapter 3 · Tools and the Autonomy Dial
:link: 03-tools-and-autonomy.ipynb

A model that can only judge what's in its prompt can't go and read
more, and once it can act, one good run says nothing about the next.
:::

::::

## Continuous Development · Chapters 4-6

Building on purpose: a narrow scope, labeled examples, a first version
that stays inside its limits, and a real measurement before shipping.

::::{grid} 1 1 3 3

:::{card} Chapter 4 · Scope and Curate Data
:link: 04-scope-and-data.ipynb

Tweaking the prompt after every bad run means steering by the last
example you happened to look at.
:::

:::{card} Chapter 5 · Set Up v1
:link: 05-set-up-v1.ipynb

A written scope and a list of labels don't do anything until a scout
exists that follows them.
:::

:::{card} Chapter 6 · Design Evals and Deploy
:link: 06-evals-and-deploy.ipynb

"The suggestions look fine" is an impression, and it can't see a
single missed paper.
:::

::::

## Continuous Calibration · Chapters 7-10

What happens after shipping: measuring real use, reading mistakes until
they turn into patterns, fixing without breaking, and earning the next
level of autonomy.

::::{grid} 1 1 2 2

:::{card} Chapter 7 · Run Evals on Real Use
:link: 07-real-use.ipynb

An eval only covers the papers you chose, and real use brings papers,
and problems, you never thought of.
:::

:::{card} Chapter 8 · Find Error Patterns
:link: 08-error-patterns.ipynb

Two falling numbers say that something is wrong, but not what.
:::

:::{card} Chapter 9 · Apply Fixes
:link: 09-apply-fixes.ipynb

Every fix changes the system the other mistakes live in, and some fixes
break what used to work.
:::

:::{card} Chapter 10 · New Metrics and Earning Autonomy
:link: 10-new-metrics-and-autonomy.ipynb

A scout can beat the old version on every number you track and still
get worse at something none of them measure.
:::

::::

## Capstone · Chapter 11

The whole loop one more time, one level up, and a final answer to how
far up the dial the scout should go.

::::{grid} 1 1 1 1

:::{card} Chapter 11 · The Capstone
:link: 11-capstone.ipynb

At "draft" the scout writes summaries, and some of its mistakes are the
kind only a reader can catch.
:::

::::
