# Plugin Map

- plugin: `makebox-etsy`

## MCP

- `makebox`

## Agents by Group

### etsy

- `makebox-etsy-manager`

## Skills

- `create-etsy-listing`
- `makebox-shop-manager`
- `manage-etsy-orders`
- `manage-etsy-shop`
- `optimize-etsy-listing`
- `research-etsy-market`

## How the parts fit

The remote MakeBox MCP server supplies shop-scoped reads and seller-approved actions. `makebox-etsy-manager` routes multi-step work across the five operational skills in Cowork and Claude Code. Claude chat loads `makebox-shop-manager` as the coordinating skill because it does not run the agent. `references/listing-creation-guide.md` contains the detailed creation, variation, personalization, shipping, returns and media checklist. `references/mcp-tool-guide.md` maps tool names to costs, effects and verification. The agent pack holds supporting context and handoff format. No local executable or credential is bundled.
