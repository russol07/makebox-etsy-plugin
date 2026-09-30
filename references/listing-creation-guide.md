# Listing creation: field and tool guide

This guide is for a MakeBox-connected Etsy shop. It does not authorize an Etsy write on its own. Use the seller's exact product facts and approvals.

## Before the first Etsy draft

1. `list_shops` confirms which connected shop will receive the listing; `get_account_status` shows the plan and limits.
2. Choose `physical` for a shipped product or `digital` for a download. Ask when ambiguous. Confirm the title, full buyer-facing description, real price in the shop's currency, quantity, `who_made`, `when_made`, and whether the product is a supply. Never infer maker, material, dates, measurements, or shipping promises from a photo.
3. Use `search_categories` or `browse_categories` for the `taxonomy_id`. Gather 13 unique, relevant multi-word tags of at most 20 characters each. Research can help prioritize phrases, but cannot prove a ranking.
4. For a physical item, read `list_shipping_profiles` and choose the seller-approved profile. When that profile uses calculated postage, confirm the packed weight, all three dimensions, and their units. A profile appearing in the shop's list is not proof Etsy accepts it for this product.
5. Read `list_return_policies`; show the exact returns and exchanges settings. A no-returns policy for custom items is the seller's decision, not a default. If no suitable policy exists, `create_return_policy` creates one only after approval. Read `list_sections` and `list_production_partners` when those fields matter.
6. Show the complete proposed listing to the seller, including price, type, category, shipping and return policies, variations, personalization, tags, and media plan. `create_listing` writes to Etsy and may incur Etsy fees. Obtain approval for the exact card. Keep `publish: false` for an Etsy draft unless the seller separately approved going live with all required assets.

## After Etsy returns a draft ID

- `get_listing` confirms the Etsy listing ID and draft state. Do not recreate the listing if a response is uncertain; read the shop first.
- Attach approved product photos with `add_photos_to_listing`; check them with `list_photos`, then use `set_main_photo`, `reorder_photos`, or `set_photo_alt_text` only as requested. `get_upload_link` can help with a file that needs a secure upload path. The MCP server does not generate a new image.
- For a digital download, attach the approved files using `add_digital_files_to_listing`, then check `list_digital_files`. Digital non-made-to-order listings need their files before activation.
- For existing video files, use `manage_listing_videos` and verify with `list_listing_videos`. This uploads or manages media; it is not AI video generation.
- For size, color, or other buying options, read `get_listing_variations` and `get_listing_offerings`. Stage the **complete** axes and price/quantity table with `set_listing_variations` and `set_listing_offerings` using `publish: false`; these setters replace their saved sets. After the seller approves the full table, call `push_listing_variations` with `confirm: true` and require its Etsy verification. Do not equate a local save with a verified Etsy inventory update.
- For names, dates, text, or file-upload questions, read `get_listing_personalization` before `set_listing_personalization`. The setter replaces the complete question set; preserve every approved question and option. Confirm any additional price with the seller.
- If the return policy needs correction on an existing draft, `set_listing_return_policy` can apply a shop policy after seller approval and Etsy readback. It does not publish. Use `set_listing_section` and `set_listing_translation` when the seller requests those structures.

## Final gate

Show the ready Etsy draft, its media, options, price, delivery and return terms. Only an explicit seller request to publish authorizes `set_listing_state` with `state: "active"` and `confirm: true`. Read the listing back afterward. Report any failed or unconfirmed step by name; never claim the whole listing is complete because one tool succeeded.
