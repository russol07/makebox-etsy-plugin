#!/usr/bin/env python3
"""Validate local links, skill manifests, tool names and API fixtures. No network or tool calls.

Needs PyYAML and jsonschema. Optionally compares with an export of the actual local
MakeBox runtime schemas. It does not certify model behavior or marketplace approval.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import jsonschema
import yaml


def without_descriptions(value):
    if isinstance(value, dict):
        return {k: ({name: without_descriptions(schema) for name, schema in v.items()}
                    if k in ("properties", "patternProperties", "$defs", "definitions") else without_descriptions(v))
                for k, v in value.items() if k not in ("description", "example", "examples")}
    if isinstance(value, list):
        return [without_descriptions(v) for v in value]
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime-schemas", type=Path)
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    failures, links = [], 0
    snapshot = json.loads((root / "references/etsy-tool-schemas.json").read_text())
    tools = {t["name"]: t["input_schema"] for t in snapshot["tools"]}
    assert len(tools) == snapshot["operation_count"] == 105, "Expected distinct 105-operation snapshot"
    for md in root.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text()
        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = match.group(1).split("#")[0].strip("<>")
            if not target or ":" in target:
                continue
            links += 1
            if not (md.parent / unquote(target)).exists():
                failures.append(f"Broken link: {md.relative_to(root)} → {target}")
        for name in set(re.findall(r"\betsy_[a-z0-9_]+\b", text)):
            if name not in tools:
                failures.append(f"Unknown direct tool: {md.relative_to(root)} → {name}")
    skills = list((root / "skills").glob("*/SKILL.md"))
    for file in skills:
        match = re.match(r"^---\n(.*?)\n---\n", file.read_text(), re.S)
        if not match:
            failures.append(f"Missing frontmatter: {file}")
            continue
        meta = yaml.safe_load(match.group(1))
        if meta.get("name") != file.parent.name or not meta.get("description"):
            failures.append(f"Invalid skill identity: {file}")
    agent = yaml.safe_load((root / "agents/makebox-etsy-manager.md").read_text().split("---", 2)[1])
    for skill in agent.get("skills", []):
        if not (root / "skills" / skill / "SKILL.md").exists():
            failures.append(f"Missing agent skill: {skill}")
    fixtures = json.loads((root / "examples/api-examples.json").read_text())["examples"]
    for i, fixture in enumerate(fixtures, 1):
        try:
            jsonschema.validate(fixture["arguments"], tools[fixture["tool"]])
        except (jsonschema.ValidationError, KeyError) as error:
            failures.append(f"API fixture {i} {fixture['tool']}: {getattr(error, 'message', str(error))}")
    if args.runtime_schemas:
        runtime = {t["name"]: without_descriptions(t["input_schema"]) for t in json.loads(args.runtime_schemas.read_text())}
        if runtime != tools:
            different = sorted(k for k in set(runtime) | set(tools) if runtime.get(k) != tools.get(k))
            failures.append(f"Runtime schema mismatch: {different}")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    result = subprocess.run([sys.executable, str(root / "tests/test-listing-qa.py")], cwd=root)
    if result.returncode:
        raise SystemExit(result.returncode)
    print(f"PASS: {len(skills)} skill identities, agent links, {links} local links, 105 tool schemas, {len(fixtures)} API fixtures"
          + (", exact local runtime schema parity" if args.runtime_schemas else ""))


if __name__ == "__main__":
    main()
