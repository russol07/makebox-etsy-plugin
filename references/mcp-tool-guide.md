# MakeBox MCP workflow map

The remote server in `.mcp.json` supplies the current tool catalogue. Start with [Direct Etsy API through MakeBox](direct-etsy-api-guide.md) for direct seller actions, native Etsy IDs, full schemas, file transport and readback. Do not infer missing API functionality from a convenience tool's narrower schema.

## Direct actions and extra MakeBox workflows

| Task | Default route | Optional MakeBox workflow |
| --- | --- | --- |
| Finished listing copy | `etsy_create_draft_listing` or `etsy_update_listing` after seller approval | `create_listing` for its documented convenience behavior; local draft tools when requested |
| Chat-authored SEO improvements | Read live, prepare copy in the chat, then `etsy_update_listing` and read back | `optimize_listing` only when MakeBox generation is requested and its allowance is approved |
| Prices and options | `etsy_get_listing_inventory` → approved full `etsy_update_listing_inventory` → read back | MakeBox variation/offering staging and `push_listing_variations` when local staging is requested |
| Existing media | `etsy_upload_listing_image`, `etsy_upload_listing_file`, `etsy_upload_listing_video`; read back | `get_upload_link` supplies owned assets; library/media convenience tools remain available |
| Shipping, returns, sections and processing | Corresponding `etsy_*` read/create/update/delete methods | Existing shop setup helpers can be used when their scope matches |
| Orders and financial records | Corresponding live receipts, transactions, payments and ledger reads | `list_orders`, `get_order`, `get_shop_stats` offer summaries |
| Public Etsy market data | Public `etsy_*` listing/shop/review/taxonomy reads | Keyword database and niche-analysis tools add MakeBox-specific estimates and quotas |
| Internal bulk AI generation | Not required for a chat-authored batch | `quote_bulk_seo` → approved `start_bulk_seo` → `get_bulk_seo_job` → review → approved `push_bulk_seo_job` |

Direct `etsy_*` transport does not spend MakeBox AI allowances or rewrite the payload. Plan gates and Etsy fees remain. MakeBox-specific research can have daily quotas. `optimize_listing` uses one listing action for all three text fields or one third for a single field; `start_bulk_seo` charges the quoted allowance and does not publish by itself. Never invoke either just to send already-prepared content.

Separate chat suggestions, MakeBox-only staging, an Etsy-accepted request, an Etsy draft and a verified published listing. If an outcome is uncertain, read before retrying. Report the actual source, target ID and any unresolved step.
