---
name: use-etsy-api
description: Use MakeBox as a direct intermediary to Etsy when the seller asks for a supported API action, supplies finished content, needs a capability missing from a convenience tool, or wants live listings, policies, orders, reports, account data or media operations.
---

# Use the direct Etsy API

Read `../../references/direct-etsy-api-guide.md` for the connection, request, authorization, media and readback contract.

1. Identify the seller's request and connected account. Discover the relevant live `etsy_*` operation and inspect its full input schema. Do not assume a capability is unavailable because an older MakeBox tool lacks it.
2. Prepare only the seller-approved fields. Direct calls use native Etsy IDs and do not need an imported MakeBox row. Keep omitted fields omitted and preserve the permitted value types. Public research may use another shop's ID; private writes stay in the connected shop.
3. For finished content or copy you prepare in the chat, use direct transport. Do not trigger internal MakeBox AI generation unless the seller requested it and approved the allowance.
4. Before writing, show the exact target and values, including buyer-facing effects, and use the seller's explicit approval for that scope. Reuse valid approval for the same action; set `confirm: true` only then.
5. Read the returned Etsy status and payload. HTTP acceptance with `verified: false` is not a separate verification. Follow `readback` or the corresponding read tool. Never replay an uncertain write automatically.
6. Report the result and any actual Etsy permission or validation blocker. Additional personal-data scopes require the seller's OAuth consent; never request credentials in chat.

Use the focused listing, order, research or shop skill for domain details. The runtime tool catalogue, not a count or list saved in this plugin, is the authority for current capabilities.
