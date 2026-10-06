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

## Reading YouTube transcripts (for lessons)

The video library from the `youtube-digest` project is available to chats here.
`scripts/video_source.py` pulls one video's **transcript** and, where screen
capture has run, its **on-screen charts/slides** (read by Claude vision, with
the time in the video), matched by video id:

```
py scripts/video_source.py https://www.youtube.com/watch?v=<id>
py scripts/video_source.py --find "damodaran equity risk premium"
py scripts/video_source.py <id> --out notes/<name>.md
```

To find **which** videos a lesson should come from, search what is said and
shown in every video of every channel (~7,600 videos). Results are ranked by how
many of your words a video contains, then how much it is *about* them, each with
its best excerpt:

```
py scripts/video_source.py --search "spaced repetition" --channel "justin sung"
py scripts/video_source.py --search procrastination --k 20
py scripts/video_source.py --search motivation --phrase "dopamine detox"
```

Words match whole (plus plurals; "studying" also finds "study"), `word*` matches
a prefix, and exact phrases go in quotes (`'like this'` in PowerShell) or
`--phrase`. `--channel` narrows to channels whose name contains it; `--k` sets
how many videos come back (default 10). Then open the best hits with
`py scripts/video_source.py <url>` to read them in full.

It reads the copy on the PC first (`Downloads/Youtube Scraper`) and falls back
to the public GitHub repo, so it works from a phone/cloud session too. Covers
every channel in the library (Aswath Damodaran, Justin Sung, HealthyGamerGG, …).
`--search` needs the library on disk: on the PC it just works (about 1 s with
`--channel`, a few seconds across everything, longer while the PC is busy); in
a phone/cloud session the first search prints a one-time `git clone` command to
run.
Use it when writing or checking lessons, e.g. for `valuation_curriculum.json`:
quote what was said, cite the video link, and treat chart readings as possibly
misread (check a number against the video before relying on it).
