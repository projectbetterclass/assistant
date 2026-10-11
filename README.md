# Where My Time Went

A personal time-tracking assistant: start/stop timers, planned tasks with
estimate-vs-actual, a capture inbox, goals broken into daily actions, a
deep-work scoreboard, streaks, and a Bloom's-taxonomy skill ladder for
progressive overload on what you're learning.

**Live app:** https://claude.ai/code/artifact/98a84d40-cd2d-436d-8ea5-831db36dccbb

## How this project actually works

This is **one self-contained HTML file** (`time-tracker.html`). It is not a
normal deployed web app — it's a Claude **Artifact**. Publishing the file
through the Artifact tool *is* the deployment; there's no build step, no
host, no CI.

The live page also **saves its own data**: every time you start/stop a
timer or edit a goal, the page rebuilds itself (styles + script + your
current data) and republishes itself to the same URL via the `artifact`
capability. So the live version's `<script id="app-state">` block always
holds your real, current data — which will usually be *ahead of* whatever
is committed here in git.

## This repo vs. the live app

| | This GitHub repo | The live Artifact |
|---|---|---|
| Holds | Versioned history of the **code** | The **running app + your real data** |
| Updated by | `git commit` / `git push` | The Artifact tool's `publish` action |
| Push here does... | ...nothing to the live app | — |

**Pushing to GitHub does not update the live app.** They're two separate
systems on purpose — this repo is a backup/history of the code, not the
deploy mechanism.

## Making a change (from anywhere — including your phone)

1. Open a Claude Code session (desktop app, or `claude.ai/code` in any
   browser, including your phone's).
2. Give it this project's context — either point it at this repo, or use
   the starter prompt in [`build-on-phone-prompt.txt`](build-on-phone-prompt.txt).
3. **Before editing:** read the *live* artifact at the URL above to get the
   current HTML — it has your real logged data, which this repo's copy does
   not.
4. Make the code change, keeping the live `<script id="app-state">` JSON
   intact (that's the user's real data — never replace it with old/seed
   data from this repo).
5. **Publish** the merged file to the *same* artifact URL (pass it as
   `url`) — this updates the live app.
6. **Commit** the code change here and push — this updates the history.

Steps 5 and 6 are both needed for a change to be "done": publish makes it
live, commit keeps a record.

## Articles (the reading shelves)

Short reads live on three shelves, each on one goal:

| Shelf | Goal | What's on it |
|---|---|---|
| `invest` (the default) | Long-term investing | "From your channels": the stock-commentary videos, newest first |
| `business` | Business: offers & sales | Alex & Leila Hormozi videos, as a numbered path |
| `books` | Read 20 minutes a day | Chapter notes, in my own words, for the books on the shelf |

Each one is a markdown file in [`articles/`](articles/) with a small header:
`id`, `channel` (for a book: its title), `title`, and either a `date` (dated
videos) or an `n` (the place in a path or on the shelf). Optional: `shelf`,
`videoMin`, `part` (a chapter, e.g. `Ch. 3–4`), `by` (a book's author),
`checked`, `charts`. Lesson ids such as `L08` or `P02` in the text become
links to the lesson. They ship in their own `<script id="app-articles">` block,
separate from the code and from your data, and the page carries that block
along when it republishes itself. To add a batch: write the files, run
`node scripts/build-articles.mjs`, then publish as above. Only what you've
read is saved in app-state (`artRead`).
