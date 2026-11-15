# Feedback-quality evals — turn "is this slop?" into a number

This is how the assistant's feedback (the project Advisor, the handoff grader, and the
per-repo `/review`) is kept honest: not by hoping it's grounded, but by **measuring** it
against cases where you already know the right answer, and tracking one number over time.

The number is **Cohen's κ** — how well the system's verdicts agree with *your* labels,
corrected for chance. The bar is **κ ≥ 0.70** (Landis & Koch "substantial"); below it,
you read the disagreements, fix the rubric/prompt, and re-run. You don't trust a feedback
system you haven't scored.

## The loop

1. **Grow the gold set** (`gold.json`) — real cases from your own work: a `finding`, the
   `change` that came back, and *your* `label` (`yes` / `partial` / `no` — did the change
   address the finding?). Your handoff records are already most of this; harvest them.
   Aim for **30–200** real cases (100–200 gets ~85% agreement achievable). Include a few
   **adversarial** ones — changes that *look* like they address the finding but don't
   (a comment instead of a test; a warning instead of enforcement; a disclaimer instead of
   a fix). Those are where slop hides.
2. **Record a run** — run those same cases through the feedback system (the app's grader,
   or a `/review`) and write down the verdict it gave for each, as `runs/<name>.json`
   (`{ "<caseId>": "yes|partial|no" }`). `node evals/score.mjs --template mine` writes a
   blank one to fill in.
3. **Score it** — `node evals/score.mjs runs/mine.json`. Read κ, the false-accept /
   false-reject counts, and the adversarial catch-rate.
4. **Fix and re-run** — read the disagreements (the scorer prints them, with the *why*).
   If κ < 0.70, tighten the grader's rubric/prompt and score again. Re-score monthly to
   catch drift.

## Files

- `gold.json` — the labeled cases (the ground truth). Edit this to grow the set.
- `score.mjs` — the scorer (stdlib Node, no deps, no API key). Computes κ, a confusion
  matrix, false-accept / false-reject on the "fully addressed?" gate, and the adversarial
  catch-rate; exits non-zero if κ < 0.70 (so it can gate CI).
- `runs/example.json` — a worked example so `score.mjs` prints real numbers out of the box.
  It's deliberately imperfect (κ ≈ 0.18) to show what catching slop looks like.

## Run

```
node evals/score.mjs                    # score the example run
node evals/score.mjs runs/mine.json     # score your recorded run
node evals/score.mjs --template mine    # write a blank run to fill in
```

## Reading the numbers

- **Cohen's κ** — the headline. ≥0.70 = substantial, safe to lean on. Lower = the system
  disagrees with you more than chance credit allows; don't automate on it yet.
- **False ACCEPT** — it rubber-stamped a change that wasn't actually done. For a merge
  gate this is the dangerous error; drive it toward zero on the gold set.
- **False REJECT** — it killed a change that was genuinely done (over-correction). Annoying,
  not dangerous, but it erodes trust and hides real progress.
- **Adversarial catch-rate** — of the trick cases, how many it got right. A high κ with a
  low adversarial catch-rate means it's fine on easy cases and blind on the hard ones —
  the most important number to watch.

## Honest limits

- Evals don't make LLM feedback *correct* — even calibrated, LLM code-review tops out around
  *moderate* accuracy. They make it **measurable, improvable, and honest about its own error
  rate**, with you as the final gate.
- **Never let the system grade its own work** as the ground truth — a model's self-check
  shows consistency, not correctness. The ground truth here is *your* label, the tests it
  didn't write, and — the non-gameable one — **real outcomes over time**: did the change you
  merged actually hold up? Fold those back into `gold.json` and the eval keeps getting truer.
