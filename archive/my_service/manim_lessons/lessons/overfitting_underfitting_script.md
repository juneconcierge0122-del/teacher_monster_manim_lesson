# Overfitting vs Underfitting — Narration Script
**Lesson file**: `overfitting_underfitting.py`
**Target length**: ~5 minutes (8th grade, 10 min focus → use ~50% of attention)
**Audio language**: English (matches script content)

---

## Scene 1 (Hook) — about 45 seconds

`[3 student boxes appear one by one]`
> Three students are about to take a math test.

`[Anna box highlighted]`
> Anna didn't study. She'll guess on every question.

`[Ben box highlighted]`
> Ben memorized every problem from past quizzes — word for word.

`[Cathy box highlighted]`
> Cathy understood the underlying concepts.

`[question line appears at bottom]`
> Now the test has NEW questions, never shown before.
> Who passes?

---

## Scene 2 (What's a model) — about 50 seconds

`[heading "What is a 'model'?"]`
> Before we answer, one quick word.

`[teach_concept block: Model]`
> A "model" is just a rule. It takes some input — and gives a prediction.

`[flow diagram: input → rule → output]`
> See a red, round fruit?
> The rule says "apple."
> That's a model. Nothing fancy.

---

## Scene 3 (Misconception) — about 75 seconds

`[scatter dots and axes appear]`
> Now imagine these dots are practice problems we've already seen.

`[green straight line drawn]`
> Here's a simple rule — one straight line. It misses some dots, but it captures the trend.

`[red squiggly curve drawn through every dot]`
> Here's a fancy rule. It touches every single dot perfectly.
> So... is the fancy one better?

`[yellow "new question" dot appears off the curves]`
> Let's see. Here comes a NEW question.

`[scatter fades to misconception panel]`
> Many people think a more complex rule is always better.

`[right green panel appears]`
> But here's what really happens:
> A complex rule memorizes the old data — and FAILS on new data.

---

## Scene 4 (U-curve) — about 90 seconds

`[teach_concept: Training error]`
> So we measure two things.
> First: training error — how wrong our rule is on OLD problems we've already seen.

`[teach_concept: Test error]`
> Second: test error — how wrong on NEW problems we haven't seen.

`[teach_concept: Complexity]`
> And one more idea — complexity. Just means: how fancy is the rule? Straight line is simple. Wavy curve is complex.

`[axes appear]`
> Now watch what happens as we make the rule more and more complex.

`[green training error curve drawn, sweeping down]`
> Training error always goes DOWN. The fancier the rule, the better it fits the OLD data.

`[red test error U-curve drawn]`
> But test error — does this. It goes down, hits a minimum, then back UP.

`[3 colored bands appear: underfit, sweet spot, overfit]`
> Three regions. On the left — too simple. We call that underfitting.
> On the right — too complex. That's overfitting.
> In the middle — the sweet spot.

`[green dot at curve minimum]`
> Right where test error is lowest. That's the rule we want.
> This ability to do well on NEW data — generalization — is the whole point.

---

## Scene 5 (Connect students) — about 45 seconds

`[heading "Same idea, in plain words"]`
> Now let's go back to our three students.

`[row 1 appears]`
> Anna didn't study. Both her training error AND test error are high. She underfits.

`[row 2 appears]`
> Ben memorized everything. His training error is low — he aces practice quizzes. But test error is high. He overfits.

`[row 3 appears]`
> Cathy understood the concepts. Both errors are low. She's at the sweet spot.

---

## Scene 6 (Framework) — about 50 seconds

`[framework title and steps appear, framed in box]`
> When you build a new model, ask three questions.
> Is training error high? Your rule is too simple. Underfitting.
> Is training error low but test error high? Your rule memorized. Overfitting.
> Are both low? You're at the sweet spot. Ship it.

> That's the trade-off. The best model is never the most complex one.

---

## Recording notes

- 8th grade audience: keep words short, no jargon beyond what's defined
- Slow down on "underfit / overfit / sweet spot" — these are NEW words
- Smile in voice on Cathy ("understood the concepts") and on the final "Ship it"
- 0.5 sec pause before each new student row in Scene 5

## Preflight (must pass)
- No meta sentences left in narration
- No leftover placeholders
- All 6 lacks concepts introduced via teach_concept: model, training error, test error, complexity, overfitting, underfitting
- Misconception explicitly addressed (Scene 3)
- Closing framework (Scene 6, boxed)
- The point about generalization (doing well on NEW unseen data) is implicit throughout — make it explicit in Scene 4 narration
- Total length about 5 minutes (well under 10 min focus)
