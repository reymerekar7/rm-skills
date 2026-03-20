#!/usr/bin/env python3
"""
video-performance-analyzer — analyze_video.py

Uploads a local video file (or passes a YouTube URL) to the Gemini API,
extracts a full transcript, and returns a structured performance analysis.

Usage:
    python analyze_video.py /path/to/video.mp4
    python analyze_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python analyze_video.py /path/to/video.mp4 --output /path/to/output.md

Requires:
    pip install google-genai --break-system-packages
    GEMINI_API_KEY set in .env at repo root
"""

import argparse
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Load API key from .env
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """Walk up from this script to find .env in the repo root."""
    script_dir = Path(__file__).resolve().parent
    search = script_dir
    for _ in range(6):
        env_path = search / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        search = search.parent
    # Fall back to environment variable
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("ERROR: GEMINI_API_KEY not found in .env or environment.", file=sys.stderr)
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

def get_client():
    try:
        import google.genai as genai  # noqa: F401
    except ImportError:
        print("ERROR: google-genai not installed. Run: pip install google-genai --break-system-packages", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=load_api_key())


# ---------------------------------------------------------------------------
# Video upload + polling
# ---------------------------------------------------------------------------

def upload_video(client, file_path: str):
    """Upload a local video file to Gemini Files API and wait for ACTIVE state."""
    from google import genai  # noqa
    print(f"Uploading video: {file_path}", file=sys.stderr)
    video_file = client.files.upload(
        file=file_path,
        config={"mime_type": "video/mp4"}
    )
    print(f"Upload complete: {video_file.name} — waiting for processing...", file=sys.stderr)

    # Poll until ACTIVE
    max_wait = 120  # seconds
    waited = 0
    while video_file.state.name == "PROCESSING":
        if waited >= max_wait:
            print("ERROR: Video processing timed out after 120 seconds.", file=sys.stderr)
            sys.exit(1)
        time.sleep(5)
        waited += 5
        video_file = client.files.get(name=video_file.name)
        print(f"  Still processing... ({waited}s)", file=sys.stderr)

    if video_file.state.name != "ACTIVE":
        print(f"ERROR: Video entered unexpected state: {video_file.state.name}", file=sys.stderr)
        sys.exit(1)

    print(f"Video ready: {video_file.uri}", file=sys.stderr)
    return video_file


# ---------------------------------------------------------------------------
# Analysis prompt
# ---------------------------------------------------------------------------

ANALYSIS_PROMPT = """
You are analyzing a short-form social media video (TikTok / Instagram Reel / YouTube Short).
Return a structured Markdown analysis covering the sections below. Be specific and detailed —
generic observations are useless. Quote exact words where relevant.

---

## 1. FULL TRANSCRIPT

Provide a complete verbatim transcript with timestamps. Format:

**[HH:MM:SS – HH:MM:SS]**
> Spoken words here

Also note:
- Any on-screen text overlays (format as `[OVERLAY: "text"]`)
- Any background music (format as `[MUSIC: description]`)
- Any visual transitions or B-roll cuts (format as `[CUT: description]`)

---

## 2. VISUAL & AUDIO BREAKDOWN

- **Format:** (talking head / voiceover + B-roll / screen recording / mixed)
- **Creator presence:** Is the creator on camera? Voice-only? Faceless?
- **Background / set quality:** What does the environment look like? Any overlays, graphics, article screenshots?
- **Music:** Is there background music? Describe tempo, mood, genre. Does it add urgency or stay neutral?
- **Visual change frequency:** Roughly how often does the visual change (new overlay, cut, text card)? Estimate changes per minute.
- **Audio quality:** How crisp is the delivery? Mic type (earbud, studio, phone, etc.)?

---

## 3. HOOK ANALYSIS (first 0–5 seconds)

- **Exact hook words:** Quote the first sentence verbatim.
- **Hook type:** Which of these does it use?
  - Contradiction (says something that sounds wrong)
  - Specific number + unexpected context
  - Direct accusation (calls the viewer out)
  - Stolen thought (says what viewer secretly thinks)
  - Absurd reframe (makes something mundane dramatic)
  - Pattern interrupt (linguistic or visual surprise)
- **Hook strength (1–10):** Score it and explain why.
- **Is it viewer-first or creator-first?** Does the hook implicate the viewer, or announce the creator?

---

## 4. PROGRESSIVE INTRIGUE — STAKES MAP

List each major beat of the video (roughly every 20–40 seconds) and score the stakes level (1 = low, 5 = critical). The scores should increase over time in a well-constructed video.

Format:
| Timestamp | Beat description | Stakes (1–5) | Gap opened? |
|-----------|-----------------|--------------|-------------|
| 0:00–0:15 | ... | ... | ... |
| ... | ... | ... | ... |

Then assess:
- Does each beat raise the stakes from the last, or stay flat?
- Are beats connected by "therefore/but" (cause-consequence) or "and then" (passive continuation)?
- Where does the video lose momentum, if anywhere?

---

## 5. CREDIBILITY SIGNALS

List every specific claim in the video that includes:
- A named person (real name, title)
- A specific number, dollar amount, percentage, or date
- A named law, policy, company, or product
- Visual proof shown (article screenshot, headline, document)

Format: `[Timestamp] "Claim" — Signal type`

Weak claims (no specifics) should be flagged as: `[Timestamp] "Claim" — vague`

---

## 6. CTA ANALYSIS

- **Explicit CTA:** Is there a direct ask? Quote it exactly.
- **Implied CTA:** Does the close create a condition where following/sharing is the obvious next action?
- **Loop state:** Does the close resolve the viewer's open question (satisfying close) or leave one hanging (implied CTA, drives follows)?
- **CTA strength (1–10):** Score and explain.

---

## 7. PERFORMANCE SCORECARD

Score each dimension Weak / Moderate / Strong with a 1-sentence explanation:

| Dimension | Score | Why |
|-----------|-------|-----|
| Hook strength | | |
| Progressive intrigue | | |
| Specificity / credibility signals | | |
| Viewer-first framing | | |
| Visual pattern interrupts | | |
| Audio quality | | |
| CTA quality | | |

**Overall performance prediction:** Would this video likely outperform, match, or underperform the creator's average? Why?

---

## 8. REPURPOSING PLAYBOOK

Identify 5–8 standalone content ideas derived directly from this video. Each idea should be immediately actionable for a short-form creator.

For each idea:

**[Format] — [Working title / angle]**
- **Hook:** (1 sentence, viewer-first)
- **Format:** Short-form video / LinkedIn post / X thread / Newsletter section
- **Content pillar:** AI Implementation Reality / Behind the Scenes / Industry Hot Takes / Democratizing Expertise
- **Funnel stage:** TOFU / MOFU / BOFU
- **Why it'll work:** (1 sentence — specific mechanism, not generic)
- **Source moment:** (timestamp in the original video where this angle lives)

---

## 9. WHAT TO STEAL

List 3–5 specific techniques from this video that a creator should copy directly into their own content system. Be precise — name the exact moment, the exact technique, and why it works.

Format:
**Technique:** [Name it]
**Where it appears:** [Timestamp + quote]
**Why it works:** [Mechanism — psychological or structural]
**How to apply it:** [One concrete instruction]
"""


# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------

def run_analysis(client, video_source: str) -> str:
    """Run the analysis prompt against a video source (URI or YouTube URL)."""
    from google import genai  # noqa
    from google.genai import types  # noqa

    is_youtube = video_source.startswith("http://") or video_source.startswith("https://")

    if is_youtube:
        print(f"Using YouTube URL: {video_source}", file=sys.stderr)
        contents = [
            types.Part.from_uri(file_uri=video_source, mime_type="video/mp4"),
            types.Part.from_text(text=ANALYSIS_PROMPT),
        ]
    else:
        # Local file — upload first
        video_file = upload_video(client, video_source)
        contents = [
            types.Part.from_uri(file_uri=video_file.uri, mime_type="video/mp4"),
            types.Part.from_text(text=ANALYSIS_PROMPT),
        ]

    print("Running analysis (this may take 20–60 seconds)...", file=sys.stderr)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents,
    )

    return response.text


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Analyze a short-form video for transcript, performance, and repurposing ideas."
    )
    parser.add_argument(
        "video",
        help="Path to an MP4 file, or a YouTube URL (public videos only).",
    )
    parser.add_argument(
        "--output",
        help="Optional: save the analysis to this file path (Markdown).",
        default=None,
    )
    args = parser.parse_args()

    # Validate input
    video_input = args.video
    is_url = video_input.startswith("http://") or video_input.startswith("https://")
    if not is_url:
        if not Path(video_input).exists():
            print(f"ERROR: File not found: {video_input}", file=sys.stderr)
            sys.exit(1)
        if not video_input.lower().endswith(".mp4"):
            print("WARNING: File does not have .mp4 extension. Proceeding anyway.", file=sys.stderr)

    client = get_client()
    result = run_analysis(client, video_input)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(result)
        print(f"\nAnalysis saved to: {output_path}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
