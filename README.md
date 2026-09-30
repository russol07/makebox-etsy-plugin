# MakeBox for Etsy

![MakeBox AI icon](assets/makebox-logo.png)

MakeBox for Etsy connects Claude to the seller's own MakeBox workspace and Etsy shop. Its remote MCP connector provides listing, shop, research, and order tools. One shop-manager agent coordinates five focused workflow skills: creating a complete listing, improving existing listings, working with orders, researching keywords and niches, and managing shop structures. A sixth routing skill gives Claude chat the same shop-manager role, because chat does not run plugin sub-agents. The skills do not run code or make network requests by themselves; they guide Claude to the connected MakeBox tools when the seller asks for a task.

## Connect and use

Add this plugin in Claude, then connect the **MakeBox** connector through its OAuth sign-in. A MakeBox account and a connected Etsy shop are needed for Etsy listing actions. Reading and research are subject to the account's plan limits; listing management through MCP requires an eligible plan. Claude can help prepare listing content, but creating a draft, changing an Etsy listing, or publishing it requires the seller's review and approval. An Etsy draft is not visible to buyers; Etsy may apply its normal listing fees.

Try “create a draft listing for my product,” “improve the title and tags of this listing,” “which orders need attention?” or “research keywords for my niche.” The skills cover required listing fields, variations, personalization, shipping and return policies, photos and files, bulk SEO, order readback, and shop setup. They distinguish an unsaved AI suggestion from a saved MakeBox draft and a verified Etsy change. Image or video generation is not provided by this MCP connector.

## Data and support

The connector sends only the data needed for the selected tool call to MakeBox at `https://mcp.makebox.ai/mcp`. MakeBox uses the seller's OAuth connection for authorized Etsy operations. The plugin contains no credentials and does not access local files on its own. See [MakeBox](https://www.makebox.ai/) for product information, [privacy policy](https://www.makebox.ai/privacy), and [support](mailto:support@makebox.ai).

## Components

- `agents/makebox-etsy-manager.md`: the specialist's role, boundaries, and skill routing in Cowork and Claude Code.
- `skills/makebox-shop-manager/SKILL.md`: the coordinating role for ordinary Claude chat.
- `skills/create-etsy-listing/SKILL.md`: gather confirmed facts, create an Etsy draft, handle approved options and media, and verify it.
- `skills/optimize-etsy-listing/SKILL.md`: single and bulk SEO, reviewable suggestions, staging, and verified Etsy updates.
- `skills/manage-etsy-orders/SKILL.md`: live order reads and seller-approved fulfillment.
- `skills/research-etsy-market/SKILL.md`: keyword and niche evidence with product relevance checks.
- `skills/manage-etsy-shop/SKILL.md`: sections, shipping, returns, shop statistics, and monitoring.
- `.mcp.json`: the remote MakeBox MCP server; no local executable or API key is bundled.

Claude chat loads the skills and remote connector but does not run plugin sub-agents. In Cowork and Claude Code, the shop-manager agent can coordinate the same skills. This is a platform difference, not a missing MakeBox capability.
