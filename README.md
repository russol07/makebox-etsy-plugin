# MakeBox for Etsy

![MakeBox AI icon](assets/makebox-logo.png)

MakeBox connects Claude to Etsy through the seller's authorized MakeBox workspace. Claude interprets the seller's request and prepares the values; the remote MCP server passes approved requests to Etsy and returns Etsy's response. Direct Etsy calls do not invoke another MakeBox model or spend MakeBox AI allowances.

Version 0.2.0 adds guidance for the direct `etsy_*` tools. The server exposes adapters for all 105 operations in Etsy's official API snapshot dated October 1, 2026, alongside the existing MakeBox workflow tools. This covers the published API, not every feature of Etsy's website. Availability depends on Etsy permissions, app access, valid product data, and the seller's MakeBox plan.

## Connect and use

Install the plugin in Claude, then connect **MakeBox** through OAuth. Use `list_shops` and `get_account_status` to identify the selected workspace and access. Private actions are bound to the seller's connected shop. Public Etsy research can read other shops. MCP listing management requires an eligible MakeBox plan; Etsy's normal fees may apply to the requested action.

Try “change this listing's shipping profile,” “create an Etsy draft from this finished copy,” “show my latest orders and payment ledger,” or “research relevant keywords.” Claude uses the live tool schemas rather than a fixed list embedded in the plugin. If an existing conversation lacks newly added tools, refresh the connector or start a new conversation; discovery and caching depend on the client.

A direct `etsy_*` action uses Etsy IDs and does not require a MakeBox import first. Writes need authorization for the exact target and values. A successful HTTP response is separate from a fresh readback proving the final state. Existing MakeBox draft, research, optimization and bulk-job tools remain available when those workflows are requested. Image and video generation are not provided by this MCP connector; existing files can be uploaded and managed.

## Data and support

The connector sends the selected tool request to MakeBox at `https://mcp.makebox.ai/mcp`, which calls Etsy with the seller's OAuth authorization. Direct operations may include listing content, order and buyer details, shipping information, payment records and shop policies. Display only the data needed for the seller's task. Optional personal Etsy email/address methods require additional Etsy consent; the ordinary connection does not gain these permissions automatically.

The plugin contains no credentials, local executable, or autonomous background worker. Its skills guide the host to use the connected tools. Seller-owned files are uploaded only with permission through `get_upload_link` or the Asset Library; direct multipart fields use the resulting `asset_id`. Never share OAuth tokens or arbitrary server paths.

See [MakeBox](https://www.makebox.ai/), the [privacy policy](https://www.makebox.ai/privacy), and [support](mailto:support@makebox.ai).

## Components

- `agents/makebox-etsy-manager.md`: coordinates work in Cowork and Claude Code.
- `skills/makebox-shop-manager/SKILL.md`: the coordinating role in ordinary Claude chat.
- `skills/use-etsy-api/SKILL.md`: direct API discovery, authorization, transport and readback.
- `skills/create-etsy-listing/SKILL.md`: complete listing drafts, options, policies and media.
- `skills/optimize-etsy-listing/SKILL.md`: chat-authored improvements or explicitly requested MakeBox AI jobs.
- `skills/manage-etsy-orders/SKILL.md`: current orders, transactions, payment records and authorized fulfillment.
- `skills/research-etsy-market/SKILL.md`: public Etsy observations and MakeBox keyword evidence.
- `skills/manage-etsy-shop/SKILL.md`: shipping, returns, sections, processing and shop settings.
- `references/direct-etsy-api-guide.md`: the direct connector contract and examples.
- `.mcp.json`: the remote server URL; server code and credentials are not bundled.

Claude chat uses the skills and connector but does not run plugin sub-agents. Cowork and Claude Code can use the manager agent. Remote tool updates come from the MCP server; skill/agent changes require an updated plugin version. See [CHANGELOG.md](CHANGELOG.md).
