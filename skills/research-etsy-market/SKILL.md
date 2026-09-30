---
name: research-etsy-market
description: Research Etsy keywords, competitors, and a product niche with MakeBox when the seller asks what buyers search for or which phrases fit a real listing.
---

# Research keywords and niches

Use MakeBox MCP for evidence, then apply product relevance before suggesting words. Research results are guidance, not proof of Etsy ranking or future sales.

1. Start with the seller's product or an existing listing from `get_listing`. Identify type, materials, buyer use, and any seller-approved constraints. Ask for missing facts rather than using a generic niche assumption.
2. Use `search_keywords` for candidate phrases. It reports MakeBox database estimates of monthly searches, competing listings, and an opportunity score; its default sort values opportunity, not raw search volume. Use `check_keywords` for up to 40 exact phrases worth comparing. Missing statistics mean the database has no record, not that demand is zero.
3. When the seller asks for niche or competitor context, use `find_shops_in_my_niche`, `search_top_listings`, `analyze_competitor_listing`, or `competitor_tags` as relevant. Separate live public Etsy observations from MakeBox keyword estimates. A shop's lifetime sales are not sales of an individual listing.
4. Rank suggestions by fit with the actual product and likely buyer intent, then weigh available demand and competition. Reject competitor brands, trademarks, irrelevant phrases, unsupported materials, and repeated synonyms used just to fill a quota.
5. Return a concise shortlist with the evidence and uncertainty for each term. If preparing Etsy tags, choose exactly 13 distinct relevant multi-word phrases at most 20 characters each; if you cannot reach 13 honestly, ask for more product facts or say the set is incomplete. Do not promise traffic or a ranking position.

Keyword and niche lookups count against the seller's plan limits. Do not repeatedly query the same terms without a reason.
