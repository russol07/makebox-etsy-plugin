---
name: optimize-etsy-listing
description: Improve Etsy listing copy or other approved fields through MakeBox, using chat-authored suggestions and direct Etsy updates by default; use internal MakeBox AI or bulk jobs only when requested and their cost is approved.
---

# Improve an existing Etsy listing

Use the connected MCP server and read `../../references/direct-etsy-api-guide.md`. Keep the seller's verified product facts and the current Etsy content in view.

1. Read the listing with `etsy_get_listing`; identify which fields the seller wants changed. Read images or inventory when relevant. MakeBox keyword tools can provide evidence within their quotas.
2. Prepare the requested improvements in this chat or preserve the seller's finished replacement. Compare the proposed values with the current listing. No additional MakeBox generation is required.
3. Follow Etsy's native field limits and avoid invented facts, irrelevant keywords or ranking guarantees. If the seller requests a full SEO proposal, aim for a useful complete tag set; do not force 13 multi-word tags into an approved direct request that Etsy permits with fewer.
4. Show the exact changes. After approval for those values and targets, use `etsy_update_listing` for its exposed fields. Price/quantity/variation changes use a freshly read, complete `etsy_update_listing_inventory` payload; preserve options not approved for removal.
5. Read back with `etsy_get_listing` or `etsy_get_listing_inventory`. `accepted_by_etsy: true` with `verified: false` is HTTP acceptance, not a separate verification. Never activate a draft as a side effect of optimization.

For a chat-authored batch, confirm the exact listing set and per-listing changes, apply the approved requests, and track each result. Do not start a paid MakeBox AI job just because the request mentions several listings.

## Optional MakeBox AI workflow

If the seller asks MakeBox to generate the improvements, use `optimize_listing` only after its scope and allowance are approved. It returns an unsaved suggestion and consumes a MakeBox AI allowance. Local staging with `update_listing(publish: false)` and a subsequent approved push remain available when requested.

For an internal bulk AI run: `quote_bulk_seo` → approval of list and cost → `start_bulk_seo` → `get_bulk_seo_job` → review → approved `push_bulk_seo_job`. A completed job is not publication. The all-results push requires approval for every included listing; use the per-listing path if only some are approved.

Never repeat an uncertain write or successful generation automatically.
