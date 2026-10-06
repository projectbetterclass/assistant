"""Pull one YouTube video's words AND its on-screen charts from the youtube-digest library.

The youtube-digest project (a separate repo, projectbetterclass/youtube-digest) archives
every watched video under data/archive/<video_id>/:
  * transcript.md -- what is said (YouTube captions)
  * visuals.md    -- for chart-heavy channels, the slides/charts read off the screen by
                     Claude vision, each with its time in the video
Both are filed by the YouTube video id, so they always belong to the same video. Use this
when writing or checking a lesson from a video (e.g. the Damodaran curriculum in
valuation_curriculum.json): quote what was actually said, and use the chart readings for
numbers that are shown but not said out loud.

    py scripts/video_source.py https://www.youtube.com/watch?v=_ABDiQYrSw0
    py scripts/video_source.py _ABDiQYrSw0 --out notes/agi.md
    py scripts/video_source.py --find "damodaran equity risk premium"

Or search every video in the library -- every watched channel, what is said AND shown --
for a topic, ranked, with the best excerpt from each (to find the videos a lesson
should be built from):

    py scripts/video_source.py --search "spaced repetition" --channel "justin sung"
    py scripts/video_source.py --search procrastination --phrase "dopamine" --k 20

One video: looks on this PC first (the youtube-digest working copy in the Downloads folder
next to this repo), then falls back to the public GitHub copy, so it also works from a
phone or cloud session. --search needs the library on disk (this PC, or a one-time clone;
the error says how). Stdlib only. (Same tool as video_source.py in the valuation-agent repo.)
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple

_DOWNLOADS = Path(__file__).resolve().parents[2]  # scripts/ -> repo -> the folder holding both repos
LOCAL_ARCHIVE = Path(os.environ.get(
    "YTDIGEST_ARCHIVE", _DOWNLOADS / "Youtube Scraper" / "data" / "archive"))
RAW_ARCHIVE = "https://raw.githubusercontent.com/projectbetterclass/youtube-digest/main/data/archive/"

_ID = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")
_BARE_ID = re.compile(r"[A-Za-z0-9_-]{11}")
_URL = re.compile(r"<(https?://[^>]+)>")


def video_id(ref: str) -> str:
    """The 11-character YouTube id from a URL or a bare id."""
    ref = ref.strip()
    if _BARE_ID.fullmatch(ref):
        return ref
    m = _ID.search(ref)
    if not m:
        raise ValueError(f"not a YouTube URL or video id: {ref!r}")
    return m.group(1)


def _fetch_github(rel: str) -> Optional[str]:
    try:
        with urllib.request.urlopen(RAW_ARCHIVE + rel, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def _read(rel: str, archive: Path, fetch: Callable[[str], Optional[str]]) -> Tuple[Optional[str], str]:
    local = archive / rel
    if local.is_file():
        return local.read_text(encoding="utf-8"), "this PC"
    text = fetch(rel)
    return text, ("GitHub" if text is not None else "")


def _body_after_url(text: str) -> str:
    """Drop the '# title' / '<url>' header (and visuals.md's italic note)."""
    m = _URL.search(text)
    body = text[m.end():] if m else text
    body = body.strip()
    if body.startswith("_") and "\n" in body:  # visuals.md: "_Slides, charts ... omitted._"
        first, rest = body.split("\n", 1)
        if first.rstrip().endswith("_"):
            body = rest.strip()
    return body


@dataclass
class VideoSource:
    video_id: str
    url: str
    title: str
    transcript: Optional[str]  # body only, None if not archived
    visuals: Optional[str]     # body only, None if no screen capture for this video
    where: str                 # "this PC" / "GitHub"


def load(ref: str, archive: Optional[Path] = None,
         fetch: Optional[Callable[[str], Optional[str]]] = None) -> VideoSource:
    """Load one video's transcript + on-screen visuals from the library."""
    vid = video_id(ref)
    archive = LOCAL_ARCHIVE if archive is None else archive
    fetch = _fetch_github if fetch is None else fetch
    transcript, w1 = _read(f"{vid}/transcript.md", archive, fetch)
    visuals, w2 = _read(f"{vid}/visuals.md", archive, fetch)
    if transcript is None and visuals is None:
        raise LookupError(f"video {vid} is not in the youtube-digest library "
                          "(not a watched channel, or not collected yet)")
    head = transcript or visuals
    title = head.split("\n", 1)[0].lstrip("# ").strip()
    title = re.sub(r"^On-screen visuals\s*[—-]\s*", "", title)
    url_m = _URL.search(head)
    return VideoSource(
        video_id=vid,
        url=url_m.group(1) if url_m else f"https://www.youtube.com/watch?v={vid}",
        title=title,
        transcript=_body_after_url(transcript) if transcript else None,
        visuals=_body_after_url(visuals) if visuals else None,
        where=w1 or w2,
    )


def render(src: VideoSource) -> str:
    """One markdown document: on-screen numbers first (short, exact), then the words."""
    out = [f"# {src.title}", "", f"<{src.url}>  (video `{src.video_id}`, from the youtube-digest library on {src.where})", ""]
    out.append("## On-screen charts and slides (time in video)")
    out.append("")
    if src.visuals:
        out.append("_Read off the screen by Claude vision: may contain OCR errors; check a "
                   "number against the video before relying on it._")
        out.append("")
        out.append(src.visuals)
    else:
        out.append("_None captured for this video: its channel isn't opted in to screen "
                   "capture, or the frames haven't been read yet. Only the transcript below._")
    out.append("")
    out.append("## Transcript (what is said)")
    out.append("")
    if src.transcript:
        out.append("_YouTube captions: may lack punctuation, names/jargon are sometimes "
                   "misheard, no speaker labels._")
        out.append("")
        out.append(src.transcript)
    else:
        out.append("_No transcript archived for this video._")
    return "\n".join(out).rstrip() + "\n"


# Title may itself contain [brackets] ("... [40% of His Portfolio]"): lazy up to "](http".
_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*\[(.+?)\]\((https?://[^)]+)\)")


def _row(line: str) -> Optional[Tuple[str, str, str, str]]:
    """(date, channel, title, url) of one INDEX.md table row; titles there escape '|' as '\\|'."""
    m = _ROW.match(line)
    if not m:
        return None
    date, channel, title, url = m.groups()
    return date, channel, title.replace("\\|", "|"), url


def find(query: str, index_text: Optional[str] = None, limit: int = 10) -> List[Tuple[str, str, str, str]]:
    """(date, channel, title, url) rows of the library INDEX whose channel+title contain every word."""
    if index_text is None:
        index_text, _ = _read("INDEX.md", LOCAL_ARCHIVE, _fetch_github)
        index_text = index_text or ""
    words = [w for w in re.findall(r"\w+", query.lower()) if w]
    hits = []
    for line in index_text.splitlines():
        row = _row(line)
        if not row:
            continue
        date, channel, title, url = row
        hay = re.findall(r"\w+", f"{channel} {title}".lower())
        # each query word must START a word ("agi" matches "AGI", not "tragic")
        if words and all(any(h.startswith(w) for h in hay) for w in words):
            hits.append((date, channel, title, url))
            if len(hits) >= limit:
                break
    return hits


# ── Full-text search ──────────────────────────────────────────────────────────
# Searches what is SAID (transcript.md), what is SHOWN (visuals.md) and the title of every
# library video. Needs the library on disk (a straight scan of ~180 MB takes seconds);
# the public GitHub copy is too many files to search one by one.

CLONE_HINT = (
    "Full-text search needs the youtube-digest library on disk, and it isn't at {path}.\n"
    "On a phone/cloud session, fetch it once (~100 MB download) next to this repo:\n"
    '    git clone --depth 1 https://github.com/projectbetterclass/youtube-digest "{clone_to}"\n'
    "or point YTDIGEST_ARCHIVE at an existing copy's data/archive folder."
)
# Phrases: "double quotes" (bash) or 'single quotes' (PowerShell 5.1 strips inner double
# quotes); --phrase works in any shell. A single-quoted span must start with a letter and
# not end in "s'" so apostrophes ('24, 'cause, investors') aren't mistaken for quotes.
_PHRASE = re.compile(r'"([^"]+)"|(?<![\w\'])\'([A-Za-z][^\']*?[^\'\ss])\'(?![\w\'])')
# Tokens, keeping finance compounds whole: P/E, R&D, S&P, D/E, $1, 10-K, don't,
# 1,000, 2.5%, BRK.B. A trailing * asks for prefix matching ("repetit*").
_TOKEN = re.compile(r"\$?\d{1,3}(?:,\d{3})+(?:\.\d+)?%?|\$?\w+(?:[&/.'’-]\w+)*%?\*?")
# Dropped from a query when it has other words: they occur in nearly every video and would
# otherwise decide the ranking and the excerpt ("how to stop procrastinating").
_STOP = frozenset(
    "a an and are as at be been but by can could did do does for from had has have how i if in "
    "into is it its just me my no not of on or our should so than that the their them then there "
    "these they this to was we were what when where which who why will with would you your".split())
# Endings that mark an inflected word: matched by stem, so "procrastinating" also finds
# "procrastination" and "investing" finds "investor". Uninflected words (intel, meta,
# apple) match whole words only, so they never hit "intelligence" or "metaverse".
_STEM_SUFFIXES = ("ations", "ation", "ings", "ing", "ions", "ion", "ities", "ity", "ments",
                  "ment", "ies", "ied", "ers", "er", "ed")
_NOT_PLURAL = frozenset("news series means species physics economics ethics politics gas yes".split())
_COMMON_DF = 0.30   # a term in >30% of videos is "common": missing it barely matters


class ChannelNotFound(LookupError):
    """--channel matched none of the library's channels (the message lists them)."""


@dataclass
class SearchHit:
    video_id: str
    title: str
    channel: str
    date: str
    url: str
    score: float      # BM25 relevance (higher = topic more central to the video)
    distinct: int     # how many of the query's terms/phrases the video contains
    terms: int        # how many terms/phrases were searched (after dropping stopwords)
    in_charts: bool   # some match is in the on-screen chart readings, not just speech
    excerpt: str      # the passage that best covers the query's terms


def _query_terms(query: str, phrases: Optional[List[str]] = None) -> List[str]:
    """Phrases kept whole; a single letter/digit glued to the word before it ("vitamin d",
    "gen z", "plan b"); stopwords dropped unless nothing else is left."""
    found = [" ".join(p.lower().split()) for p in (phrases or []) if p.strip()]

    def grab(m):
        found.append(" ".join((m.group(1) or m.group(2)).lower().split()))
        return " , "  # a separator, so the words either side don't glue together

    rest = _PHRASE.sub(grab, query)
    words: List[str] = []
    for m in re.finditer(_TOKEN.pattern + r"|,", rest):
        w = m.group(0).lower()
        if w == ",":
            words.append(",")
        elif len(w) == 1 and w.isalnum() and words and words[-1] not in (",",) \
                and words[-1] not in _STOP and " " not in words[-1]:
            words[-1] = words[-1] + " " + w      # implicit phrase: "vitamin d"
        elif len(w) > 1 or w.endswith("*"):
            words.append(w)
    words = [w for w in words if w != "," and w.rstrip("*")]
    content = [w for w in words if w not in _STOP]
    if content or found:
        words = content
    seen, out = set(), []
    for t in found + words:
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _is_word(c: str) -> bool:
    return c.isalnum() or c == "_"


def _ends_word(low: str, j: int, plural: bool) -> bool:
    """True if a match ending at j ends the word (optionally allowing s / es / 's)."""
    if j >= len(low) or not _is_word(low[j]):
        return True
    if not plural:
        return False
    for suf in ("s", "es", "'s", "’s"):
        k = j + len(suf)
        if low.startswith(suf, j) and (k >= len(low) or not _is_word(low[k])):
            return True
    return False


def _word_rule(term: str) -> Tuple[str, str]:
    """(needle, mode) for one query word: mode 'prefix' (stem/explicit *) or 'whole'."""
    if term.endswith("*"):
        return term.rstrip("*"), "prefix"
    base = term
    if len(term) >= 4 and term.endswith("s") and not term.endswith(("ss", "is", "us")) \
            and term not in _NOT_PLURAL:
        base = term[:-1]                       # stocks -> stock, etfs -> etf
    for suf in _STEM_SUFFIXES:
        if base.endswith(suf) and len(base) - len(suf) >= 5:
            return base[: -len(suf)], "prefix"   # procrastinating -> procrastinat*
    return base, "whole"


def _finder(term: str):
    """positions(low_text) -> match offsets for one query term.

    Every match must start a word ("ai" never hits "said"). Words match whole (plus s/es/'s)
    unless inflected or written with a trailing * (see _word_rule). Phrases and hyphenated
    words allow any spacing or hyphen between their parts ("dollar-cost" finds "dollar cost").
    The pattern starts with a literal (so the regex engine's fast literal scan applies) and
    carries the word-END rule itself; only the word-START check runs in Python, per match.
    """
    parts = [p for p in re.split(r"[\s-]+", term) if p]
    rules = [_word_rule(p) for p in parts]
    last_needle, last_mode = rules[-1]
    body = r"[\s-]+".join([re.escape(p) for p in parts[:-1]] + [re.escape(last_needle)])
    end = "" if last_mode == "prefix" else r"(?:s|es|'s|’s)?(?!\w)"
    rx = re.compile(body + end)
    first = parts[0] if len(parts) > 1 else last_needle

    def positions(low: str) -> List[int]:
        if first not in low:  # C-speed skip for the many videos without the term
            return []
        return [m.start() for m in rx.finditer(low)
                if m.start() == 0 or not _is_word(low[m.start() - 1])]
    return positions


def _norm(s: str) -> str:
    return re.sub(r"\W+", "", s.lower())


def _index_meta(archive: Path) -> dict:
    """video_id -> (date, channel, title, url) from the library's INDEX.md."""
    meta = {}
    p = archive / "INDEX.md"
    if p.is_file():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            row = _row(line)
            if row:
                date, channel, title, url = row
                try:
                    meta[video_id(url)] = (date, channel, title, url)
                except ValueError:
                    pass
    return meta


def _excerpt(text: str, low: str, hits: List[Tuple[int, int, float]], width: int = 300) -> str:
    """The ~2*width window that best covers the query: each DISTINCT term counts its idf,
    repeats add only a little (0.1 * idf * log(count)), so a passage with several of the query's
    terms beats a run of one repeated word. hits = (position, term_index, idf). O(n*T)."""
    if not hits:
        return " ".join(text[: 2 * width].split())
    hits.sort()
    counts: dict = {}
    best, j = (-1.0, 0, 0), 0

    def score() -> float:
        # distinct terms dominate; repeats only break ties (a run of one word never wins
        # over a passage that has more of the query in it)
        return sum(w * (1 + 0.1 * math.log(c)) for (c, w) in counts.values())

    for i, (p, t, w) in enumerate(hits):
        c = counts.get(t, (0, w))[0]
        counts[t] = (c + 1, w)
        while hits[i][0] - hits[j][0] > 2 * width:
            pj, tj, wj = hits[j]
            cj = counts[tj][0] - 1
            if cj:
                counts[tj] = (cj, wj)
            else:
                del counts[tj]
            j += 1
        s = score()
        if s > best[0]:
            best = (s, j, i)
    first, last = hits[best[1]][0], hits[best[2]][0]
    pad = max(0, (2 * width - (last - first)) // 2)
    lo = max(0, first - pad)
    hi = min(len(low), max(last + 60, lo + 2 * width))  # always include the last match itself
    src = text if len(text) == len(low) else low  # Unicode case-folding can shift offsets
    snippet = " ".join(src[lo:hi].split())
    return ("… " if lo else "") + snippet + (" …" if hi < len(low) else "")


_PLACEHOLDER = re.compile(r"^_[^_\n].*_\s*$", re.M)  # whole-line italic notes, e.g.
# "_No informative on-screen visuals were found in this video._" and
# "_No transcript/captions were available for this video._"


_VISUALS_LINK = re.compile(r"\[visuals\]\(([A-Za-z0-9_-]{11})/visuals\.md\)")


def _visuals_ids(archive: Path) -> Optional[Tuple[set, float]]:
    """(videos known to have a visuals.md, when the visuals ledger was saved). Only a few
    hundred of ~7,600 videos have one, so this lets search skip ~7,000 doomed open() calls.
    Known = the ledger (data/visuals_state.json) plus INDEX.md's [visuals] links. The ledger
    is saved once per reading run, so a run in progress has newer files it doesn't list
    yet: search also opens visuals.md in any video folder changed since the ledger's save
    time (a new file moves its folder's mtime). None = no ledger next to the archive: then
    every video's file is tried (INDEX.md alone lags behind, so it is never trusted alone)."""
    import json

    ledger_path = archive.parent / "visuals_state.json"
    try:
        saved = ledger_path.stat().st_mtime
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ids = {v for v, r in ledger.get("visuals", {}).items() if not r.get("error")}
    except (OSError, ValueError, AttributeError):
        return None
    try:
        ids.update(_VISUALS_LINK.findall((archive / "INDEX.md").read_text(encoding="utf-8", errors="replace")))
    except OSError:
        pass
    return ids, saved


def _read_body(path) -> str:
    """Spoken/shown content only: no '# title' / '<url>' header, no italic placeholder notes.
    Opens directly (a missing file just reads as empty): on Windows a separate exists/is_file
    check per file costs more than the read itself across ~7,600 videos."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            body = _body_after_url(fh.read())
    except (FileNotFoundError, NotADirectoryError):
        return ""
    if body.startswith("_") or "\n_" in body:  # only then can a placeholder line exist
        body = _PLACEHOLDER.sub("", body)
    return body.strip()


def search(query: str, k: int = 10, channel: Optional[str] = None,
           archive: Optional[Path] = None, phrases: Optional[List[str]] = None) -> List[SearchHit]:
    """Top-k library videos for a topic.

    Ranked first by how many of the query's informative terms a video contains (a term in
    more than 30% of videos, like "stop" or "company", doesn't count toward this), then by
    BM25: term frequency with diminishing returns, normalised for length, so a video *about*
    the topic beats a 3-hour podcast that mentions it once. Searches the title plus what is
    said and shown; file headers, URLs and placeholder notes are excluded. `channel` keeps
    channels whose name contains it, ignoring case/spaces/punctuation ("ticker symbol you"
    matches "Ticker Symbol: YOU"); a channel that matches nothing raises ChannelNotFound.
    """
    archive = LOCAL_ARCHIVE if archive is None else Path(archive)
    if not archive.is_dir():
        clone_to = (archive.parent.parent if archive.name == "archive" else archive)
        raise FileNotFoundError(CLONE_HINT.format(path=archive, clone_to=clone_to))
    k = max(1, int(k))
    terms = _query_terms(query, phrases)
    if not terms:
        return []
    finders = [_finder(t) for t in terms]
    meta = _index_meta(archive)
    want = _norm(channel) if channel is not None and channel.strip() else ""
    if channel is not None and channel.strip() and not want:
        raise ChannelNotFound(f"{channel!r} has no letters or digits to match a channel name.")
    if want:
        names = sorted({m[1] for m in meta.values() if m[1]})
        if not names:
            raise ChannelNotFound("INDEX.md is missing or empty, so channels are unknown; "
                                  "run the search without --channel.")
        if not any(want in _norm(n) for n in names):
            raise ChannelNotFound(f"No channel matches {channel!r}. Channels: " + ", ".join(names))

    docs = []  # (vid, n_words, counts or None, chart_counts or None)
    with os.scandir(archive) as entries:  # on Windows, is_dir()/stat() here need no extra syscall
        video_dirs = [e for e in entries if e.is_dir()]
    known = _visuals_ids(archive)
    for entry in video_dirs:
        vid, dpath = entry.name, entry.path
        date, ch, title, _ = meta.get(vid, ("", "", "", ""))
        if want and want not in _norm(ch):
            continue
        t_low = _read_body(os.path.join(dpath, "transcript.md")).lower()
        try_visuals = (known is None or vid in known[0]
                       or entry.stat().st_mtime >= known[1] - 2)  # changed since the ledger save
        v_low = _read_body(os.path.join(dpath, "visuals.md")).lower() if try_visuals else ""
        if not (t_low or v_low):
            continue
        low = title.lower() + "\n" + t_low + "\n" + v_low
        n_words = len(low) // 6 + 1
        counts = [len(f(low)) for f in finders]
        if not any(counts):
            docs.append((vid, n_words, None, None))  # still counts toward the average length
            continue
        chart = [len(f(v_low)) if (v_low and c) else 0 for f, c in zip(finders, counts)]
        docs.append((vid, n_words, counts, chart))

    n_docs = len(docs) or 1
    avgdl = sum(x[1] for x in docs) / n_docs
    df = [sum(1 for x in docs if x[2] and x[2][i]) for i in range(len(terms))]
    idf = [math.log(1 + (n_docs - f + 0.5) / (f + 0.5)) for f in df]
    informative = [i for i in range(len(terms)) if df[i] <= _COMMON_DF * n_docs] or list(range(len(terms)))
    k1, b = 1.2, 0.75
    scored = []
    for vid, dl, counts, chart in docs:
        if not counts:
            continue
        bm25 = sum(idf[i] * c * (k1 + 1) / (c + k1 * (1 - b + b * dl / avgdl))
                   for i, c in enumerate(counts) if c)
        covered = sum(1 for i in informative if counts[i])
        scored.append((covered, bm25, vid, counts, chart))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)

    hits = []
    for covered, bm25, vid, counts, chart in scored[:k]:
        d = archive / vid
        date, ch, title, url = meta.get(vid, ("", "", "", f"https://www.youtube.com/watch?v={vid}"))
        body = "\n".join(x for x in (_read_body(d / "transcript.md"), _read_body(d / "visuals.md")) if x)
        low = body.lower()
        positions = [(p, i, idf[i]) for i, f in enumerate(finders) for p in f(low)]
        if not title:
            head = d / "transcript.md"
            title = (head.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0].lstrip("# ").strip()
                     if head.is_file() else vid)
        hits.append(SearchHit(vid, title, ch, date, url, round(bm25, 2),
                              sum(1 for c in counts if c), len(terms), any(chart),
                              _excerpt(body, low, positions)))
    return hits


def _positive_int(v: str) -> int:
    n = int(v)
    if n < 1:
        raise argparse.ArgumentTypeError("must be 1 or more")
    return n


def main(argv=None) -> int:
    try:  # Windows consoles default to cp1252; titles carry emoji and em-dashes
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="A video's transcript + on-screen charts from the youtube-digest library.")
    ap.add_argument("video", nargs="?", help="YouTube URL or 11-character video id")
    ap.add_argument("--find", metavar="WORDS", help="look a video up by channel/title words instead")
    ap.add_argument("--search", metavar="TOPIC",
                    help="search what is said and shown in every video. Words match whole "
                         "(plus plurals; inflected words like 'investing' match by stem), "
                         "word* matches a prefix, exact phrases go in quotes: \"free cash flow\" "
                         "(bash) or 'free cash flow' (PowerShell) -- or use --phrase")
    ap.add_argument("--phrase", action="append", default=[],
                    help="with --search: an exact phrase to require (repeatable; works in any shell)")
    ap.add_argument("--channel", help="with --search: only channels whose name contains this")
    ap.add_argument("--k", type=_positive_int, default=10, help="with --search: how many videos to return")
    ap.add_argument("--out", help="write the markdown here instead of printing it")
    args = ap.parse_args(argv)

    if args.phrase and not args.search:
        args.search = " "
    if args.search:
        if not _query_terms(args.search, args.phrase):
            print(f"{args.search!r} has no searchable words (single letters and punctuation are ignored).")
            return 1
        try:
            hits = search(args.search, k=args.k, channel=args.channel, phrases=args.phrase)
        except (FileNotFoundError, ChannelNotFound) as exc:
            print(exc)
            return 1
        if not hits:
            print(f"No library video mentions {args.search!r}"
                  + (f" in channels matching {args.channel!r}." if args.channel else "."))
            return 1
        print(f"Top {len(hits)} videos for {args.search!r}"
              + (f" (channels matching {args.channel!r})" if args.channel else "") + ":\n")
        for i, h in enumerate(hits, 1):
            where = "speech + charts" if h.in_charts else "speech"
            print(f"{i}. [{h.channel or '?'}] {h.title}" + (f"  ({h.date})" if h.date not in ("", "—") else ""))
            print(f"   {h.url}  | {h.distinct}/{h.terms} terms, relevance {h.score}, in {where}")
            print(f"   {h.excerpt}\n")
        print("Open one with: py scripts/video_source.py <url>")
        return 0
    if args.find:
        hits = find(args.find)
        if not hits:
            print(f"No library video matches {args.find!r}.")
            return 1
        for date, channel, title, url in hits:
            print(f"{date}  {channel}  |  {title}\n    {url}")
        return 0
    if not args.video:
        ap.error("give a YouTube URL / video id, or --find WORDS")
    try:
        src = load(args.video)
    except (ValueError, LookupError) as exc:
        print(exc)
        return 1
    text = render(src)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8")
        n = src.visuals.count("\n## ") + src.visuals.startswith("## ") if src.visuals else 0
        print(f"Wrote {args.out}: {src.title} ({n} on-screen visuals, transcript "
              f"{'yes' if src.transcript else 'no'}; from {src.where})")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
