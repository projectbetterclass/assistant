# Testing and publishing time-tracker.html

Browser checks for the app, and the script that publishes new code without touching the saved data. They run against
`tests/page.html`: the new code with the live app's saved data in it. That file holds your data, so it is never committed
(see `.gitignore`); this folder is public.

Needs Node and Playwright with Chromium (`npm i -D playwright && npx playwright install chromium` on a new machine).

## 1. Build the page to test

1. Read the live artifact with the Artifact tool (`action: "read"` on the app's URL). It saves the whole page to a file.
2. Get the code that is live now: the commit that was last published, e.g. `git show <commit>:time-tracker.html > tests/prev.html`.
3. Put the new code around the live data:

```
node tests/build-next.mjs tests/prev.html <saved live page> time-tracker.html tests/page.html
```

`build-next.mjs` stops if the live page isn't running `prev.html`'s code (someone published in between), and otherwise
writes the new code with the live saved data byte-for-byte unchanged.

## 2. Run the checks (from `tests/`)

| Check | What it covers |
|---|---|
| `node coursecheck.mjs <goal> <prefix> <n>` | one course, every lesson: thread, idea, walk-through, numbers, answer, revisit. `goal_fire F 12`, `goal_build P 9`, `goal_biz B 15`, `goal_opt H 18`, `goal_fx X 12`, `goal_career C 15`, `goal_pbi Q 12` |
| `node learncheck.mjs` | investing sittings, Learn step |
| `node refcheck.mjs` | tappable D-xx rule references |
| `node revcheck.mjs` | revisits: their own numbers and closed answers |
| `node flows.mjs`, `smoke.mjs` | the main screens and flows |
| `node parts.mjs` | lessons in two halves: part 1 learn it, part 2 do it, and Done counts the day |
| `node shot-test.mjs` | starting a task from a screenshot |
| `node docs.mjs` | the doctrine cards |
| `node shot-all.mjs` | every investing lesson at phone width |
| `node deep.mjs` | clicks every card and link in every course; flags links that aren't videos (source links are expected) |

All must pass before publishing. A new course gets its lessons checked with `coursecheck.mjs`.

## 3. Publish

Build the same way from a fresh read of the live page (the app saves itself, so the data may have changed), compare it
with the tested page apart from the saved data, and publish it to the same artifact URL, leaving out `capabilities`
and `icon` so the page keeps them. Commit and push the code first.
