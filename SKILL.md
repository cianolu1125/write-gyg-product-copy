---
name: write-gyg-product-copy
description: Research, create, rewrite, audit, validate, and package high-conversion English GetYourGuide (GYG) product listings from a rough itinerary or detailed tour brief. Use for GYG 产品文案, 行程文案, destination and competitor research, selling-point discovery, traveler-view review, 57-60-character sales-focused titles, 190-200-character short descriptions, exactly five highlights, product-type-aware long descriptions, voucher instructions, know-before-you-go notices, booking options, and polished Word .docx delivery.
---

# Write GYG Product Copy

Turn even a rough itinerary timetable into accurate, differentiated English GYG copy and a validated Word document.

## Read before working

Read these files in order:

1. `references/field-rules.json` — hard limits and counting method.
2. `references/template-evidence.md` — the user's exact DOCX layout.
3. `references/research-workflow.md` — destination, competitor, and selling-point research.
4. `references/input-schema.md` — fact normalization and clarification gates.
5. `references/traveler-completeness-check.md` — traveler-view audit and option requirements.
6. `references/content-zoning.md` — purpose, tone, and permitted content for every field.
7. `references/gyg-copy-rules.md` — conversion and field-writing rules.
8. `references/output-schema.md` — final JSON and Word structure.

Do not rely on remembered rules when these files are available.

## Mandatory preflight plus five-stage workflow

### 0. Audit the submitted product before any research or copywriting

Read the submission as a first-time traveler. Classify the product as `day_tour`, `ticket`, or `experience`; determine whether options exist or may be needed; and check whether the facts are sufficient to write every later field. Use `references/traveler-completeness-check.md` and ask one consolidated, prioritized question set covering every material ambiguity. Do not ask piecemeal follow-ups that could have been identified in this audit. Start research and drafting only after all critical answers are resolved and record the preflight as `PASS`.

### 1. Research the confirmed itinerary

Normalize all supplied facts and separate `confirmed`, `researched_context`, `approved_default`, `unknown`, and `conflict`. Browse authoritative destination sources and current same-place GYG competitors. Save the destination knowledge base and competitor scan required by `references/research-workflow.md`. Never convert competitor claims into this product's inclusions.

### 2. Build and rank the selling points

Rank attractions first by traveler recognition, popularity, visual appeal, and purchase influence. Then rank soft-service differentiators such as small-group comfort, hotel pickup, route efficiency, special access, expertise, inclusions, or reduced planning. Convert route facts into customer value and map each selling point to a field. The title must combine as many top-ranked attraction and service highlights as clarity allows.

### 3. Write the first draft to GYG limits and format

Draft Long Description, five Highlights, Short Description, Product Title, operational sections, then Options. For `day_tour`, use chronological itinerary nodes. For `ticket` or `experience`, replace the timeline with distinct selling-point sections describing access, content, participation, atmosphere, benefits, and verified inclusions. Follow the exact layout and hard limits. Use original, introduction-style, high-conversion language in every Description field. Keep disclaimers and travel execution instructions out of promotional copy.

### 4. Review the draft as a traveler

Run `references/traveler-completeness-check.md`. Judge whether a first-time visitor understands why to book, what each stop adds, what the options change, and whether any important expectation is missing. Ask a small prioritized question set when missing facts affect the purchase or trip. Do not hide uncertainty in polished prose.

### 5. Polish each field for its specific purpose

Apply the tone and content boundaries in `references/content-zoning.md`. Strengthen attraction and service value in sales fields; move participation instructions to Voucher Information; move disclaimers and cautions to Know Before You Go. Then validate JSON, generate the Word document, read it back, and deliver only after `PASS`.

## Non-negotiable rules

- Count visible characters including spaces and punctuation; exclude layout line breaks.
- Enforce Product Title 57-60 and Short Description 190-200.
- Integrate top-ranked attraction highlights and the strongest verified service differentiator into the title whenever they fit clearly.
- Produce exactly five 75-80-character highlights, each starting with an action verb.
- Use chronological `▼` nodes only for `day_tour`. Use non-time-based `▼` selling-point sections for `ticket` and `experience`. Keep every section body within 200-400 characters and the complete Long Description within 2,000-2,300.
- Keep Option titles short, precise, appealing, parallel, and instantly distinguishable from one another.
- Enforce every Option Description at 180-200 characters: state the exact option content and difference first, then finish with an appealing purchase motivation.
- Use real Word bullets; never type bullet glyphs into JSON.
- Avoid number ambiguity in titles: do not let a stop count look like a group-size claim.
- Keep all Description fields vivid, persuasive, guest-centered, and introduction-like.
- Put trip participation instructions only in Voucher Information.
- Put disclaimers, restrictions, and cautionary notes only in Know Before You Go, except an option-specific eligibility condition needed to choose that option.
- Keep Know Before You Go polite, tactful, and unambiguous.
- Mention email or WhatsApp generically when relevant; omit addresses and phone numbers.
- Never use unresolved placeholders or unsupported claims.

## Rule priority

1. Current-task facts and explicit user instructions.
2. User house rules and referenced-conversation preferences encoded in this Skill.
3. Current official GYG supplier guidance.
4. Destination research and marketplace patterns.

Marketplace patterns inform positioning; they do not prove conversion causality. Never claim that copy alone guarantees sales.

## Completion standard

Report `PASS` only when research, selling-point analysis, traveler completeness, all hard limits, cross-field consistency, and DOCX structural read-back are complete, with no critical unknowns hidden in polished prose.
