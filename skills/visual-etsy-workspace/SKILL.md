---
name: visual-etsy-workspace
description: Open the MakeBox listings workspace when a seller asks for a visual catalogue or wants to select a listing for discussion. Works only when the connected MCP server exposes the workspace tool and the host supports MCP Apps.
---

Call `get_account_status` at the start of the task. If the seller asks to browse visually and `open_makebox_workspace` is available, call it with no arguments. It presents MakeBox saved listings and separate live Etsy active and draft views. Its optional buttons start a conversation about creating a listing, improving SEO or researching keywords; they do not themselves run paid generation or change Etsy. When the host does not render MCP Apps or the tool is unavailable, use the existing `list_listings` and `get_listing` tools instead; never claim the view opened when it did not.

MakeBox listing IDs and Etsy listing IDs are separate namespaces. For a saved MakeBox item use its MakeBox ID with `get_listing`. For an Etsy item use its Etsy ID with `etsy_get_listing`; verify the returned item before any operation. Distinguish Etsy live data from the MakeBox mirror. Never invent photos, SKU, price currency or other missing fields. The workspace is read-only. Existing seller approval and verification requirements still apply to every change, generation and publication.
