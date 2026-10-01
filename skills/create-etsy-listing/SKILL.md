---
name: create-etsy-listing
description: Create an Etsy listing through MakeBox from the seller's product facts or finished copy, prepare a complete draft, attach approved media, configure options and publish only with seller authorization.
---

# Create an Etsy listing

Read `../../references/listing-creation-guide.md` for the complete sequence and `../../references/direct-etsy-api-guide.md` for direct transport. A skill alone creates or publishes nothing.

1. Identify the connected shop with `list_shops` and account access with `get_account_status`. Read the current schema of `etsy_create_draft_listing`.
2. Collect seller-confirmed product type, price, quantity, category, maker/provenance, materials, options and any shipping claims. Prepare requested copy in the chat; preserve finished copy the seller supplied. Use Etsy's actual enum values from the live schema.
3. Use current taxonomy, shipping, returns, section and production-partner reads as relevant. Confirm the selected profiles and real packed weight/dimensions where required. Do not infer that an existing profile will be valid for every product.
4. Research may guide relevant title/tag suggestions but does not prove ranking or product facts. Follow native Etsy limits for a direct request. Do not force extra multi-word tags into a seller-approved payload solely to satisfy a separate MakeBox generation policy.
5. Show the complete proposed draft and approved media/option plan. After approval, call `etsy_create_draft_listing` with its `body` and `confirm: true`. This creates a draft; publication is a separate explicit action.
6. Read the Etsy result, attach approved media, configure the complete inventory and personalization as requested, and verify each step. No internal MakeBox AI call is needed to send chat-authored copy.
7. Only when the seller authorizes publication of the ready listing, use `etsy_update_listing` with the approved `state: active` change. Read the listing back and report its actual state; Etsy's normal fees may apply.

If a write fails or is uncertain, read before deciding on a retry. Never create another listing just to test whether the first creation succeeded. Existing MakeBox creation/staging workflows remain available when the seller specifically wants them.
