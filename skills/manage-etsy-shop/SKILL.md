---
name: manage-etsy-shop
description: Manage seller-authorized Etsy shop settings through MakeBox, including sections, shipping and return profiles, processing, holiday preferences, shop details, account permissions and monitoring.
---

# Manage an Etsy shop

Read `../../references/direct-etsy-api-guide.md`. Use current `etsy_*` schemas for direct shop operations, and read the existing configuration before changing it.

1. Identify the selected workspace with `list_shops` and plan access with `get_account_status`. Current Etsy shop details are available through `etsy_get_shop`; `etsy_get_me` identifies the authorized Etsy account.
2. Use the corresponding section read/create/update/delete operations for shop structure. Explain what removing a section does to its listings and use the seller's exact approval.
3. Read `etsy_get_shop_shipping_profiles` and `etsy_get_shop_shipping_profile` to show destinations and charges. To assign a profile to an existing listing, use `etsy_update_listing` with only the approved `shipping_profile_id`, then read it back. The focused `set_listing_shipping_profile` helper is also available. A manual Etsy edit is not required merely because a convenience tool lacks the field.
4. Shipping profile, destination and upgrade operations can change terms for multiple listings. Identify affected listings, show rates/origin/timing and obtain authorization for that scope. Do not edit or delete a shared profile merely to fix one listing; first move dependencies when appropriate.
5. Read return policies and confirm returns, exchanges and deadline before creating or changing one. Direct listing policy assignment uses `etsy_update_listing`; policy consolidation can move all dependent listings and delete the source policy, so explain the complete effect.
6. Use the live processing/readiness and holiday-preference tools for confirmed dispatch schedules. Use `etsy_update_shop` only for the seller-approved text fields. Do not guess promises to buyers.
7. Personal email or saved-address methods are for the connected Etsy user's account and may require optional `email_r` or `address_r` consent. Read the returned blocker and reconnect link; never request credentials or silently expand access.
8. Existing MakeBox monitoring tools remain available within plan limits. Distinguish their stored observations from live Etsy data.

After an accepted write, read the resource again and report the actual state. An overview request authorizes reading, not a shop change.
