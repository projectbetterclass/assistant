"""video_source pulls a video's transcript + on-screen visuals from the youtube-digest library.

No network: a temp folder stands in for the PC copy and a stub stands in for GitHub.

    py -m unittest discover -s scripts -v
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import video_source as V

VID = "_ABDiQYrSw0"
TRANSCRIPT = "# AGI Has Arrived\n\n<https://www.youtube.com/watch?v=_ABDiQYrSw0>\n\nagents use 15 to 100x the compute\n"
VISUALS = ("# On-screen visuals — AGI Has Arrived\n\n<https://www.youtube.com/watch?v=_ABDiQYrSw0>\n\n"
           "_Slides, charts, and diagrams read from the video by Claude vision. Text is "
           "transcribed from the screen and may contain OCR errors; not on-screen visuals "
           "are omitted._\n\n## 1. [01:57] Agents chart\n\n700 of 1,200 (58%)\n")


def _archive(files):
    d = Path(tempfile.mkdtemp())
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text, encoding="utf-8")
    return d


def _no_network(rel):
    raise AssertionError(f"should not fetch {rel}")


class TestVideoSource(unittest.TestCase):
    def test_video_id_from_urls_and_bare_ids(self):
        for ref in (VID, f"https://www.youtube.com/watch?v={VID}&t=30s",
                    f"https://youtu.be/{VID}", f"https://www.youtube.com/shorts/{VID}"):
            self.assertEqual(V.video_id(ref), VID)
        with self.assertRaises(ValueError):
            V.video_id("not a video")

    def test_loads_both_files_of_the_same_video_from_this_pc(self):
        arch = _archive({f"{VID}/transcript.md": TRANSCRIPT, f"{VID}/visuals.md": VISUALS})
        src = V.load(f"https://youtu.be/{VID}", archive=arch, fetch=_no_network)
        self.assertEqual((src.video_id, src.title, src.where), (VID, "AGI Has Arrived", "this PC"))
        self.assertTrue(src.transcript.startswith("agents use"))
        self.assertTrue(src.visuals.startswith("## 1. [01:57]"))  # header + note stripped

    def test_falls_back_to_github(self):
        files = {f"{VID}/transcript.md": TRANSCRIPT}
        src = V.load(VID, archive=_archive({}), fetch=files.get)
        self.assertEqual(src.where, "GitHub")
        self.assertIsNone(src.visuals)

    def test_render_puts_visuals_first_and_flags_missing_ones(self):
        arch = _archive({f"{VID}/transcript.md": TRANSCRIPT, f"{VID}/visuals.md": VISUALS})
        text = V.render(V.load(VID, archive=arch, fetch=_no_network))
        self.assertLess(text.index("On-screen charts"), text.index("Transcript (what is said)"))
        self.assertIn("700 of 1,200 (58%)", text)
        only_tx = V.render(V.load(VID, archive=_archive({f"{VID}/transcript.md": TRANSCRIPT}),
                                  fetch=lambda rel: None))
        self.assertIn("None captured for this video", only_tx)

    def test_unknown_video_is_a_clear_error(self):
        with self.assertRaises(LookupError):
            V.load(VID, archive=_archive({}), fetch=lambda rel: None)

    def test_find_matches_channel_and_title_words(self):
        index = ("| date | channel | title |\n|---|---|---|\n"
                 f"| 2026-09-12 | Ticker Symbol: YOU | [AGI Has Arrived. Here's How](https://www.youtube.com/watch?v={VID}) | skim |\n"
                 "| 2026-09-01 | BWB | [Bitcoin ETFs](https://www.youtube.com/watch?v=abcdefghijk) | watch |\n"
                 "| — | Ticker Symbol: YOU | [The Most Tragic IPO](https://www.youtube.com/watch?v=TEimEZVjN9o) | — |\n")
        hits = V.find("ticker agi", index_text=index)
        self.assertEqual([h[3] for h in hits], [f"https://www.youtube.com/watch?v={VID}"])
        self.assertEqual(V.find("nvidia", index_text=index), [])


if __name__ == "__main__":
    unittest.main()
