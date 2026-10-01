# ◎ Agentic AI: An Interactive Course

Twelve chapters, one running example: a paper scout that reads new AI
papers and suggests which ones are worth my time. I built it because
picking a paper for Vector Reads every week starts with skimming a
hundred abstracts, and I wanted to see how far a small agent could take
that over.

Every chapter starts from something that breaks, looks at why, adds one
fix, and runs into the next problem. The first three chapters build the
agent. The rest follow the CC/CD lifecycle (Continuous Development and
Continuous Calibration, from Aishwarya Reganti and Kiriti Badam's
article *Why your AI product needs a different development lifecycle*):
build the narrowest useful version, measure it, watch it on real use,
find the patterns in its mistakes, fix them, and only then let it do
more on its own. The last chapter deploys it on live arXiv papers with a
real model.

Chapters 1 to 11 run in your browser with hand-written stand-in model
replies, so every reader hits the same failures. Chapter 12 needs Colab
and a free Gemini API key.

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

## Capstone · Chapters 11-12

The whole loop one more time, one level up, and then the real thing:
the scout deployed on live papers, measured on real use.

::::{grid} 1 1 2 2

:::{card} Chapter 11 · The Capstone
:link: 11-capstone.ipynb

At "draft" the scout writes summaries, and some of its mistakes are the
kind only a reader can catch.
:::

:::{card} Chapter 12 · Deploy Your Scout (Production Lab)
:link: 12-deploy-your-scout.ipynb

The real scout on live arXiv papers: daily call limits, outages,
tests, deployment, cost, and an attempt to trick it.
:::

::::
