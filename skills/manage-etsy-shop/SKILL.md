---
name: manage-etsy-shop
description: Manage the connected Etsy shop through MakeBox when the seller asks about sections, shipping or return policies, shop statistics, languages, monitored shops, or store setup.
---

# Manage an Etsy shop

Use MakeBox MCP for the seller's own connected shop. Read the current state before suggesting an operation.

1. Confirm the connected workspace with `list_shops` and plan access with `get_account_status`. Use `get_shop_stats` for a current overview and label any field the tool says is MakeBox-synced rather than Etsy-live.
2. For structure, read `list_sections` before `manage_shop_sections` or `set_listing_section`. Creating, renaming, and deleting sections change the Etsy shop; show the exact effect and get seller approval. Removing a section does not delete its listings, but can leave them unsectioned.
3. For physical products, read `list_shipping_profiles` live and confirm the correct one. A profile ID existing in the shop does not guarantee Etsy will accept it for a particular listing. Ask for real origin, postage, processing, weight, and dimensions where required; never invent them. Use `create_shipping_profile` or `create_processing_profile` only from seller-approved facts.
4. Read `list_return_policies` before choosing or creating one. Returns and exchanges are promises to buyers. Use `create_return_policy` only after the seller confirms those terms. `set_listing_return_policy` can assign an existing policy to an Etsy draft after approval; it checks the policy and Etsy readback and does not publish the draft.
5. For research and monitoring, use `list_monitored_shops`, `monitor_shop`, and `stop_monitoring_shop` within plan limits. Explain whether a result is a fresh Etsy read or a saved MakeBox snapshot.

Never switch shop connections, alter buyer-facing policies, or publish a listing merely because the user asked for an overview.
