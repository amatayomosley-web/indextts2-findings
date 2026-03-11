#!/usr/bin/env python3
"""Sarcastic Tag experiment — tag changes character, not speed.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: Emotion tags change delivery CHARACTER (how it sounds), not speed. Speed is
controlled by word count (attention budget), not by tag selection.

Method: Same 35-word text generated with [sarcastic] tag and without any tag.
        Compare WPM and listen for character difference.

Results:
    [sarcastic] tag  -> 12.2s, 173 WPM
    No tag           -> 12.3s, 170 WPM

Conclusion: Tag changes character (sarcastic delivery), not speed. 3 WPM difference
is within noise.
"""

# ---- Test definitions (exact texts used in experiments) ----

TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120

TEXT = (
    "your incredible ability to state the obvious with such unearned "
    "confidence is truly a marvel of modern psychology; I am sure everyone "
    "is absolutely fascinated by your profound discovery that water is "
    "actually still wet."
)

VARIANTS = [
    {
        "id": "sarcastic_full",
        "tag": "sarcastic",
        "text": TEXT,
        "note": "Full sarcastic passage with [sarcastic] tag.",
    },
    {
        "id": "sarcastic_notag",
        "tag": "",
        "text": TEXT,
        "note": "Same text, NO tag. Compare character difference.",
    },
]
