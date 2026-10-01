---
name: research-etsy-market
description: Research relevant Etsy keywords, competitors, reviews and product niches through MakeBox, distinguishing current public Etsy observations from MakeBox keyword estimates.
---

# Research keywords and niches

Use MakeBox MCP for evidence, then apply product relevance. Read `../../references/direct-etsy-api-guide.md` when selecting an exact Etsy API method.

1. Establish the real product, confirmed materials/use and seller constraints. Read an existing target with `etsy_get_listing` when available; do not treat competitor copy as product facts.
2. MakeBox `search_keywords` and `check_keywords` provide database estimates within plan quotas. Missing statistics mean unknown, not zero demand. An opportunity score is not a ranking prediction.
3. Public direct tools include `etsy_find_all_listings_active`, `etsy_find_shops`, `etsy_get_shop` and listing/shop review reads. Discover the relevant live schema and paginate. Public research may target other shops; private writes may not.
4. Existing `search_top_listings`, `competitor_tags`, `find_shops_in_my_niche` and analysis tools can add MakeBox-specific summaries. Label their source and observation date. Lifetime shop sales are not per-listing sales.
5. Rank phrases by fit with the seller's product and buyer intent, then available demand/competition evidence. Exclude unsupported product claims, unrelated brands and filler phrases.
6. Return an evidence-backed shortlist with uncertainty. When drafting tags, follow Etsy limits and seller intent. Exactly 13 multi-word tags is a MakeBox AI generation rule, not an extra requirement on a valid seller-approved direct API request.

Do not promise traffic, sales or a search position. Research does not authorize listing edits or paid AI generation.
