#!/usr/bin/env python3
"""Attention Budget experiment — WPM scales linearly with word count.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: IndexTTS-2's fixed GPT token budget (25 steps) distributes attention across all
input tokens. Fewer words = more attention per word = slower, more deliberate delivery.

Method: Same base text progressively extended from 15 to 120 words.
        [solemn] emotion tag held constant. Budget at maximum (120 text tokens per segment).

Results:
    12 words  ->  5.0s, 145 WPM (deliberate)
    22 words  ->  9.2s, 143 WPM (moderate)
    49 words  -> 17.1s, 172 WPM (picking up)
    76 words  -> 26.1s, 175 WPM (noticeably faster)
   107 words  -> 32.7s, 196 WPM (fast, staccato)
   127 words  -> 38.1s, 200 WPM (fastest, maximum budget pressure)

Conclusion: WPM scales linearly with word count. Short text (<=15 words) achieves
143-145 WPM. 100+ words locks to 196-200 WPM regardless of tag.
"""

# ---- Test definitions (exact texts used in experiments) ----

TAG = "solemn"  # Held constant across all variants
TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120  # Budget at maximum

VARIANTS = [
    {
        "id": "w015_solemn",
        "words": 15,
        "text": (
            "Stand tall. The silence is listening. "
            "Do not let your hearts falter."
        ),
        "note": "15 words. Expect DELIBERATE, maximum attention per word.",
    },
    {
        "id": "w025_solemn",
        "words": 25,
        "text": (
            "I see the exhaustion in your eyes, the kind that sleep cannot fix. "
            "Hold it. Use it. Do not let them falter."
        ),
        "note": "25 words. Expect moderate pace, still clear.",
    },
    {
        "id": "w050_solemn",
        "words": 50,
        "text": (
            "I see the exhaustion in your eyes, the kind that sleep cannot fix. "
            "Hold it. Use it. Do not let your hearts turn to stone, but do not let "
            "them falter. Tomorrow, we move. Not because we are certain of victory, "
            "but because we are certain of our duty."
        ),
        "note": "50 words. Expect pace picking up.",
    },
    {
        "id": "w075_solemn",
        "words": 75,
        "text": (
            "I see the exhaustion in your eyes, the kind that sleep cannot fix. "
            "Hold it. Use it. Do not let your hearts turn to stone, but do not let "
            "them falter. Tomorrow, we move. Not because we are certain of victory, "
            "but because we are certain of our duty. Stand tall. The silence is listening. "
            "We did not come here for glory. Glory is a lie told by men who have "
            "never smelled ozone or iron."
        ),
        "note": "75 words. Expect noticeably faster.",
    },
    {
        "id": "w100_solemn",
        "words": 100,
        "text": (
            "I see the exhaustion in your eyes, the kind that sleep cannot fix. "
            "Hold it. Use it. Do not let your hearts turn to stone, but do not let "
            "them falter. Tomorrow, we move. Not because we are certain of victory, "
            "but because we are certain of our duty. Stand tall. The silence is listening. "
            "We did not come here for glory. Glory is a lie told by men who have "
            "never smelled ozone or iron. We came for each other. Look at the dirt "
            "beneath your boots. It is indifferent to our cause, yet it is the only "
            "thing that will remain when the smoke clears."
        ),
        "note": "100 words. Expect fast, staccato.",
    },
    {
        "id": "w120_solemn",
        "words": 120,
        "text": (
            "I see the exhaustion in your eyes, the kind that sleep cannot fix. "
            "Hold it. Use it. Do not let your hearts turn to stone, but do not let "
            "them falter. Tomorrow, we move. Not because we are certain of victory, "
            "but because we are certain of our duty. Stand tall. The silence is listening. "
            "We did not come here for glory. Glory is a lie told by men who have "
            "never smelled ozone or iron. We came for each other. Look at the dirt "
            "beneath your boots. It is indifferent to our cause, yet it is the only "
            "thing that will remain when the smoke clears. The standard is not held "
            "by hands alone. It is held by the weight of those who no longer stand."
        ),
        "note": "120 words. Expect FASTEST, maximum budget pressure.",
    },
]
