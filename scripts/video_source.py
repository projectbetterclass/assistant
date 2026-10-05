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

Looks on this PC first (the youtube-digest working copy in the Downloads folder next to
this repo), then falls back to the public GitHub copy, so it also works from a phone or
cloud session. Stdlib only. (Same tool as video_source.py in the valuation-agent repo.)
"""
from __future__ import annotations

import argparse
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


_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)")


def find(query: str, index_text: Optional[str] = None, limit: int = 10) -> List[Tuple[str, str, str, str]]:
    """(date, channel, title, url) rows of the library INDEX whose channel+title contain every word."""
    if index_text is None:
        index_text, _ = _read("INDEX.md", LOCAL_ARCHIVE, _fetch_github)
        index_text = index_text or ""
    words = [w for w in re.findall(r"\w+", query.lower()) if w]
    hits = []
    for line in index_text.splitlines():
        m = _ROW.match(line)
        if not m:
            continue
        date, channel, title, url = m.groups()
        hay = re.findall(r"\w+", f"{channel} {title}".lower())
        # each query word must START a word ("agi" matches "AGI", not "tragic")
        if words and all(any(h.startswith(w) for h in hay) for w in words):
            hits.append((date, channel, title, url))
            if len(hits) >= limit:
                break
    return hits


def main(argv=None) -> int:
    try:  # Windows consoles default to cp1252; titles carry emoji and em-dashes
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description="A video's transcript + on-screen charts from the youtube-digest library.")
    ap.add_argument("video", nargs="?", help="YouTube URL or 11-character video id")
    ap.add_argument("--find", metavar="WORDS", help="look a video up by channel/title words instead")
    ap.add_argument("--out", help="write the markdown here instead of printing it")
    args = ap.parse_args(argv)

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
