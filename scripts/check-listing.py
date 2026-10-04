#!/usr/bin/env python3
"""Offline structural QA for a copy/settings packet. No network, writes or paid actions.

This cannot verify product truth, IP rights, Etsy status or SEO performance.
"""
import argparse
import json
import math
import re
import unicodedata
from pathlib import Path


def check(packet, mode="generated"):
    errors, warnings = [], []
    title, description, tags = packet.get("title"), packet.get("description"), packet.get("tags")
    for key, value in (("title", title), ("description", description)):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key}: nonempty text required")
        elif re.search(r"\[(?:TBD|TODO|SIZE|MATERIAL|PRICE|SHIPPING|INSERT[^\]]*)\]|\bTBD\b", value, re.I):
            errors.append(f"{key}: unresolved placeholder in copy-ready text")
    if isinstance(title, str):
        if len(title) > 140:
            errors.append(f"title: {len(title)} characters exceeds 140")
        if len(title.split()) >= 15:
            warnings.append("title: review readability; under 15 words is guidance, not a native rejection rule")
        if any(not (unicodedata.category(c).startswith(("L", "P")) or unicodedata.category(c) in ("Nd", "Sm", "Zs")
                    or c in "™©®") for c in title):
            errors.append("title: unsupported decorative symbol or control character")
        if any(title.count(c) > 1 for c in "%:&+"):
            errors.append("title: %, :, & and + may each occur only once in current Etsy API titles")
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        errors.append("tags: array of strings required")
        tags = []
    else:
        if len(tags) > 13 or (mode == "generated" and len(tags) != 13):
            errors.append(f"tags: received {len(tags)}; generated sets require 13, native sets allow at most 13")
        seen = set()
        for i, tag in enumerate(tags, 1):
            normalized = " ".join(unicodedata.normalize("NFKC", tag).casefold().split())
            if not normalized or len(tag) > 20:
                errors.append(f"tag {i}: empty or exceeds 20 characters ({len(tag)})")
            if normalized in seen:
                errors.append(f"tag {i}: duplicate phrase")
            seen.add(normalized)
            if mode == "generated" and packet.get("space_delimited_language", True) and len(normalized.split()) < 2:
                errors.append(f"tag {i}: generated set needs a relevant multi-word phrase in this language")
    kind = packet.get("type")
    if kind not in ("physical", "download", "custom-digital"):
        errors.append("type: physical, download or custom-digital required for packet QA")
    if kind in ("download", "custom-digital"):
        if packet.get("variants"):
            errors.append("digital: ordinary product variations are not supported")
        if packet.get("shipping"):
            errors.append("digital: physical shipping configuration conflicts with product type")
        if not packet.get("digital_contents"):
            warnings.append("digital: actual file contents/access/software/license still need review")
    for label in ("price", "quantity"):
        if label not in packet:
            warnings.append(f"{label}: missing; copy draft is not an executable complete creation payload")
        else:
            value = packet[label]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                errors.append(f"{label}: positive finite number required for new listing")
            elif label == "quantity" and not isinstance(value, int):
                errors.append("quantity: integer required")
    package = packet.get("package")
    if isinstance(package, dict):
        if package.get("measurement_status") != "confirmed":
            warnings.append("package: estimates cannot be sent as confirmed shipping measurements")
        if any(key in package for key in ("length", "width", "height")):
            if not all(key in package for key in ("length", "width", "height", "dimensions_unit")):
                errors.append("package: all dimensions and their unit are required together")
        if "weight" in package and "weight_unit" not in package:
            errors.append("package: weight unit required")
        for key in ("length", "width", "height", "weight"):
            if key in package and (isinstance(package[key], bool) or not isinstance(package[key], (int, float))
                                   or not math.isfinite(package[key]) or package[key] <= 0):
                errors.append(f"package.{key}: positive finite number required")
    for fact in packet.get("facts", []):
        if isinstance(fact, dict) and fact.get("status") in ("missing", "conflicting"):
            warnings.append(f"fact {fact.get('name', 'unnamed')}: {fact['status']}; resolve or omit claim")
    if packet.get("blockers"):
        warnings.append("publication blockers remain; do not label the listing ready to publish")
    questions = packet.get("personalization", [])
    if not isinstance(questions, list):
        errors.append("personalization: question array required")
    else:
        if len(questions) > 5:
            errors.append("personalization: maximum five questions")
        uploads = 0
        for i, question in enumerate(questions, 1):
            if not isinstance(question, dict):
                errors.append(f"question {i}: object required")
                continue
            text, qt = question.get("question_text", ""), question.get("question_type")
            if not isinstance(text, str) or not 1 <= len(text) <= 45:
                errors.append(f"question {i}: title must be 1–45 characters")
            instructions = question.get("instructions")
            if instructions is not None and (not isinstance(instructions, str) or len(instructions) > 120):
                errors.append(f"question {i}: instructions must be at most120 characters")
            if not isinstance(question.get("required"), bool):
                errors.append(f"question {i}: required must be a boolean")
            if qt == "text_input":
                limit = question.get("max_allowed_characters")
                cap = 256 if packet.get("personalization_route") == "local" else 1024
                if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= cap:
                    errors.append(f"question {i}: text limit must be 1–{cap} on chosen route")
            elif qt in ("dropdown", "labeled_upload", "unlabeled_upload"):
                if qt != "dropdown":
                    uploads += 1
                    count = question.get("max_allowed_files")
                    if isinstance(count, bool) or not isinstance(count, int) or not (2 if qt == "labeled_upload" else 1) <= count <= 10:
                        errors.append(f"question {i}: invalid upload count")
                if qt in ("dropdown", "labeled_upload"):
                    options = question.get("options")
                    labels = [o.get("label") if isinstance(o, dict) else None for o in options] if isinstance(options, list) else []
                    max_label = 20 if qt == "dropdown" else 45
                    valid_labels = all(isinstance(v, str) and 1 <= len(v) <= max_label for v in labels)
                    if not labels or not valid_labels or (valid_labels and len(set(labels)) != len(labels)):
                        errors.append(f"question {i}: unique valid option labels required")
                    if qt == "dropdown" and (len(labels) > 30 or instructions not in (None, "")):
                        errors.append(f"question {i}: dropdown max30 options and no instructions")
                    if qt == "labeled_upload" and len(labels) != question.get("max_allowed_files"):
                        errors.append(f"question {i}: labelled upload count must match labels")
            else:
                errors.append(f"question {i}: unsupported question_type")
        if uploads > 1:
            errors.append("personalization: at most one upload-type question")
    return {"structural_valid": not errors, "mode": mode, "errors": errors, "warnings": warnings,
            "title_characters": len(title) if isinstance(title, str) else None,
            "tag_count": len(tags), "tag_lengths": [len(t) for t in tags],
            "notice": "Structural QA only. Manually verify facts, relevance, settings and actual Etsy state."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("packet", type=Path)
    p.add_argument("--mode", choices=("generated", "native"), default="generated")
    args = p.parse_args()
    result = check(json.loads(args.packet.read_text()), args.mode)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["structural_valid"] else 1)


if __name__ == "__main__":
    main()
