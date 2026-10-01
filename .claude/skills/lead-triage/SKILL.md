---
name: lead-triage
description: Classify inbound client messages (X/Instagram DMs, brief-form text) into campaign, retainer, partnership, question or scam, and queue them for human reply. Use when handling inquiries. Never auto-reply.
---

# Lead triage

Run: `python3 ops/run.py triage "<message>" [--live]`. Workflow: `ops/workflows/lead-triage.json`.

## What it asks (one request)
kind (Choice), urgency (Score 0-2), scam_risk (Noul), has_budget (Noul).

## Routing
- **inbox**: confident, non-scam lead. Owner replies.
- **review**: dry-run, scam risk, `spam_scam`, `other`, or low confidence. A human looks.
- Nothing is sent. Replying or posting is in `policy.approval_required`.

## Crypto-specific scam signals (treat as review even if confident)
Pays or asks you to pay first, wallet connect, seed phrase, "claim/airdrop/giveaway" links, fake collab from a lookalike handle, urgency plus off-platform move (Telegram/WhatsApp), unverifiable "partner" claims.

## Good leads
Name the project, chain, deliverable, deadline, budget. Use these to prefill the reply draft: quote range per project, ask for the contract address and a link to the project's X.

## Verified 2026-10-01
Live test: a legitimate memecoin launch request routed to inbox (`new_campaign`); an airdrop/seed-phrase message routed to review (`spam_scam`).
