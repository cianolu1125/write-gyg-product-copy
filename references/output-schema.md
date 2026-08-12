# Output schema

Create one UTF-8 JSON file with this exact structure. Use empty arrays for inapplicable list sections and empty strings only for genuinely inapplicable scalar fields.

```json
{
  "product_title": "57-60 characters combining top attractions and service USP",
  "short_description": "190-200 characters of persuasive introduction copy in 2-3 sentences.",
  "highlights": [
    "Action-led highlight 1",
    "Action-led highlight 2",
    "Action-led highlight 3",
    "Action-led highlight 4",
    "Action-led highlight 5"
  ],
  "full_description": {
    "stops": [
      {
        "heading": "▼ 07:50 - Departure from Tokyo",
        "details": [],
        "body": "A 200-400-character factual, experiential paragraph."
      },
      {
        "heading": "▼ 10:30 - Hirano Beach at Lake Yamanaka (40 min)",
        "details": [],
        "body": "A 200-400-character factual, experiential paragraph."
      }
    ]
  },
  "includes": [],
  "not_includes": [],
  "what_to_bring": [],
  "not_allowed": [],
  "know_before_you_go": [],
  "voucher_information": [],
  "options": [
    {
      "title": "Scannable differentiator",
      "description": "Material inclusion or difference, followed by an option-specific caution when needed.",
      "includes": [],
      "not_includes": [],
      "meeting_pickup": "Exact customer action and recognition cue.",
      "availability": "Actual activity departure/start time, not pickup-window start."
    }
  ],
  "unresolved_items": [],
  "source_notes": []
}
```

Do not add `opening` or `closing` fields to `full_description`. The departure and return nodes perform those functions in the user's required layout. Do not type `•` into `details`; the Word builder creates real bullet paragraphs.

Keep exact meeting, pickup, arrival, contact, and check-in instructions in `voucher_information`. Keep weather, traffic, cancellation, refund, late/no-show, luggage, accessibility, and other cautionary text in `know_before_you_go`. Do not place those messages in Product Title, Short Description, Highlights, Long Description, or Option Description.

When `options` is non-empty, every option requires a non-placeholder `title`, `description`, and `availability`. Use `meeting_pickup: "Not applicable"` only when the option genuinely has no meeting or pickup instruction. Keep option inclusions/exclusions explicit when they differ.

## Word section order

1. Product Title
2. Short Description
3. Highlights
4. Full Description
5. Includes
6. Not Included
7. What to Bring
8. Not Allowed
9. Know Before You Go
10. Voucher Information
11. Booking Options
12. Validation Summary

Use real Word headings and bullets. Put character counts beside the title, short description, highlights, full description, and stop bodies in the validation summary—not inside customer-facing copy.
