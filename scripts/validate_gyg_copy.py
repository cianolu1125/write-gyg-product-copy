#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parent.parent / "references" / "field-rules.json"
RULES = json.loads(RULES_PATH.read_text(encoding="utf-8"))
HARD = RULES["hard_limits"]
RECOMMENDED = RULES["recommended_limits"]

ACTION_VERBS = {
    "admire", "capture", "cruise", "discover", "enjoy", "experience", "explore",
    "get", "have", "learn", "marvel", "ride", "savor", "see", "step", "stop",
    "take", "taste", "travel", "uncover", "visit", "watch"
}
TITLE_BANNED = {"amazing", "best", "unforgettable"}
CONTACT_RE = re.compile(r"(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\+?\d[\d ()-]{7,}\d)")
PLACEHOLDER_RE = re.compile(r"(?:\bTBD\b|\bXXX\b|\{[^{}]+\}|\[(?:insert|add|confirm|tbd)[^\]]*\])", re.I)
HEADING_RE = re.compile(r"^▼\s+.+$")
AMBIGUOUS_TITLE_COUNT_RE = re.compile(r"\b\d+\s+(?:spots?|highlights?)\s+(?:small[- ]group|group)\b", re.I)
GENERIC_OPTION_TITLE_RE = re.compile(r"^(?:option\s*\d*|standard|basic|premium)$", re.I)
DISCLAIMER_RE = re.compile(
    r"(?:cannot be guaranteed|non[- ]refundable|no[- ]shows?|late arrivals?|"
    r"refunds?|cancellations?|subject to (?:weather|traffic)|"
    r"(?:schedule|route|itinerary|order of stops).{0,35}(?:may|can).{0,20}(?:change|vary|adjust)|"
    r"(?:weather|traffic) conditions.{0,35}(?:change|vary|adjust|affect))",
    re.I,
)
TRAVEL_INSTRUCTION_RE = re.compile(
    r"(?:meet at|arrive (?:at least )?\d+ minutes|hotel lobby|"
    r"check (?:your )?(?:spam|junk)|keep (?:your )?phone|phone (?:reachable|accessible)|"
    r"(?:driver|vehicle|pickup) details.{0,40}(?:email|whatsapp)|"
    r"via (?:email|whatsapp|email or whatsapp).{0,35}(?:day before|before departure))",
    re.I,
)


def visible_length(value):
    """Count visible characters, including spaces/punctuation but excluding CR/LF."""
    return len(re.sub(r"[\r\n]", "", str(value or "").strip()))


def sentence_count(text):
    text = str(text or "").strip()
    return len([x for x in re.split(r"(?<=[.!?])\s+", text) if x]) if text else 0


def full_text(data):
    parts = []
    for stop in data.get("full_description", {}).get("stops", []):
        parts.append(str(stop.get("heading", "")).strip())
        parts.extend(str(x).strip() for x in stop.get("details", []) if str(x).strip())
        parts.append(str(stop.get("body", "")).strip())
    return "\n".join(x for x in parts if x)


def iter_string_values(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from iter_string_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_string_values(child)
    elif isinstance(value, str):
        yield value


def check_range(errors, label, value, rule):
    count = visible_length(value)
    if count < rule["min"] or count > rule["max"]:
        errors.append(f"{label} is {count} characters; required range is {rule['min']}-{rule['max']}.")
    return count


def recommend_range(warnings, label, value, rule_name):
    if not str(value or "").strip():
        return
    rule = RECOMMENDED[rule_name]
    count = visible_length(value)
    if not rule["min"] <= count <= rule["max"]:
        warnings.append(f"{label} is {count} characters; recommended range is {rule['min']}-{rule['max']} (do not pad).")


def validate(data):
    errors, warnings = [], []
    title = str(data.get("product_title", "")).strip()
    short = str(data.get("short_description", "")).strip()
    highlights = data.get("highlights", [])
    full = full_text(data)

    title_count = check_range(errors, "Product title", title, HARD["product_title"])
    if ":" not in title:
        warnings.append("Product title should normally use 'Location: Activity + USP'.")
    if AMBIGUOUS_TITLE_COUNT_RE.search(title):
        errors.append("Product title places a stop/highlight count beside a group label, creating group-size ambiguity.")
    for word in TITLE_BANNED:
        if re.search(rf"\b{re.escape(word)}\b", title.lower()):
            errors.append(f"Product title contains unsupported subjective word: {word}.")

    short_count = check_range(errors, "Short description", short, HARD["short_description"])
    sc = sentence_count(short)
    short_rule = HARD["short_description"]
    if not short_rule["sentences_min"] <= sc <= short_rule["sentences_max"]:
        errors.append(
            f"Short description has {sc} sentence(s); required range is "
            f"{short_rule['sentences_min']}-{short_rule['sentences_max']}."
        )

    highlight_counts = []
    h_rule = HARD["highlights"]
    if not isinstance(highlights, list) or len(highlights) != h_rule["count"]:
        errors.append(f"Exactly {h_rule['count']} highlights are required.")
    else:
        normalized = []
        for i, item in enumerate(highlights, 1):
            item = str(item).strip()
            count = visible_length(item)
            highlight_counts.append(count)
            if not h_rule["min_each"] <= count <= h_rule["max_each"]:
                errors.append(
                    f"Highlight {i} is {count} characters; required range is "
                    f"{h_rule['min_each']}-{h_rule['max_each']}."
                )
            words = item.split()
            first = re.sub(r"[^A-Za-z'-]", "", words[0]).lower() if words else ""
            if first not in ACTION_VERBS:
                errors.append(f"Highlight {i} must start with an action verb; found '{words[0] if words else ''}'.")
            normalized.append(re.sub(r"\W+", " ", item.lower()).strip())
        if len(set(normalized)) != len(normalized):
            errors.append("Highlights contain an exact duplicate.")

    full_count = check_range(errors, "Full description", full, HARD["full_description"])
    full_obj = data.get("full_description", {})
    if "opening" in full_obj or "closing" in full_obj:
        errors.append("Full description must not contain standalone opening or closing fields; use departure and return nodes.")
    stops = full_obj.get("stops", [])
    stop_counts = []
    if not isinstance(stops, list) or not stops:
        errors.append("At least one full-description stop is required.")
    else:
        opening_keys = []
        for i, stop in enumerate(stops, 1):
            heading = str(stop.get("heading", "")).strip()
            body = str(stop.get("body", "")).strip()
            details = stop.get("details", [])
            if not heading or not body:
                errors.append(f"Stop {i} requires both heading and body.")
            if heading and ("\n" in heading or "\r" in heading or not HEADING_RE.fullmatch(heading)):
                errors.append(f"Stop {i} heading must be one line beginning with '▼ '.")
            if not isinstance(details, list):
                errors.append(f"Stop {i} details must be an array.")
            else:
                for j, detail in enumerate(details, 1):
                    detail = str(detail).strip()
                    if not detail:
                        errors.append(f"Stop {i} detail {j} is empty.")
                    if detail.startswith(("•", "-", "*")):
                        errors.append(f"Stop {i} detail {j} must not include a typed bullet marker.")
            count = visible_length(body)
            stop_counts.append(count)
            opening_key = " ".join(re.findall(r"[A-Za-z']+", body.lower())[:3])
            if opening_key:
                opening_keys.append((i, opening_key))
            stop_rule = HARD["stop_body"]
            if not stop_rule["min"] <= count <= stop_rule["max"]:
                errors.append(
                    f"Stop {i} body is {count} characters; required range is "
                    f"{stop_rule['min']}-{stop_rule['max']}."
                )
        seen_openings = {}
        for index, opening_key in opening_keys:
            if opening_key in seen_openings:
                errors.append(
                    f"Stops {seen_openings[opening_key]} and {index} repeat the same opening phrase "
                    f"'{opening_key}'; vary each itinerary-node opening."
                )
            else:
                seen_openings[opening_key] = index

    if short and full and short.lower() in full.lower():
        errors.append("Short description is copied verbatim into the full description; rewrite it independently.")

    promotional_fields = [("Product title", title), ("Short description", short)]
    promotional_fields.extend((f"Highlight {i}", str(item)) for i, item in enumerate(highlights, 1))
    for i, stop in enumerate(stops, 1):
        promotional_fields.append((f"Stop {i} heading", str(stop.get("heading", ""))))
        promotional_fields.append((f"Stop {i} body", str(stop.get("body", ""))))
        promotional_fields.extend(
            (f"Stop {i} detail {j}", str(detail))
            for j, detail in enumerate(stop.get("details", []), 1)
        )
    for i, option in enumerate(data.get("options", []), 1):
        if isinstance(option, dict):
            promotional_fields.append((f"Option {i} title", str(option.get("title", ""))))
            promotional_fields.append((f"Option {i} description", str(option.get("description", ""))))
    for label, value in promotional_fields:
        if DISCLAIMER_RE.search(value):
            errors.append(f"{label} contains disclaimer/caution text; move it to Know Before You Go.")
        if TRAVEL_INSTRUCTION_RE.search(value):
            errors.append(f"{label} contains trip participation instructions; move them to Voucher Information.")

    for key in ("includes", "not_includes"):
        for i, item in enumerate(data.get(key, []), 1):
            recommend_range(warnings, f"{key} item {i}", item, "include_exclude_item")
    for i, item in enumerate(data.get("know_before_you_go", []), 1):
        recommend_range(warnings, f"Know Before You Go item {i}", item, "know_before_you_go_item")
    for i, item in enumerate(data.get("voucher_information", []), 1):
        recommend_range(warnings, f"Voucher Information item {i}", item, "voucher_information_item")
    if not data.get("voucher_information"):
        errors.append("Voucher Information requires post-booking trip participation instructions.")
    for i, option in enumerate(data.get("options", []), 1):
        if not isinstance(option, dict):
            errors.append(f"Option {i} must be an object.")
            continue
        option_title = str(option.get("title", "")).strip()
        option_description = str(option.get("description", "")).strip()
        meeting_pickup = str(option.get("meeting_pickup", "")).strip()
        availability = str(option.get("availability", "")).strip()
        if not option_title:
            errors.append(f"Option {i} title is required.")
        elif GENERIC_OPTION_TITLE_RE.fullmatch(option_title):
            errors.append(f"Option {i} title must state a concrete differentiator, not '{option_title}'.")
        if not option_description:
            errors.append(f"Option {i} description is required.")
        if not meeting_pickup:
            errors.append(f"Option {i} meeting/pickup is required; use 'Not applicable' only when true.")
        if not availability:
            errors.append(f"Option {i} availability is required and must state the actual activity start/departure time.")
        for key in ("includes", "not_includes"):
            if key in option and not isinstance(option[key], list):
                errors.append(f"Option {i} {key} must be an array.")
        recommend_range(warnings, f"Option {i} title", option_title, "option_title")
        recommend_range(warnings, f"Option {i} description", option_description, "option_description")
        if meeting_pickup.lower() != "not applicable":
            recommend_range(warnings, f"Option {i} meeting/pickup", meeting_pickup, "meeting_pickup")
        recommend_range(warnings, f"Option {i} availability", availability, "availability")

    serialized = json.dumps(data, ensure_ascii=False)
    if CONTACT_RE.search(serialized):
        errors.append("Specific email address or phone number detected; use only generic email/WhatsApp wording.")
    if any(PLACEHOLDER_RE.search(value) for value in iter_string_values(data)):
        errors.append("Unresolved placeholder text detected.")
    if data.get("unresolved_items"):
        errors.append("Unresolved items remain; resolve them before final delivery.")

    return errors, warnings, {
        "product_title": title_count,
        "short_description": short_count,
        "highlights": highlight_counts,
        "full_description": full_count,
        "stop_bodies": stop_counts,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate structured GYG product copy.")
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    data = json.loads(args.json_file.read_text(encoding="utf-8-sig"))
    errors, warnings, counts = validate(data)
    report = {"status": "PASS" if not errors else "FAIL", "counts": counts, "errors": errors, "warnings": warnings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
