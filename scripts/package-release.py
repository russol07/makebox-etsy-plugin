#!/usr/bin/env python3
"""Build Claude/Codex connected and standalone archives without credentials or network."""
import argparse
import json
import shutil
import zipfile
from pathlib import Path

PARTS = ("README.md", "CHANGELOG.md", "LICENSE", "ОПИС-УКРАЇНСЬКОЮ.md", "assets", "agents",
         "agent-packs", "skills", "references", "templates", "checklists", "examples", "scripts", "tests")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--codex-manifest", type=Path, required=True, help="Existing public metadata manifest, not reviewer credentials")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
    codex = json.loads(args.codex_manifest.read_text())
    version = claude["version"]
    args.output.mkdir(parents=True, exist_ok=True)
    for runtime in ("claude", "codex"):
        for mode in ("connected", "standalone"):
            label = f"makebox-etsy-{runtime}-{mode}-{version}"
            stage = args.output / label
            if stage.exists():
                raise SystemExit(f"Refusing to overwrite existing package stage: {stage}")
            package = stage / "makebox-etsy"
            package.mkdir(parents=True)
            for part in PARTS:
                source = root / part
                if source.is_dir():
                    shutil.copytree(source, package / part, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                else:
                    shutil.copy2(source, package / part)
            config = json.loads((root / ".mcp.json").read_text()) if mode == "connected" else {"mcpServers": {}}
            (package / ".mcp.json").write_text(json.dumps(config, indent=2) + "\n")
            metadata = json.loads(json.dumps(claude if runtime == "claude" else codex))
            metadata["version"] = version
            metadata["description"] = claude["description"]
            if mode == "standalone":
                metadata["name"] = "makebox-etsy-standalone"
            if runtime == "claude":
                if mode == "standalone":
                    metadata["displayName"] = "MakeBox for Etsy — Standalone"
                folder = ".claude-plugin"
            else:
                folder = ".codex-plugin"
                interface = metadata.setdefault("interface", {})
                interface["shortDescription"] = "Create better Etsy listings"
                interface["longDescription"] = (
                    "An Etsy SEO strategist for complete copy-ready listings, factual audits, keyword evidence, "
                    "options, personalization, shipping/packaging and digital contents. Works from pasted text, photos "
                    "or CSVs without a connector. The coordinating skill carries the expert role. "
                    + ("The optional MakeBox MCP connection adds live Etsy reads and exactly authorized operations, with authoritative readback. "
                       if mode == "connected" else "This standalone package includes no MCP connection or live shop access. ")
                    + "It does not guarantee rank or sales, and the connector does not generate images or video.")
                interface["defaultPrompt"] = ["Create a complete Etsy listing from these product facts.",
                                              "Improve this pasted listing without losing specifications.",
                                              "Analyze my keyword CSV and explain which phrases fit my product."]
                ext = metadata.setdefault("extensions", {}).setdefault("com.openai", {})
                ext["onboardingSkill"] = "./skills/makebox-shop-manager/SKILL.md"
                ext.setdefault("publication", {})["release_notes"] = f"Version {version}: detailed Etsy strategist role, seven workflows, 1024-character personalization, fixed optional-text fees and verified direct Etsy execution."
                if mode == "connected":
                    metadata["mcpServers"] = "./.mcp.json"
                    review = ext.get("review", {})
                    for case in review.get("test_cases", {}).get("positive", []):
                        if "optimize_listing" in case.get("tools_triggered", ""):
                            case["tools_triggered"] = "list_listings, get_listing"
                            case["expected_behavior"] = "Read this seller's listing and prepare an original chat-authored proposal. No paid internal generation and no Etsy write."
                else:
                    metadata.pop("mcpServers", None)
                    ext.pop("review", None)
                    interface["displayName"] = "MakeBox for Etsy — Standalone"
                    interface["capabilities"] = ["Prepare complete listing copy", "Audit pasted listings", "Analyze supplied keyword evidence", "Plan product settings"]
            (package / folder).mkdir()
            (package / folder / "plugin.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
            with zipfile.ZipFile(args.output / f"{label}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
                for file in sorted(package.rglob("*")):
                    if file.is_file():
                        archive.write(file, file.relative_to(stage))
            print(args.output / f"{label}.zip")


if __name__ == "__main__":
    main()
