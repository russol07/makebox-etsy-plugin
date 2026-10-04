#!/usr/bin/env python3
"""Build a dated offline reference from MakeBox's official-operation manifest. No network."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def tool_name(operation_id):
    return "etsy_" + re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", operation_id).lower()


def compact(value):
    if isinstance(value, dict):
        return {k: ({name: compact(schema) for name, schema in v.items()}
                    if k in ("properties", "patternProperties", "$defs", "definitions") else compact(v))
                for k, v in value.items() if k not in ("description", "example", "examples")}
    if isinstance(value, list):
        return [compact(v) for v in value]
    return value


def schema_for(op):
    read = op["method"] == "GET" or op["id"] == "tokenScopes"
    params = [p for p in op["params"] if not (
        p["name"] == "shop_id" and (not read or op["scopes"])
        or p["name"] == "user_id" and op["scopes"])]
    props = {p["name"]: compact(p["schema"]) for p in params}
    required = [p["name"] for p in params if p["required"]]
    if op.get("bodySchema") and op["id"] != "tokenScopes":
        props["body"] = compact(op["bodySchema"])
        required.append("body")
    if not read:
        props["confirm"] = {"type": "boolean", "const": True}
        required.append("confirm")
        if op["id"] == "deleteListing":
            props["expected_title"] = {"type": "string"}
            required.append("expected_title")
    return {"type": "object", "properties": props, "required": required, "additionalProperties": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    p.add_argument("--date", required=True, help="Verification date YYYY-MM-DD")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    raw = args.manifest.read_bytes()
    ops = json.loads(raw)
    entries = [{"name": tool_name(op["id"]), "operation": op["id"], "method": op["method"],
                "path": op["path"], "scopes": op["scopes"], "binary_fields": op["binaryFields"],
                "input_schema": schema_for(op)} for op in ops]
    output = {"verified_date": args.date, "source": "MakeBox official Etsy operation manifest",
              "source_sha256": hashlib.sha256(raw).hexdigest(), "operation_count": len(entries),
              "notice": "Offline snapshot; inspect the live MCP schema before execution. No credentials.",
              "tools": entries}
    (root / "references/etsy-tool-schemas.json").write_text(json.dumps(output, indent=2) + "\n")
    lines = ["# Etsy operation index", "", f"Verified {args.date}: {len(entries)} direct tools from MakeBox's Etsy manifest.",
             "Use this index to find the exact named tool, then inspect its live schema. This is not permission to call a tool.",
             "Private shop/user identity is server-bound; public reads may still expose those IDs. The full input snapshot is in [schemas](etsy-tool-schemas.json).",
             "An empty body is still required when shown by the input schema. `token_scopes` handles the token server-side; never supply it.", "",
             "| Tool | Operation / method | Required top-level inputs | Required body fields | Scopes |",
             "| --- | --- | --- | --- | --- |"]
    for e in entries:
        s = e["input_schema"]
        br = s["properties"].get("body", {}).get("required", [])
        lines.append(f"| `{e['name']}` | [{e['operation']}](https://developers.etsy.com/documentation/reference/#operation/{e['operation']}) / {e['method']} | "
                     + ", ".join(f"`{v}`" for v in s["required"]) + " | " + ", ".join(f"`{v}`" for v in br)
                     + " | " + ", ".join(e["scopes"]) + " |")
    lines += ["", "## Known upstream boundaries", "",
              "`etsy_get_listing_property` is documented as under development/501: use `etsy_get_listing_properties`.",
              "`etsy_get_listing_video` may return an empty result: use `etsy_get_listing_videos`.",
              "Inventory/personalization replacement and media uploads require domain checks beyond schema validity.",
              "Readback after accepted writes is mandatory before claiming verified state. No automatic retries of uncertain writes."]
    (root / "references/etsy-operation-index.md").write_text("\n".join(lines) + "\n")
    print(f"Generated {len(entries)} schema/index entries; source sha256 {output['source_sha256'][:12]}")


if __name__ == "__main__":
    main()
