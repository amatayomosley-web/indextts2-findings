#!/usr/bin/env python3
"""Punctuation Transparency experiment — A/B test with identical text.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: All punctuation marks produce equivalent delivery. Punctuation is not a pacing
or intonation tool in IndexTTS-2.

Method: Same 30-word text in two versions:
        A) Heavy punctuation (commas, ellipses, exclamation, colon, question mark)
        B) Stripped to bare sentences (minimal punctuation)
        No emotion tag applied.

Results:
    WITH punctuation    -> 10.8s, 166 WPM
    WITHOUT punctuation ->  9.8s, 184 WPM

Additionally, 14 short variants with different punctuation saturation were tested.
All mark types (ellipses, quotes, semicolons, exclamations, questions) produce
equivalent delivery. No mark affects intonation differently from any other.

Conclusion: Punctuation effects are very minor. Not a useful delivery tool.
"""

# ---- Test definitions (exact texts used in experiments) ----

TAG = ""  # No emotion tag
TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120

# A/B test — same content, different punctuation
AB_VARIANTS = [
    {
        "id": "punct_heavy",
        "text": (
            "Does this sound natural? Or, perhaps, a bit robotic... "
            "Wait! I need to know: can you hear the difference between "
            "a comma, a period, and a very dramatic, lingering pause?"
        ),
        "note": "WITH punctuation: commas, ellipses, exclamation, colon, question mark.",
    },
    {
        "id": "punct_stripped",
        "text": (
            "Does this sound natural? Or perhaps a bit robotic. "
            "Wait I need to know can you hear the difference between "
            "a comma a period and a very dramatic lingering pause?"
        ),
        "note": "WITHOUT punctuation: stripped clean. Compare delivery difference.",
    },
]

# Saturation variants — short phrases with different mark types
SATURATION_VARIANTS = [
    {"id": "p01_wait", "text": "But wait.", "note": "Clean baseline."},
    {"id": "p02_wait_ellipses_quotes", "text": 'But... "wait"...?', "note": "Ellipses + quotes + question mark."},
    {"id": "p03_just_go", "text": "Just... go.", "note": "Ellipses."},
    {"id": "p04_now_go", "text": '"Now," go! ...Go? ...Go!', "note": "Quotes + comma + exclamation + ellipses + question."},
    {"id": "p05_wait_triple", "text": "...Wait... Wait! ...Wait.", "note": "Triple wait with ellipses, exclamation, period."},
    {"id": "p06_everything_fine", "text": '"Everything" is "fine"... Fine?', "note": "Quotes + ellipses + question mark."},
    {"id": "p07_stop_wait", "text": 'Stop; wait; listen; "hear"?', "note": "Semicolons + quotes + question."},
    {"id": "p08_path_clear", "text": 'The "path" is "clear"? ...Clear?', "note": "Quotes + question + ellipses + question."},
    {"id": "p09_is_it", "text": "...Is it? Maybe. No.", "note": "Ellipses + question + periods."},
    {"id": "p10_success", "text": '"Success," they say, is "near"!', "note": "Quotes + comma + exclamation."},
    {"id": "p11_wait_stop_look", "text": "Wait, stop, look? Really? Look...", "note": "Commas + questions + ellipses."},
    {"id": "p12_is_it_over", "text": 'Is... "it"... really... over?', "note": "Maximum ellipses saturation + quotes + question."},
    {"id": "p13_yes_no_maybe", "text": '"Yes." No! "Maybe..."', "note": "Quotes + period + exclamation + ellipses."},
    {"id": "p14_sigh_go", "text": "Sigh; go; just... go.", "note": "Semicolons + ellipses + period."},
]
