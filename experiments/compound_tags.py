#!/usr/bin/env python3
"""Compound Tag Blending experiment — 1 tag vs 3 tags on same text.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: Multiple emotion tags are blended by averaging their 8D vectors element-wise.
The highest alpha value is used. Blended output lands in the middle of individual
tag values.

Method: Same 18-word text generated with single tags ([playful], [awed], [happy])
        and with all three blended ([playful, awed, happy]).

Results:
    [playful]               -> 227 WPM
    [awed]                  -> 226 WPM
    [happy]                 -> 246 WPM
    [playful, awed, happy]  -> 239 WPM

Conclusion: Blend lands in the middle of individual tag values. Stacking does not
degrade quality at 3 tags on short text.

Note on 8D emotion vectors:
    Dimensions: [happy, sad, angry, surprised, scared, warm, neutral, serious]
    Mode 3 control allows direct numeric specification per dimension.
    When multiple tags are provided, vectors are averaged element-wise.
"""

# ---- Test definitions (exact texts used in experiments) ----

TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120

TEXT = (
    "Tomorrow we move and the silence will follow us, "
    "and every step will carry the weight of duty."
)

VARIANTS = [
    {
        "id": "1tag_playful",
        "tags": "playful",
        "text": TEXT,
        "note": "1 tag: [playful]",
    },
    {
        "id": "1tag_awed",
        "tags": "awed",
        "text": TEXT,
        "note": "1 tag: [awed]",
    },
    {
        "id": "1tag_happy",
        "tags": "happy",
        "text": TEXT,
        "note": "1 tag: [happy]",
    },
    {
        "id": "3tag_playful_awed_happy",
        "tags": "playful, awed, happy",
        "text": TEXT,
        "note": "3 tags: [playful, awed, happy] blended (vectors averaged element-wise)",
    },
]
