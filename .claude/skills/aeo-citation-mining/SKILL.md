---
name: aeo-citation-mining
description: Measure and improve how AI assistants mention and cite Young Stunners using entity-based probes, citation mining and small on-page tests. Use for AI-visibility work after the basics in seo-aeo-geo-playbook are done.
---

# AEO citation mining

Source: Dan Petrovic on the Ahrefs podcast (transcript doc), plus our research. Claims marked (unverified) came from the transcript only.

## How the engines get answers
- The model does not crawl. A harness runs fan-out searches, a search index returns results, the model re-ranks and writes. So rank in the indexes first: ChatGPT leans on Bing (and sometimes Google), Gemini on Google, Claude on Brave. Submit to **Bing Webmaster** and check **Brave Search** too, not just Google.
- Grounding (your page is supplied), citation (a sentence is attributed to it) and mention (brand named; a **link mention** is best) are different. Optimise for the link mention.
- Google may attach several sources to one sentence; OpenAI tends to attach one. Gemini gets extractive snippets (verbatim cut-outs), so **each section must carry the brand and the offer in its own extractable sentences**.
- Reddit and review-site citations reportedly collapsed in ChatGPT while help/docs pages rose (unverified, social post). Direction to follow either way: invest in the site's own answer content, not only social.

## No prompt volume exists
Do not chase "prompt search volume". Use entities instead: "Web3 video content creator", "crypto KOL for token launches", "Young Stunners".

## Weekly probe (workflow `visibility-sample`)
1. For each entity ask each engine with web grounding on: "A client is looking for {entity}. Recommend some brands." Fixed wording every week.
2. Record per run: present?, ordinal position, mention type (text/link), cited URL, competitors. Append to `docs/visibility/log.csv`.
3. Metrics: frequency, average position, mention share, citation share. Trend over weeks; one run is noise.
4. Reverse method: give a URL to a model and ask "what would people type to be recommended this page?"; keep prompts where it actually happens.
5. **Citation mining**: open the pages that are cited for your entities. Copy their structure (comparison tables, dates, specifics), never their text.
6. **On-page loop**: one small change at a time (a section's first sentence, a comparison, a dated fact), re-probe next week, keep what moves position.

## Site-level to-dos this implies
- Bing Webmaster + Brave check (needs owner login/DNS).
- Comparison and "how it works" content (answer-first), kept short per concise-copy.
- Topical centrality: do not add off-topic sections.
- llms.txt is harmless; do not rely on it (the transcript's "OKF" protocol claim is unverified).
