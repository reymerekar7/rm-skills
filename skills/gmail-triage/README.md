# Gmail Triage

Automated inbox triage that flags what's important, summarizes newsletters, and cleans up noise — without ever sending an email.

## What It Does

- Categorizes unread emails into Action Required, Newsletter, and Low Priority
- Summarizes newsletters by topic (AI/Tech, Business, Health, etc.)
- Marks low-priority and newsletter emails as read
- Delivers a scannable briefing in under 60 seconds

## Prerequisites

- **Google Workspace CLI** — `npm install -g @googleworkspace/cli`
- Run `gws auth setup` to authenticate with your Gmail account
- Python 3.9+ (for the newsletter text extractor)

## Usage

This skill is designed to be invoked by Claude Code. Just say:
- "Check my email"
- "Triage my inbox"
- "Any important emails?"
- "Newsletter recap"

## How It Works

1. Pulls unread primary inbox via `gws gmail +triage`
2. Categorizes each email (Action Required / Newsletter / Low Priority)
3. Fetches and summarizes newsletter content
4. Marks newsletters and low-priority emails as read
5. Presents a structured briefing

## Important

This skill is **read-only** — it never sends, replies to, forwards, or deletes emails.
