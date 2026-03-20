---
name: video-performance-analyzer
description: >
  Analyze a short-form video (TikTok, Instagram Reel, or any MP4) to extract
  its full transcript, understand why it performed, and generate concrete
  repurposing ideas. Use this skill whenever the user asks to: analyze a video,
  understand why something went viral, reverse-engineer a creator's content,
  extract a transcript from a video, figure out what makes a video perform,
  or get repurposing ideas from a video. Also trigger when the user says things
  like "why did this perform", "what's the hook here", "can I repurpose this",
  "analyze this TikTok", or drops a video file path or URL.
compatibility: "Requires GEMINI_API_KEY in .env at repo root. Install google-genai: pip install google-genai --break-system-packages"
---

# Video Performance Analyzer

## What This Skill Does

Takes a short-form video (MP4 file or YouTube URL) and returns three things:

1. **Full transcript** — every spoken word, on-screen text, audio cues, with timestamps
2. **Performance analysis** — why it works, mapped against proven growth frameworks
3. **Repurposing playbook** — concrete content ideas derived from the video

---

## Setup

The analysis script uses Google's Gemini API (generative model for transcript + analysis).

**API Key:** Read from `.env` at repo root — `GEMINI_API_KEY`

**Install dependency (one-time):**
```bash
pip install google-genai --break-system-packages
```

**Script location:** `<skill-directory>/scripts/analyze_video.py`

---

## Input Formats

| Format | How to pass it | Notes |
|--------|---------------|-------|
| Local MP4 file | File path as argument | Any size up to 2GB (free) / 20GB (paid) |
| YouTube URL | URL as argument | Public videos only |
| TikTok / Instagram | Download first, then pass MP4 path | Use browser extension or yt-dlp |

---

## Running the Analysis

### Quick run
```bash
python <skill-directory>/scripts/analyze_video.py /path/to/video.mp4
```

### YouTube URL
```bash
python <skill-directory>/scripts/analyze_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### With output saved to file
```bash
python <skill-directory>/scripts/analyze_video.py /path/to/video.mp4 --output /path/to/output.md
```

The script prints structured Markdown to stdout. Pipe or redirect as needed.

---

## Analysis Workflow

### Step 1: Run the script

Run `analyze_video.py` with the video path. The script will:
- Upload the video to Gemini Files API (or pass YouTube URL directly)
- Wait for processing (usually 10-30 seconds)
- Send the analysis prompt to `gemini-3-flash-preview`
- Return raw structured output

### Step 2: Map against growth frameworks

After the script returns, interpret the output through these growth dimensions:

**Hook — "The Hook Is a Contract"**
- Did the hook make the viewer feel implicated, called out, or urgently curious?
- Does it pass any of the 5 hook techniques? (Contradiction, Specific number + unexpected context, Direct accusation, Stolen thought, Absurd reframe)
- Is it about the viewer's situation — or the creator's achievement?
- Framing trick to look for: deliberate word choice that raises perceived stakes

**Structure — Progressive Intrigue**
- Map each timestamp beat and score whether stakes escalate beat-to-beat
- Look for the "therefore/but" chain — does each beat cause the next, or just follow it?
- Identify where the information gaps open and where they close
- Flag any beat that could be predicted from the one before it

**Credibility — Specificity Signal**
- Count concrete numbers, named people, specific dates, dollar amounts
- Note any "documentary proof" moments (showing receipts/sources visually as claims are made)
- Generic claims = weak. Named + numbered claims = strong.

**Framing — Reader-First**
- Is the video about the creator's achievement, or the viewer's situation?
- Every strong performing video frames its value around what the *viewer* gets
- Personal milestone framing = performs with existing audience, dies everywhere else

**Retention — Visual Pattern Interrupts**
- How often does the visual change? Every 5-10s is the target
- Better backgrounds / overlays = higher retention = platform pushes to new audiences
- Note any transitions, overlays, text cards, B-roll cuts that reset attention

**CTA — Loop-Closing vs. Loop-Opening**
- Does the close resolve the viewer's question, or leave one open?
- Best CTAs create a condition where following is the obvious next move (implied CTA)
- Weak CTAs: "like and follow if you learned something", "let me know in the comments"
- Strong CTAs: "we'll see what happens in a few hours" (creates forward momentum)

### Step 3: Generate repurposing ideas

Based on the analysis, identify every angle that could become standalone content. For each idea:
- What format fits best (short-form video, LinkedIn post, X thread, newsletter section)
- What the hook/banner should be
- Whether it maps to a content pillar (AI Implementation Reality, Behind the Scenes, Industry Hot Takes, Democratizing Expertise)
- Funnel stage (TOFU / MOFU / BOFU)

**Repurposing sources to mine:**
- The strongest single claim in the video -> standalone hot take post
- The "before/after" or "X vs. Y" implicit in the narrative -> comparison format
- Any step-by-step workflow mentioned -> listicle or tools video
- The emotional core (fear, surprise, outrage, relief) -> personal angle script
- Any stat or number -> data-driven short-form
- The contrarian framing (if present) -> X thread or newsletter hook

### Step 4: (Optional) Push to your content calendar

If you use Notion as a content calendar, you can push repurposing ideas after analysis.

Configure your Notion data source ID in your project settings:
```
data_source_id: <your-notion-database-id>
```

Default fields for repurposed content:
- Status: `Backlog`
- Platform: based on format fit
- Content Format: `["Video"]` for scripts, `["Text"]` for posts
- Content Type: based on angle
- Funnel Stage: `TOFU` (most repurposed content is awareness-level)
- Re-purpose?: `Yes`

---

## Output Format

Deliver results in this order:

### 1. Full Transcript
Timestamped, verbatim. Include on-screen text overlays noted inline.

### 2. Visual & Audio Breakdown
- Format (talking head / voiceover / B-roll / screen recording)
- Background / set design quality
- Music / audio tone
- Visual change frequency (pattern interrupts per minute)

### 3. Performance Analysis
Score each dimension (Strong / Moderate / Weak):

| Dimension | Score | Notes |
|-----------|-------|-------|
| Hook strength | | |
| Progressive intrigue | | |
| Specificity / credibility | | |
| Reader-first framing | | |
| Visual pattern interrupts | | |
| CTA quality | | |

Then 3-5 bullet points on *why* this video performs — the specific mechanisms, not generic observations.

### 4. Repurposing Playbook
For each idea:
```
**[Format] — [Working title / angle]**
- Hook: ...
- Format: ...
- Content pillar: ...
- Funnel stage: ...
- Why it'll work: 1 sentence
```

Aim for 4-8 repurposing ideas per video. At least 2 should be immediately scriptable.

### 5. What to Steal
3-5 specific, actionable techniques from this video that you should copy directly into your own content system. Concrete, not generic. Reference the specific moment in the video where each technique appears.

---

## What This Skill Does NOT Do

- Download TikTok or Instagram videos (download manually, then pass the path)
- Post or publish anything — analysis and ideation only
- Access private or unlisted YouTube videos
- Replace your creative judgment — the analysis surfaces what's working, your taste picks what to steal

---

## Notes on Model Selection

- **Transcript + analysis:** `gemini-3-flash-preview` — best video understanding, handles 3-5min short-form easily
- **Embedding (future):** `gemini-embedding-2-preview` — for comparing videos semantically against a library of performers. Not yet implemented in the script but the architecture is ready.
- **Free tier limits:** 8 hours of YouTube video/day. No limit on uploaded files (paid tier). Short-form videos are well within limits.
