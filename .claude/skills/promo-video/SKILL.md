---
name: promo-video
description: Make a captivating short promo video for Young Stunners with zero paid APIs - code-driven animation, offline neural voice-over, synthesized score. Use when the owner asks for a video, reel, trailer or explainer of the work.
---

# Promo video (free, local, repeatable)

Everything lives in `video/`. No API keys, no credits: Chromium renders frames, Piper (offline neural TTS) speaks, numpy writes the music, ffmpeg muxes. Never swap in ElevenLabs/MuAPI/Gemini/etc. for this.

## Pipeline
1. `scene.template.html` - deterministic animation driven by `setT(t)` (no wall-clock). Edit copy/timings here; `scene.html` is generated from it by replacing `__AV__` with the avatar list.
2. `node video/audit.mjs` - **must be clean before rendering.** Flags text outside the 16px safe margin and text-on-text overlaps. (The first cut shipped with clipped headlines; this exists so it never happens again.)
3. `voice.py` - `LINES` = (start s, max seconds, text). Starts must equal visual beats. Lines that overrun are sped up to 1.35x max; if you need more, cut words, don't rush.
4. `score.py` - 120 BPM synth, impacts on scene cuts, music ducks under the voice. Run after `voice.py`.
5. `node video/render.mjs <start> <end> <dir>` (end exclusive; run 4 shards of 225 frames in parallel), then ffmpeg `-framerate 30 -i f%04d.jpg -i score.wav` -> libx264 crf 18, yuv420p, aac, +faststart.
6. Deliver **both** `young-stunners-30s.mp4` (1080x1920) and `young-stunners-30s-landscape.mp4` (1920x1080, same video centred over a blurred copy of itself, so no viewer ever crops it).

## Setup in a fresh container
`pip install --target /tmp/pylibs numpy imageio-ffmpeg piper-tts`; voice model from `huggingface.co/rhasspy/piper-voices` (`en/en_US/ryan/high/en_US-ryan-high.onnx` + `.json`) into `/tmp/voices`. Run python with `PYTHONPATH=/tmp/pylibs`.

## Creative rules (what makes it land)
- Hook in 1 second, and name the pain: "Your project is brilliant. Nobody saw it."
- One idea per scene, 3-6 s: hook, who, brief->create->approve, amplify, offer, CTA.
- Every cut gets a flash + impact hit; every number counts up; every word on screen is also spoken.
- Voice is the pacing authority: write the line, time it, then place the visual.
- Sticker system only: paper/ink/red, Montserrat, hard shadows. No gradients-on-everything, no stock emoji.
- Only true facts: numbers come from `index.html` facts line (38 projects, 130 posts, dated range). Never invent metrics, quotes or client names. The game's GitHub repo is never shown.
- Review at least 12 spot frames across all scenes (contact sheet) and read the transcript out loud before sending.
