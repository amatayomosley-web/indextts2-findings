# IndexTTS-2: Structural Delivery Rules

Controlled experiments revealing how IndexTTS-2's architecture shapes speech delivery. These findings were produced during audiobook production R&D targeting 150-160 WPM narration pace.

**Model**: [IndexTTS-2](https://github.com/index-tts/index-tts) (~2.5B params, BigVGAN v2 vocoder, 22kHz)
**Hardware**: RTX 5060 Ti 16GB, FP16
**Voice**: Single female reference (political/analytical register)
**Emotion control**: Mode 3 (8D vector) -- dimensions: [happy, sad, angry, surprised, scared, warm, neutral, serious]

---

## TL;DR

IndexTTS-2 uses a fixed GPT token budget (25 steps) that compresses all text tokens into a fixed-length output. This creates an architectural speed floor: more words per segment = faster speech. Target audiobook pace (150-160 WPM) is unreachable at usable quality.

Four structural rules govern delivery:

| # | Rule | Summary |
|---|------|---------|
| 1 | **Attention Budget** | WPM scales linearly with word count. Short text = deliberate. Long = staccato. |
| 2 | **Punctuation Transparency** | All punctuation marks produce equivalent delivery. Not a pacing tool. |
| 3 | **Flatteners vs Preservers** | Some emotion tags suppress delivery contours; others preserve them. Independent of text. |
| 4 | **Invisible Dimensions** | Word weight, grammar voice, and repetition patterns are transparent to the model. |

---

## Rule 1: Attention Budget

**Hypothesis**: The fixed GPT budget distributes attention across all input tokens. Fewer words = more attention per word = slower, more deliberate delivery.

**Method**: Same text progressively extended from 12 to 127 words. [solemn] emotion tag held constant. Budget at maximum (120 text tokens per segment).

### Results

| Words | Duration | WPM | Observation |
|------:|--------:|----:|-------------|
| 12 | 5.0s | 145 | Deliberate, maximum attention per word |
| 22 | 9.2s | 143 | Moderate pace, still clear |
| 49 | 17.1s | 172 | Pace picking up |
| 76 | 26.1s | 175 | Noticeably faster |
| 107 | 32.7s | 196 | Fast, staccato |
| 127 | 38.1s | 200 | Fastest, maximum budget pressure |

**Conclusion**: WPM scales linearly with word count. Short text (15 words or fewer) achieves 143-145 WPM, near audiobook target. 100+ words locks to 196-200 WPM regardless of emotion tag. The only way to slow delivery is to reduce word count per segment.

**Script**: [`experiments/attention_budget.py`](experiments/attention_budget.py)

---

## Rule 2: Punctuation Transparency

**Hypothesis**: Punctuation marks (commas, ellipses, semicolons, exclamations, question marks) do not independently affect delivery pacing or intonation.

**Method**: A/B test with identical 30-word text. Version A uses heavy punctuation (commas, ellipses, exclamation, colon, question mark). Version B strips most punctuation to bare sentences.

### Results

| Variant | Duration | WPM |
|---------|--------:|----:|
| WITH punctuation | 10.8s | 166 |
| WITHOUT punctuation | 9.8s | 184 |

Additionally, 14 short variants were tested with different punctuation saturation levels (ellipses, quotes, semicolons, exclamations, questions). All mark types produce equivalent delivery -- no mark affects intonation differently from any other.

**Conclusion**: Punctuation effects are very minor. Marks are not a useful delivery tool in IndexTTS-2. The model does not interpret punctuation as prosodic instruction.

**Script**: [`experiments/punctuation_ab.py`](experiments/punctuation_ab.py)
**Audio**: [`audio/punctuation_ab/`](audio/punctuation_ab/) -- `punct_heavy.wav` (with punctuation) vs `punct_stripped.wav` (without) -- listen for what *should* sound different but doesn't

---

## Rule 3: Flatteners vs Preservers

**Hypothesis**: Emotion tags and text structure operate as independent layers. Tags control *character* (how it sounds). Structure controls *quality* (how well it sounds). Some tags actively suppress delivery contours ("flatteners"), while others preserve natural dynamics ("preservers").

**Method**: Two texts designed with opposing structural properties, then cross-tested with both a flattener tag ([solemn]) and a preserver tag ([playful]).

- **Flattener text** (rigid, declarative): "The foundation is set. Every stone is placed with absolute precision. We do not deviate. We do not falter. The structure remains perfectly still, echoing through the cold, silent halls."
- **Preserver text** (dynamic, questioning): "Did you see that? It is just a tiny spark, dancing in the dark. Shhh... if we stay very still, we might see where the light decides to land next. Is it not wonderful?"

### Results

| Text | [solemn] | [playful] |
|------|--------:|--------:|
| Flattener (30w) | 143 WPM, 12.6s | 174 WPM, 10.4s |
| Preserver (34w) | 179 WPM, 11.4s | 207 WPM, 9.9s |

**Conclusion**: [solemn] actively suppresses delivery contours regardless of text structure. [playful] preserves natural dynamics but cannot add contour that the text does not already contain. Tags and structure are independent layers -- structure controls quality, tags control character.

**Script**: [`experiments/flattener_preserver.py`](experiments/flattener_preserver.py)
**Audio**: [`audio/flattener_preserver/`](audio/flattener_preserver/) -- 4 WAV files demonstrating the tag swap

---

## Rule 4: Invisible Dimensions

**Hypothesis**: Certain writing dimensions that affect human reading (word weight, grammar voice, repetition patterns) are transparent to the model.

**Method**: Three A/B pairs testing each dimension in isolation with no emotion tag.

### Word Weight (concrete vs abstract nouns, same sentence structure)

| Variant | Words | Duration | WPM |
|---------|------:|--------:|----:|
| Concrete (blood, iron, stone) | 15 | 4.7s | 193 |
| Abstract (concept, theory, idea) | 14 | 5.1s | 163 |

WPM difference tracks word count (attention budget), not word weight. Delivery is identical.

### Grammar Voice (active vs passive vs imperative)

| Variant | Words | Duration | WPM |
|---------|------:|--------:|----:|
| Active | 12 | 3.9s | 185 |
| Passive | 12 | 4.0s | 180 |
| Imperative | 9 | 3.2s | 169 |

Active/passive within 5 WPM on same word count. Imperative lower due to fewer words. All sound the same.

### Repetition (anaphora vs varied structure)

| Variant | Words | Duration | WPM |
|---------|------:|--------:|----:|
| Anaphora ("We hold" x3) | 12 | 3.8s | 191 |
| Varied (no repetition) | 12 | 4.1s | 176 |

No rhythmic momentum from repetition. All monotone. Confirmed by listening.

**Conclusion**: All three dimensions are invisible to the model. Writing style does not affect delivery.

**Script**: [`experiments/transparent_dims.py`](experiments/transparent_dims.py)

---

## Additional Experiments

### Tag Character Test (sarcastic)

Same 35-word text with and without [sarcastic] tag:

| Variant | Duration | WPM |
|---------|--------:|----:|
| [sarcastic] tag | 12.2s | 173 |
| No tag (same text) | 12.3s | 170 |

Tags change character (sarcastic delivery), not speed. 3 WPM difference is within noise.

**Script**: [`experiments/sarcastic_tag.py`](experiments/sarcastic_tag.py)
**Audio**: [`audio/sarcastic_tag/`](audio/sarcastic_tag/) -- with tag vs without

### Compound Tag Blending

Same 18-word text with single tags vs 3-tag blend (vectors averaged element-wise, highest alpha used):

| Variant | WPM |
|---------|----:|
| [playful] | 227 |
| [awed] | 226 |
| [happy] | 246 |
| [playful, awed, happy] | 239 |

Blend lands in the middle of individual tag values. Stacking does not degrade quality at 3 tags on short text.

**Script**: [`experiments/compound_tags.py`](experiments/compound_tags.py)

### Multi-Take Reconstruction

Best-take selection from multiple generations using energy-continuity scoring:

| Takes | WPM | Duration |
|------:|----:|--------:|
| 1 | 181 | 87.4s |
| 3 | 196 | 85.6s |
| 5 | 200 | 91.1s |

Multi-take selection does not slow delivery. Best takes tend toward higher energy (faster).

### Prosody Audio Conditioning (CAMPPlus)

Modified `infer_v2.py` to inject prosody audio via CAMPPlus speaker embedding pathway:

| Condition | WPM |
|-----------|----:|
| Isolated (control) | 219 |
| Alpha=0.3 | 224 |
| Alpha=0.5 | 210 |

CAMPPlus pathway affects timbre, not pace. The speaker embedding does not carry prosodic timing information.

---

## Workarounds Exhausted

All approaches to achieve 150-160 WPM were tested and failed:

| Approach | Result |
|----------|--------|
| Budget reduction | Too choppy below 25 steps |
| Multi-take selection | Best take still 196-210 WPM |
| Audio compiler | Fixes transitions, not speed |
| Text preroll | Concatenation doubles word count, WPM goes UP |
| Prosody audio conditioning | Affects timbre, not pace |
| Lookahead/crossfade | Smooths cuts between segments, not speed |

**Root cause**: The fixed GPT token budget (25 steps) is architectural. Speed is a function of word count, not a tunable parameter.

**Recommendation**: Revisit when IndexTTS-2.5 releases, which may decouple GPT steps from text token count.

---

## Critical Constraints (for implementers)

- **Contraction bug**: Tokenizer corrupts contractions ("don't" produces garbled audio). Expand all contractions before synthesis.
- **BigVGAN pop**: 10-30ms fade-out mandatory on every clip to prevent end-of-clip pops.
- **CUDA memory leak**: Model must be recreated every ~150 segments to prevent OOM.
- **FP16 required**: FP32 produces degraded audio quality.
- **Budget = speed**: Fixed GPT steps (25) compress all tokens. More words = faster. This is not tunable.

---

## About the Experiments

All experiments use the same voice reference, temperature (0.5), and maximum token budget (120). Emotion tags are applied via Mode 3 (8D vector control). Scripts in `experiments/` contain the exact test definitions (texts, variants, parameters) used to produce these results. They are reference implementations -- running them requires IndexTTS-2 model weights and the synthesis engine.

---

## License

MIT
