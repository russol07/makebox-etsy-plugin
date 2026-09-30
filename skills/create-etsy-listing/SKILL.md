---
name: create-etsy-listing
description: Create a new Etsy listing through MakeBox when the seller asks to turn a real product or digital item into a complete draft, attach approved media, or prepare it for publication.
---

# Create an Etsy listing

Use the MakeBox MCP connector for this workflow. A skill alone does not create or publish anything.
For the complete field, variation, personalization, media, and policy sequence, read `../../references/listing-creation-guide.md` when those parts are relevant.

1. Identify the seller's connected shop with `list_shops` and account access with `get_account_status`. If the shop is not connected or the plan blocks listing management, explain the exact blocker before drafting an Etsy action.
2. Collect confirmed facts: physical or digital type; title, description, price, quantity, Etsy category, maker, production date, materials, personalization, variations, and any size or shipping claims. Do not invent product specifications or seller policies. Use `search_categories` or `browse_categories` for a category. For physical items, read `list_shipping_profiles`; read `list_return_policies` for the seller-approved policy. Ask when a required fact is missing.
3. Prepare 13 distinct, relevant, multi-word Etsy tags of at most 20 characters each. `search_keywords` and `check_keywords` may provide evidence within the seller's plan limits; search volume is not a guarantee of Etsy rank or sales.
4. Show the complete proposed card and whether it will be a **draft** or a live listing. Explain that creating an Etsy listing may incur Etsy's normal fees. Only after the seller approves the exact card, call `create_listing` once. Leave `publish` false unless the seller explicitly approved immediate publication and the listing is ready for buyers.
5. Attach only seller-approved photos with `add_photos_to_listing`, digital files with `add_digital_files_to_listing`, or existing video files with `manage_listing_videos` when requested. Configure approved variations and their full price/stock table with the dedicated variation tools, and any agreed personalization questions with `set_listing_personalization`; verify each result. The connector does not generate images or videos. Use `get_listing` to verify the returned Etsy ID and state; report any incomplete media transfer explicitly.
6. If the seller later wants the draft live, show its current content and ask for approval before `set_listing_state` with `state: "active"` and `confirm: true`. A draft, an unsaved suggestion, and a published listing are different outcomes.

If Etsy rejects a write or the result is uncertain, report the returned reason. Read the listing before deciding on any retry; never create a second listing merely to see whether the first one worked.
