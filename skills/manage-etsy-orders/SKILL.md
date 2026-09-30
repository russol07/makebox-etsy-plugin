---
name: manage-etsy-orders
description: Read and manage the seller's Etsy orders through MakeBox when they ask what was ordered, what remains open, how much sold, or to mark a specific order shipped.
---

# Work with Etsy orders

Use the connected MakeBox MCP server. Orders are customer records; show only the details needed to answer the seller's request.

1. Confirm the connected shop with `list_shops`. Use `list_orders` for a current order list and `get_order` for one receipt. These tools read Etsy live. If Etsy cannot be reached, report the read failure instead of treating an older MakeBox snapshot as current.
2. Match the receipt ID, buyer, item, amount, currency, and status before describing or changing an order. `get_shop_stats` can summarize current order counts and totals; its section breakdown is a MakeBox-synced snapshot and should be labeled that way.
3. For fulfillment, show the exact order, tracking number, and carrier to the seller. `fulfil_order` can mark the order shipped or add tracking, which may email the buyer. Call it only after the seller explicitly approves that action and the exact tracking details. Do not invent a tracking code, carrier, dispatch date, or fulfillment state.
4. Read `get_order` again after a fulfillment action. Report the actual Etsy status and any uncertainty. If the response is ambiguous, do not repeat the write until the live state is checked.

The connector does not authorize you to refund, charge, cancel, or contact a buyer unless a specific tool and an explicit seller request support that action.
