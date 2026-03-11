#!/usr/bin/env python3
"""Transparent Dimensions experiment — word weight, grammar voice, repetition.

Reference implementation. Requires IndexTTS-2 model weights and synthesis engine to run.

Rule: Word weight, grammar voice, and repetition patterns are all invisible to
IndexTTS-2. The model delivers identical monotone regardless of these dimensions.

Method: Three A/B pairs, each isolating one dimension. No emotion tag applied.

Results:

  Word weight (concrete vs abstract, same structure):
    Concrete (blood, iron, stone) -> 15w, 4.7s, 193 WPM
    Abstract (concept, theory, idea) -> 14w, 5.1s, 163 WPM
    WPM difference tracks word count (attention budget), not word weight.

  Grammar voice (active vs passive vs imperative):
    Active -> 12w, 3.9s, 185 WPM
    Passive -> 12w, 4.0s, 180 WPM
    Imperative -> 9w, 3.2s, 169 WPM
    Active/passive within 5 WPM on same word count. Imperative lower = fewer words.

  Repetition (anaphora vs varied):
    Anaphora ("We hold" x3) -> 12w, 3.8s, 191 WPM
    Varied (no repetition) -> 12w, 4.1s, 176 WPM
    No rhythmic momentum from repetition. All monotone.

Conclusion: All three dimensions confirmed invisible. Writing style does not
affect delivery.
"""

# ---- Test definitions (exact texts used in experiments) ----

TAG = ""  # No emotion tag
TEMPERATURE = 0.5
MAX_TEXT_TOKENS = 120

VARIANTS = [
    # --- Word Weight (concrete vs abstract, same structure) ---
    {
        "id": "ww_concrete",
        "text": "The blood dried on the stone. The iron gate held. The cold wind cut through.",
        "note": "Word weight: CONCRETE nouns (blood, iron, stone, wind).",
    },
    {
        "id": "ww_abstract",
        "text": "The concept failed in the theory. The idea held. The quiet doubt crept through.",
        "note": "Word weight: ABSTRACT nouns (concept, theory, idea, doubt).",
    },

    # --- Grammar Voice (active vs passive vs imperative) ---
    {
        "id": "gv_active",
        "text": "She broke the silence. She crossed the hall. She opened the door.",
        "note": "Grammar voice: ACTIVE.",
    },
    {
        "id": "gv_passive",
        "text": "The silence was broken. The hall was crossed. The door was opened.",
        "note": "Grammar voice: PASSIVE.",
    },
    {
        "id": "gv_imperative",
        "text": "Break the silence. Cross the hall. Open the door.",
        "note": "Grammar voice: IMPERATIVE.",
    },

    # --- Repetition Patterns (anaphora vs varied) ---
    {
        "id": "rp_anaphora",
        "text": "We hold the line. We hold the ground. We hold each other.",
        "note": "Repetition: ANAPHORA (We hold x3).",
    },
    {
        "id": "rp_varied",
        "text": "We hold the line. The ground stays firm. They stand beside us.",
        "note": "Repetition: VARIED structure (no repetition).",
    },
]
