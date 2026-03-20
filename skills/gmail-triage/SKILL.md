---
name: gmail-triage
description: >
  Triage your Gmail inbox using the Google Workspace CLI (gws). Use this
  skill whenever the user asks to: check email, triage inbox, scan for important
  messages, summarize newsletters, do a morning email check, or anything involving
  reading and categorizing unread emails. Also trigger when the user says things
  like "what's in my inbox", "any important emails", "check my email",
  "email briefing", "newsletter recap", or "mark emails as read". This skill is
  READ-ONLY — it never sends, replies to, or forwards emails.
---

# Gmail Triage Skill

You help the user stay on top of their inbox without getting sucked into it. Your job is to surface what matters, summarize what's informational, and clean up the noise — all without ever sending a single email.

## Philosophy

Email is a todo list other people write for you. The goal is to protect attention:

1. **Flag what's important** — anything requiring a decision, response, or action
2. **Summarize what's informational** — newsletters grouped by topic so you get the value without the time sink
3. **Clean up the rest** — mark low-priority emails as read so they stop cluttering the unread count

This skill is strictly read-only. Never send, reply, forward, or draft emails. If something needs a response, surface it — don't do it.

---

## Prerequisites

The Google Workspace CLI must be installed and authenticated:

```bash
npm install -g @googleworkspace/cli
gws auth setup
```

Verify it works: `gws gmail +triage` should return unread inbox data.

---

## Scope

**Primary inbox only.** Only triage emails in `category:primary`. Ignore promotions, social,
updates, and forums unless explicitly asked to check those.

---

## Helper Scripts

Reusable scripts live in `<skill-directory>/scripts/`:

- **`extract_newsletter.py`** — Extracts readable text from raw `gws` message JSON (base64-decoded).
  Pipe from gws or stdin:
  ```bash
  gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' \
    | python <skill-directory>/scripts/extract_newsletter.py
  ```

- **`mark_read.sh`** — Marks one or more messages as read. Run sequentially (not backgrounded)
  to avoid race conditions:
  ```bash
  bash <skill-directory>/scripts/mark_read.sh MSG_ID1 MSG_ID2 MSG_ID3
  ```

---

## Triage Workflow

### Step 1: Pull the primary inbox

Start with the triage helper:

```bash
gws gmail +triage
```

This returns sender, subject, and date for unread messages. **Filter to primary only** —
skip anything in promotions, social, updates, or forums categories (check labelIds).

For more detail on specific messages (e.g., to read a newsletter body), fetch individually:

```bash
gws gmail users messages get --params '{"userId":"me","id":"<message_id>","format":"full"}'
```

Then pipe through the extract script to get readable text:
```bash
gws gmail users messages get --params '{"userId":"me","id":"<message_id>","format":"full"}' \
  | python <skill-directory>/scripts/extract_newsletter.py
```

Other useful queries:

```bash
gws gmail users messages list --params '{"userId":"me","maxResults":20,"q":"is:unread category:primary"}'
```

### Step 2: Categorize every email

Go through each unread message and assign it to one of three buckets:

**Action Required** — Flag these and keep unread. Characteristics:
- From a real person the user knows or works with (clients, collaborators, friends, family)
- Mentions money, deals, contracts, deadlines, or meetings
- Asks a direct question or requests a decision
- Time-sensitive (event RSVPs, expiring offers relevant to business)
- From platforms where the user has active business
- From any sender the user has told you to always flag

**Newsletter / Informational** — Summarize these, then mark as read. Characteristics:
- AI/tech newsletters (TLDR, Ben's Bites, The Neuron, Import AI, Superhuman, etc.)
- Industry updates, product launches, funding news
- Business/creator economy newsletters
- Fitness, health, mindset, or personal development content
- Marketing or growth content

**Low Priority** — Mark as read silently. Characteristics:
- Automated notifications (GitHub, Notion, app alerts)
- Marketing/promotional emails from brands
- Social media notifications (LinkedIn, X, Instagram)
- Receipts and order confirmations (unless very recent / relevant)
- Spam or irrelevant outreach

When in doubt, err on the side of flagging as important — better to surface something irrelevant than miss something that mattered.

### Step 3: Summarize newsletters by topic

For Newsletter emails, fetch the full body if needed, then group summaries by broad topic:

- **AI / Tech** — lead with this group, give it the most depth. Focus on what's relevant: AI agents, developer tools, new models, content creation tech, solo founder tools
- **Business / Creator Economy** — growth strategies, monetization, newsletter tactics, sponsorship trends
- **Fitness / Health** — training science, nutrition, recovery
- **Mindset / Personal Development** — productivity, mental models, habits
- **Other** — anything that doesn't fit the above

For each newsletter:
- 2-4 bullet points max — focus on what's actionable or relevant
- Call out anything that's a potential content idea or business opportunity
- Skip the fluff entirely

### Step 4: Mark emails as read

Mark both Newsletter and Low Priority emails as read using the helper script:

```bash
bash <skill-directory>/scripts/mark_read.sh MSG_ID1 MSG_ID2 MSG_ID3 ...
```

Or individually:
```bash
gws gmail users messages modify --params '{"userId":"me","id":"<message_id>"}' --json '{"removeLabelIds":["UNREAD"]}'
```

**Important:** Run mark-as-read sequentially, not backgrounded with `&`. Backgrounding causes race conditions with the gws keyring.

Do NOT mark Action Required emails as read — those stay unread until the user handles them.

### Step 5: Deliver the briefing

Present results in this order:

**1. Action Required** (if any)
For each: who it's from, what they need, and a suggested next step.

**2. Newsletter Highlights** (if any)
Grouped by topic (AI/Tech first, then others). Each newsletter gets a name + 2-4 bullets.

**3. Cleanup Summary**
One line: "Marked X emails as read" with a few examples of what was cleared.

Keep it tight. The whole briefing should be scannable in under 60 seconds.

---

## Important Senders (always flag)

If an email is from any of these, it's Action Required regardless of content:

- Any email from a real person (not a no-reply address) that appears to be a direct message
- Sponsors, brand partners, or anyone discussing business deals
- Any client or prospect
<!-- Add your important senders here — e.g., co-founders, key collaborators, specific platforms -->

This list evolves — if the user says to always flag someone, add them here.

---

## What This Skill Does NOT Do

- Send, reply to, forward, or draft emails
- Delete emails
- Move emails between folders/labels (except marking as read)
- Write anything to Notion or other systems
- Access accounts other than the authenticated Gmail

If asked to reply or send, remind the user this skill is read-only and suggest they handle it directly.
