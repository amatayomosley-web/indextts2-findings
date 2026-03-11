#!/usr/bin/env python3
"""Flattener vs Preserver experiment — tags and structure are independent layers.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: Emotion tags and text structure operate as independent layers.
      - Tags control CHARACTER (how it sounds)
      - Structure controls QUALITY (how well it sounds)
      - "Flattener" tags ([solemn], [measured]) suppress delivery contours
      - "Preserver" tags ([playful]) preserve natural dynamics

Method: Two texts with opposing structural properties, cross-tested with both
        a flattener tag ([solemn]) and a preserver tag ([playful]).

        Flattener text: Rigid, declarative sentences. Minimal prosodic variation.
        Preserver text: Dynamic, questioning. Natural ups and downs.

Results:
    Flattener text (30w) + [solemn]  -> 143 WPM, 12.6s
    Flattener text (30w) + [playful] -> 174 WPM, 10.4s
    Preserver text (34w) + [solemn]  -> 179 WPM, 11.4s
    Preserver text (34w) + [playful] -> 207 WPM,  9.9s

Conclusion: [solemn] actively suppresses delivery contours regardless of text
structure. [playful] preserves natural dynamics but cannot add contour that the text
does not already contain. Tags and structure are independent layers.
"""

# ---- Test definitions (exact texts used in experiments) ----

TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120

FLATTENER_TEXT = (
    "The foundation is set. Every stone is placed with absolute precision. "
    "We do not deviate. We do not falter. The structure remains perfectly "
    "still, echoing through the cold, silent halls."
)

PRESERVER_TEXT = (
    "Did you see that? It is just a tiny spark, dancing in the dark. "
    "Shhh... if we stay very still, we might see where the light decides "
    "to land next. Is it not wonderful?"
)

VARIANTS = [
    # Natural pairings
    {
        "id": "flattener_solemn",
        "text": FLATTENER_TEXT,
        "tag": "solemn",
        "note": "Flattener text + [solemn] (natural pairing)",
    },
    {
        "id": "preserver_playful",
        "text": PRESERVER_TEXT,
        "tag": "playful",
        "note": "Preserver text + [playful] (natural pairing)",
    },
    # Swapped tags
    {
        "id": "flattener_playful",
        "text": FLATTENER_TEXT,
        "tag": "playful",
        "note": "Flattener text + [playful] (SWAPPED)",
    },
    {
        "id": "preserver_solemn",
        "text": PRESERVER_TEXT,
        "tag": "solemn",
        "note": "Preserver text + [solemn] (SWAPPED)",
    },
]
