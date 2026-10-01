# Plugin Map

- Plugin: `makebox-etsy`
- Version: `0.2.0`
- Remote MCP: `makebox` → `https://mcp.makebox.ai/mcp`

## Agent and skills

The `makebox-etsy-manager` agent coordinates six operational skills in Cowork and Claude Code:

- `use-etsy-api`
- `create-etsy-listing`
- `optimize-etsy-listing`
- `manage-etsy-orders`
- `research-etsy-market`
- `manage-etsy-shop`

The seventh skill, `makebox-shop-manager`, provides the coordinating role in ordinary Claude chat, where plugin sub-agents do not run.

## Shared references

- `direct-etsy-api-guide.md`: live discovery, direct requests, identity, authorization, media and readback.
- `mcp-tool-guide.md`: when to use direct Etsy transport versus optional MakeBox workflows.
- `listing-creation-guide.md`: complete draft, inventory, personalization, policy/media and publication sequence.
- `agent-packs/etsy/makebox-etsy-manager/`: role context, domain notes, checklist and handoff format.

The remote server supplies the current tool schemas and implementation. This package does not embed that server, duplicate the 105-operation implementation, bundle credentials or create a background worker.
