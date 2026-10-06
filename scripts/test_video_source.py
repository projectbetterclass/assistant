"""video_source pulls a video's transcript + on-screen visuals from the youtube-digest library.

No network: a temp folder stands in for the PC copy and a stub stands in for GitHub.

    py -m unittest discover -s scripts -v
"""
from __future__ import annotations

import os
import tempfile
import time
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



def _search_archive():
    index = ("| date | channel | title |\n|---|---|---|\n"
             "| 2026-01-01 | Justin Sung | [Spaced Repetition Done Right](https://www.youtube.com/watch?v=aaaaaaaaaaa) | — |\n"
             "| 2026-01-02 | HealthyGamerGG | [A Long Podcast](https://www.youtube.com/watch?v=bbbbbbbbbbb) | — |\n"
             "| 2026-01-03 | Ticker Symbol: YOU | [Nvidia Chart](https://www.youtube.com/watch?v=ccccccccccc) | — |\n")
    focused = "spaced repetition is the core. use spaced repetition daily. retrieval matters."
    long_pod = ("we talk about life and many things. " * 400) + "spaced repetition came up once."
    return _archive({
        "INDEX.md": index,
        "aaaaaaaaaaa/transcript.md": "# Spaced Repetition Done Right\n\n<https://youtu.be/aaaaaaaaaaa>\n\n" + focused,
        "bbbbbbbbbbb/transcript.md": "# A Long Podcast\n\n<https://youtu.be/bbbbbbbbbbb>\n\n" + long_pod,
        "ccccccccccc/transcript.md": "# Nvidia Chart\n\n<https://youtu.be/ccccccccccc>\n\nhe said again and again",
        "ccccccccccc/visuals.md": "# On-screen visuals — Nvidia Chart\n\n<https://youtu.be/ccccccccccc>\n\n"
                                  "## 1. [01:00] Data-center revenue\n\nAI revenue $115B",
    })


class TestSearch(unittest.TestCase):
    def test_focused_video_outranks_a_passing_mention(self):
        hits = V.search("spaced repetition", archive=_search_archive())
        self.assertEqual([h.video_id for h in hits], ["aaaaaaaaaaa", "bbbbbbbbbbb"])
        self.assertEqual((hits[0].channel, hits[0].distinct, hits[0].terms), ("Justin Sung", 2, 2))
        self.assertIn("spaced repetition", hits[0].excerpt.lower())

    def test_more_terms_matched_ranks_first(self):
        hits = V.search("spaced repetition retrieval", archive=_search_archive())
        self.assertEqual(hits[0].video_id, "aaaaaaaaaaa")
        self.assertEqual(hits[0].distinct, 3)

    def test_word_boundaries_and_prefixes(self):
        arch = _search_archive()
        # "ai" must not match "said"/"again"; it does match the chart text "AI revenue"
        hits = V.search("ai", archive=arch)
        self.assertEqual([h.video_id for h in hits], ["ccccccccccc"])
        self.assertTrue(hits[0].in_charts)
        self.assertEqual([h.video_id for h in V.search("repetit*", archive=arch)][:1], ["aaaaaaaaaaa"])
        self.assertEqual(V.search("repetit", archive=arch), [])  # no * -> whole words only

    def test_quoted_phrase_and_channel_filter(self):
        arch = _search_archive()
        self.assertEqual([h.video_id for h in V.search('"core spaced"', archive=arch)], [])
        self.assertEqual([h.video_id for h in V.search('"the core"', archive=arch)], ["aaaaaaaaaaa"])
        self.assertEqual([h.video_id for h in V.search("spaced", channel="healthy", archive=arch)],
                         ["bbbbbbbbbbb"])

    def test_missing_library_explains_how_to_get_it(self):
        with self.assertRaises(FileNotFoundError) as ctx:
            V.search("x", archive=Path(tempfile.mkdtemp()) / "nope" / "data" / "archive")
        self.assertIn("git clone --depth 1", str(ctx.exception))

    def test_empty_query(self):
        self.assertEqual(V.search("  a  ", archive=_search_archive()), [])


class TestSearchReviewFixes(unittest.TestCase):
    """One test per defect the 2026-10-06 adversarial review confirmed."""

    def _arch(self):
        index = ("| date | channel | title |\n|---|---|---|\n"
                 "| 2026-01-01 | Aswath Damodaran | [Valuing R&D [Part 1]](https://www.youtube.com/watch?v=aaaaaaaaaaa) | — |\n"
                 "| 2026-01-02 | Ticker Symbol: YOU | [Nvidia at $1 trillion](https://www.youtube.com/watch?v=bbbbbbbbbbb) | — |\n"
                 "| 2026-01-03 | HealthyGamerGG | [Procrastination](https://www.youtube.com/watch?v=ccccccccccc) | — |\n"
                 "| 2026-01-04 | HealthyGamerGG | [Hero motivation](https://www.youtube.com/watch?v=ddddddddddd) | — |\n")
        hdr = lambda t, v: f"# {t}\n\n<https://www.youtube.com/watch?v={v}>\n\n"
        vis_note = ("_Slides, charts, and diagrams read from the video by Claude vision. Text is "
                    "transcribed from the screen and may contain OCR errors; not on-screen visuals "
                    "are omitted._\n\n")
        return _archive({
            "INDEX.md": index,
            "aaaaaaaaaaa/transcript.md": hdr("Valuing R&D", "aaaaaaaaaaa") +
                "capitalize r&d and look at the p/e and the s&p 500 every quarter",
            "bbbbbbbbbbb/transcript.md": hdr("Nvidia", "bbbbbbbbbbb") + "it is worth $1 trillion today, every ev maker wants chips",
            "bbbbbbbbbbb/visuals.md": "# On-screen visuals — Nvidia\n\n<https://www.youtube.com/watch?v=bbbbbbbbbbb>\n\n"
                + vis_note + "## 1. [00:10] Market cap\n\n$1 trillion",
            "ccccccccccc/transcript.md": hdr("Procrastination", "ccccccccccc") +
                ("why you procrastinate and how procrastinating works. " * 20),
            "ddddddddddd/transcript.md": hdr("Hero", "ddddddddddd") +
                ("how to be a hero. stop waiting. " * 3) + "stop procrastinating.",
            # "stop" is a common word in the real library (~half of all videos): mirror that
            **{f"{c * 11}/transcript.md": hdr("Filler", c * 11) + "they had to stop and go on"
               for c in "efghij"},
        })

    def test_finance_compounds_are_searchable(self):
        arch = self._arch()
        for q in ("R&D", "P/E", "S&P 500"):
            self.assertEqual([h.video_id for h in V.search(q, archive=arch)][:1], ["aaaaaaaaaaa"], q)

    def test_phrase_starting_with_dollar_matches(self):
        hits = V.search('"$1 trillion"', archive=self._arch())
        self.assertEqual([h.video_id for h in hits], ["bbbbbbbbbbb"])
        self.assertTrue(hits[0].in_charts)

    def test_headers_urls_and_vision_note_are_not_content(self):
        arch = self._arch()
        for q in ("youtube", "watch", "https", "claude vision", "slides charts"):
            self.assertEqual(V.search(q, archive=arch), [], q)

    def test_bracketed_titles_keep_their_channel(self):
        hits = V.search("capitalize", channel="aswath", archive=self._arch())
        self.assertEqual([(h.video_id, h.channel) for h in hits], [("aaaaaaaaaaa", "Aswath Damodaran")])
        self.assertEqual(V._index_meta(self._arch())["aaaaaaaaaaa"][2], "Valuing R&D [Part 1]")

    def test_channel_filter_is_forgiving_and_honest(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("trillion", channel="ticker symbol you", archive=arch)],
                         ["bbbbbbbbbbb"])
        self.assertEqual(len(V.search("procrastinating", channel="Healthy Gamer", archive=arch)), 2)
        with self.assertRaises(V.ChannelNotFound) as ctx:
            V.search("trillion", channel="no such channel", archive=arch)
        self.assertIn("Ticker Symbol: YOU", str(ctx.exception))

    def test_stopwords_dont_decide_the_ranking(self):
        # "how/to" are dropped; the focused procrastination video beats the clip that merely
        # contains every word of the question once.
        hits = V.search("how to stop procrastinating", archive=self._arch())
        self.assertEqual(hits[0].video_id, "ccccccccccc")
        self.assertEqual(hits[0].terms, 2)

    def test_short_terms_are_whole_words(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("ev", archive=arch)], ["bbbbbbbbbbb"])  # not "every"

    def test_single_quoted_phrase_for_powershell(self):
        self.assertEqual(V._query_terms("'free cash flow' dcf"), ["free cash flow", "dcf"])
        self.assertEqual(V._query_terms("don't panic"), ["don't", "panic"])

    def test_k_below_one_still_returns_the_best_hit(self):
        self.assertEqual(len(V.search("trillion", k=0, archive=self._arch())), 1)

    def test_excerpt_prefers_the_rare_term(self):
        low = ("the " * 200) + "valuation " + ("the " * 200)
        ex = V._excerpt(low, low, [(i, 0, 0.01) for i in range(0, 800, 4)] + [(low.index("valuation"), 1, 5.0)])
        self.assertIn("valuation", ex)

    def test_question_with_no_words_left(self):
        self.assertEqual(V._query_terms("? ! a"), [])


class TestSearchRound2(unittest.TestCase):
    """Defects found when the fixes were re-verified (2026-10-06, second review)."""

    def _arch(self):
        index = ("| date | channel | title |\n|---|---|---|\n"
                 "| 2026-01-01 | Ticker Symbol: YOU | [Intel turnaround](https://www.youtube.com/watch?v=aaaaaaaaaaa) | — |\n"
                 "| 2026-01-02 | Ticker Symbol: YOU | [AI boom](https://www.youtube.com/watch?v=bbbbbbbbbbb) | — |\n"
                 "| 2026-01-03 | BWB - Business With Brian | [ETF basics](https://www.youtube.com/watch?v=ccccccccccc) | — |\n"
                 "| 2026-01-04 | HealthyGamerGG | [How To Stop Procrastinating](https://www.youtube.com/watch?v=ddddddddddd) | — |\n"
                 "| 2026-01-05 | Ticker Symbol: YOU | [No charts here](https://www.youtube.com/watch?v=eeeeeeeeeee) | — |\n")
        hdr = lambda t, v: f"# {t}\n\n<https://www.youtube.com/watch?v={v}>\n\n"
        note = ("_Slides, charts, and diagrams read from the video by Claude vision. Text is "
                "transcribed from the screen and may contain OCR errors; not on-screen visuals "
                "are omitted._\n\n")
        return _archive({
            "INDEX.md": index,
            "aaaaaaaaaaa/transcript.md": hdr("Intel", "aaaaaaaaaaa") + "intel is cutting costs. intel's foundry. meta and intel.",
            "bbbbbbbbbbb/transcript.md": hdr("AI", "bbbbbbbbbbb") +
                "artificial intelligence and the metaverse. dollar cost averaging works. vitamin d too.",
            "ccccccccccc/transcript.md": hdr("ETF", "ccccccccccc") + "two etfs and three ipos. buy 1,000 shares at 2.5% yield.",
            "ddddddddddd/transcript.md": hdr("How To Stop Procrastinating", "ddddddddddd") + "we talk about focus and habits.",
            "eeeeeeeeeee/transcript.md": hdr("No charts", "eeeeeeeeeee") + "_No transcript/captions were available for this video._",
            "eeeeeeeeeee/visuals.md": "# On-screen visuals — No charts\n\n<https://www.youtube.com/watch?v=eeeeeeeeeee>\n\n"
                + note + "_No informative on-screen visuals were found in this video._\n",
        })

    def test_company_names_match_whole_words(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("intel", archive=arch)], ["aaaaaaaaaaa"])  # not "intelligence"
        self.assertEqual([h.video_id for h in V.search("meta", archive=arch)], ["aaaaaaaaaaa"])   # not "metaverse"

    def test_plural_acronyms_and_numbers(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("ETF", archive=arch)], ["ccccccccccc"])
        self.assertEqual([h.video_id for h in V.search("IPOs", archive=arch)], ["ccccccccccc"])
        self.assertEqual([h.video_id for h in V.search("1,000", archive=arch)], ["ccccccccccc"])
        self.assertEqual([h.video_id for h in V.search("2.5%", archive=arch)], ["ccccccccccc"])

    def test_hyphenated_and_letter_compounds(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("dollar-cost", archive=arch)], ["bbbbbbbbbbb"])
        self.assertEqual(V._query_terms("vitamin D"), ["vitamin d"])
        self.assertEqual([h.video_id for h in V.search("vitamin D", archive=arch)], ["bbbbbbbbbbb"])

    def test_placeholder_notes_are_not_content(self):
        arch = self._arch()
        for q in ("informative", "captions", "visuals"):
            self.assertEqual(V.search(q, archive=arch), [], q)

    def test_title_counts_as_content(self):
        hits = V.search("procrastinating", archive=self._arch())
        self.assertEqual([h.video_id for h in hits], ["ddddddddddd"])

    def test_informative_terms_rank_first(self):
        # every doc says "and"/"the"-like common words; the doc with BOTH rare terms wins
        arch = self._arch()
        hits = V.search("intel foundry", archive=arch)
        self.assertEqual(hits[0].video_id, "aaaaaaaaaaa")
        self.assertEqual(hits[0].distinct, 2)

    def test_phrase_option_and_apostrophes(self):
        arch = self._arch()
        self.assertEqual([h.video_id for h in V.search("", phrases=["dollar cost averaging"], archive=arch)],
                         ["bbbbbbbbbbb"])
        self.assertEqual(V._query_terms("investors' returns in '24"), ["investors", "returns", "24"])

    def test_punctuation_only_channel_is_an_error(self):
        with self.assertRaises(V.ChannelNotFound):
            V.search("intel", channel="!!!", archive=self._arch())

    def test_excerpt_prefers_a_window_with_more_distinct_terms(self):
        text = ("alpha " * 30) + ("filler " * 120) + "alpha beta gamma" + (" filler" * 120)
        low = text.lower()
        hits = [(i, 0, 1.0) for i in range(0, 180, 6)]  # 30x alpha clustered at the start
        k = low.index("alpha beta gamma")
        hits += [(k, 0, 1.0), (k + 6, 1, 1.0), (k + 11, 2, 1.0)]
        self.assertIn("alpha beta gamma", V._excerpt(text, low, hits, width=100))


class TestVisualsShortcut(unittest.TestCase):
    def test_ledger_decides_which_visuals_to_read(self):
        root = Path(tempfile.mkdtemp())
        arch = root / "data" / "archive"
        for vid, chart in (("aaaaaaaaaaa", "margin 70%"), ("bbbbbbbbbbb", "margin 40%")):
            (arch / vid).mkdir(parents=True)
            (arch / vid / "transcript.md").write_text(f"# t\n\n<https://youtu.be/{vid}>\n\nwe talk", encoding="utf-8")
            (arch / vid / "visuals.md").write_text(f"# v\n\n<https://youtu.be/{vid}>\n\n## 1. [00:01] x\n\n{chart}", encoding="utf-8")
        # no ledger: every visuals.md is read
        self.assertEqual(sorted(h.video_id for h in V.search("margin", archive=arch)), ["aaaaaaaaaaa", "bbbbbbbbbbb"])
        # with a ledger, only videos it lists (without an error) are read ...
        old = time.time() - 3600
        for vid in ("aaaaaaaaaaa", "bbbbbbbbbbb"):
            os.utime(arch / vid, (old, old))  # folders untouched since before the ledger save
        (root / "data" / "visuals_state.json").write_text(
            '{"visuals": {"aaaaaaaaaaa": {"slides": 1}, "bbbbbbbbbbb": {"slides": 0, "error": "x"}}}', encoding="utf-8")
        self.assertEqual([h.video_id for h in V.search("margin", archive=arch)], ["aaaaaaaaaaa"])
        # ... plus any folder changed after it was saved (a reading run still in progress)
        (arch / "ccccccccccc").mkdir()
        (arch / "ccccccccccc" / "visuals.md").write_text(
            "# v\n\n<https://youtu.be/ccccccccccc>\n\n## 1. [00:01] x\n\nmargin 55%", encoding="utf-8")
        self.assertEqual(sorted(h.video_id for h in V.search("margin", archive=arch)), ["aaaaaaaaaaa", "ccccccccccc"])


class TestIndexTitles(unittest.TestCase):
    def test_escaped_pipes_in_titles_are_shown_as_pipes(self):
        index = ("| date | channel | title |\n|---|---|---|\n"
                 "| 2026-01-01 | Justin Sung | [Good at studying \\| STUDY CLINIC](https://www.youtube.com/watch?v=aaaaaaaaaaa) | — |\n")
        self.assertEqual(V.find("clinic", index_text=index)[0][2], "Good at studying | STUDY CLINIC")
        arch = _archive({"INDEX.md": index,
                         "aaaaaaaaaaa/transcript.md": "# t\n\n<https://www.youtube.com/watch?v=aaaaaaaaaaa>\n\nrecall"})
        self.assertEqual(V.search("recall", archive=arch)[0].title, "Good at studying | STUDY CLINIC")


if __name__ == "__main__":
    unittest.main()
