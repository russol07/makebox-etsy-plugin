---
name: optimize-etsy-listing
description: Improve an existing Etsy listing through MakeBox when the seller asks for a better title, description, tags, or an AI-assisted SEO review with approval before changes reach Etsy.
---

# Improve an existing Etsy listing

Use the MakeBox MCP connector. Keep the original listing and its verified product facts in view throughout the workflow.
For a batch of listings, follow the separate quote, job, review, and push sequence below; never treat a completed AI job as an Etsy publication.

1. Read the target with `get_listing` and confirm which fields the seller wants changed. Distinguish a MakeBox record from a live Etsy readback. Use `list_photos` and, when relevant, `search_keywords` or `check_keywords` for context. Do not claim a guaranteed rank, traffic increase, or sales result.
2. `optimize_listing` consumes the seller's MakeBox AI allowance and returns an **unsaved suggestion**. Call it only for the requested fields, not speculatively. A single field costs one third of a listing action; all three text fields cost one listing action. Do not repeat a successful generation just to look for a different answer.
3. Compare proposed title, description, and tags with the current content. Check factual fidelity, readability, and that a complete replacement tag set contains exactly 13 unique, relevant phrases within Etsy's length limit. Show the seller the changes before saving.
4. After approval to save, use `update_listing` with `publish: false` to stage the selected fields in MakeBox. This is not an Etsy update. After separate approval to send those changes, use `push_listing_to_etsy` with `confirm: true`. This updates the linked Etsy listing but does not turn a draft into an active listing.
5. Read the result back with `get_listing`; if variations or prices changed, use the dedicated variation tools and their Etsy verification. Report whether the result is a suggestion, staged in MakeBox, verified on Etsy, or unconfirmed. Never describe a failed or uncertain push as successful.

Never activate a draft as a side effect of optimization. Use `set_listing_state` only after the seller reviews the ready listing and explicitly approves publication.

## Bulk optimization

1. Confirm every selected listing ID and requested fields. Call `quote_bulk_seo` first; it returns the exact titles, cost, balance, and any IDs outside this shop. Show that quote to the seller.
2. Only after approval of the list and cost, call `start_bulk_seo` with `confirm: true`. This charges credits and returns a background `job_id`; it does not update Etsy.
3. Use `get_bulk_seo_job` to check each listing and stage. Report failures honestly and wait for completion. Show the finished proposed changes for review.
4. `push_bulk_seo_job` with `confirm: true` changes every listing in the finished job on Etsy. Call it only after explicit approval to send **all** those changes. If the seller approves only some, use the per-listing review/push path instead of this whole-job tool.
