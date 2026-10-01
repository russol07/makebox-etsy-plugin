---
name: manage-etsy-orders
description: Read current Etsy orders, transactions and payment reports through MakeBox, or fulfill a specific order with the seller's approval and fresh Etsy readback.
---

# Work with Etsy orders and reports

Use `../../references/direct-etsy-api-guide.md`. Orders and financial records can contain private customer data; show only what answers the seller's request.

1. Confirm the connected workspace with `list_shops`. Use `etsy_get_shop_receipts` and `etsy_get_shop_receipt` for current records with the live filtering/pagination schema. `list_orders` and `get_order` remain useful summaries.
2. Match receipt ID, buyer, item, amount/currency and status before describing or changing an order. Quote buyer personalization exactly. Use `etsy_get_shop_receipt_transactions_by_receipt` or the relevant transaction read for details.
3. For financial questions, discover the appropriate payments or payment-account ledger read. These are read-only records; they do not issue refunds, charge buyers or transfer money. Paginate and label the actual date range instead of presenting a partial page as lifetime totals.
4. For fulfillment, show the exact receipt, real tracking/carrier and any buyer message or dispatch data. `etsy_create_receipt_shipment` can send a buyer notification, and `etsy_update_shop_receipt` changes its documented status fields. Use the seller's explicit approval for the exact action; never invent fulfillment facts.
5. Read the receipt after the accepted write. A timeout or ambiguous result requires readback before any retry.

`get_shop_stats` may include a section breakdown from MakeBox's imported snapshot; label it as such. Report Etsy errors without substituting stale data as current. General messaging, refund or cancellation capability must not be inferred from the existence of order reads.
