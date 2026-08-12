# GYG source input schema

Use this checklist to normalize the user's source material. Accept prose, tables, or existing documents, but map them to these fields before writing.

## Required facts

- Product type: day tour, ticket, or experience
- Whether options exist, do not exist, or require clarification
- Product language and departure city or activity location
- Activity category and core experience
- Total duration or validity
- Every included attraction or experience
- Ordered itinerary, including known times and stop durations
- Transport mode
- Group type and maximum size, if advertised
- Guide, host, driver, instructor, or audio-guide role and languages
- Included and excluded items
- Pickup or meeting-point arrangement
- Drop-off arrangement
- Option differences
- Operational restrictions and customer requirements
- Weather, traffic, access, age, luggage, mobility, and cancellation facts when applicable

## Fact status

Label each item internally as one of:

- `confirmed`: explicitly supplied by the user or source document
- `approved_default`: a reusable instruction explicitly approved by the user
- `unknown`: not supplied and not safe to infer
- `conflict`: two supplied facts disagree

Only `confirmed` and `approved_default` facts may appear as claims. Keep `unknown` items out of customer-facing copy or ask for them when essential. Resolve `conflict` items before finalization.

`researched_context` may support stable descriptions of a destination but may not establish this product's inclusions, access, route, service level, pickup, group size, language, or policies.

## High-impact questions

Ask only questions that change what a customer buys or expects, including:

- Is an entry ticket, meal, tasting, activity, or transport included?
- Is the experience shared, small-group, or private, and what is the cap?
- Is pickup included, optional, area-limited, or a separate option?
- Does the activity return to the same city or meeting point?
- Which stops are visits versus photo stops, pass-bys, or optional extras?
- Which languages are actually available for the selected option?
- Which cancellation, weather, or no-show policy is authoritative?
- For every option, what material feature changes and which timing, pickup, inclusion, eligibility, or minimum-booking rule applies?

## Reusable blank form

```text
Product/location:
Product type (day tour / ticket / experience):
Options status (present / none / unclear):
Category:
Duration:
Core promise:
Group type and cap:
Guide/driver/instructor and languages:
Transport:

Pickup/meeting point:
Pickup window:
Actual activity start time:
Drop-off/return:

Itinerary stop 1:
- Time:
- Place/activity:
- Duration:
- Departure service benefit for sales copy (for example, optional pickup; no exact instructions):
- What guests do/see:
- Included/optional/pass-by:
- Distinctive benefit:

Inclusions:
Exclusions:
What to bring:
Not allowed:
Know before you go:

Options and exact differences:
- Option title/value:
- Option-specific inclusions/exclusions:
- Option-specific minimum booking or eligibility:
- Option-specific meeting/pickup:
- Option-specific actual departure time:
Availability notes:
Voucher instructions:
- Exact meeting point and recognition cue:
- Pickup window and waiting location:
- Required arrival lead time:
- Confirmation/contact timing:
```
