# Asbestos Removals London — PROJECT CHECKPOINT

Updated: 20 September 2026
Working branch: `seo-protection-gsc-20260920`
Production branch: `main`
Repo: `mleeng2026/asbestos-removals-london`
Deployment: GitHub main -> Hostinger auto-deploy

## Governing V3 Mega Mega
Current master verified from Google Drive:
MATTHEW_1827_20_SEPTEMBER_2026_LOCAL_SEO_V3_MEGA_MEGA_MASTER_LATEST_LATEST.txt
20 September 2026 — 18:27 BST
Source: https://drive.google.com/file/d/1CE3o3HLrbvICSOTTHAIn4h5lNFG8TZxi/view?usp=drivesdk

Hard rule: read the complete current master before important page work and re-audit finished work line by line before approval/deployment.

## Completed in this audit
- Windsor/Search Console property confirmed: sc-domain:asbestosremovalsinlondon.co.uk
- GSC protection window available through Windsor: 2–17 September 2026
- SITE-INVENTORY.csv created from current sitemap + GSC data
- Current classifications: 20 PROTECT / 36 REVIEW CAREFULLY / 134 SAFE TO REWORK
- Safe working branch created before SEO changes
- Crawlable backup HTML files removed from the working branch
- Added planned legacy redirects on working branch:
  - /home.html -> /
  - /asbestos8203-roof-removal8203-8203london.html -> /asbestos-roof-removal-london.html
- Existing www -> non-www 301 retained
- Existing Sutton legacy redirect retained

## Key GSC opportunities / protection
- Homepage: PROTECT
- asbestos-artex-removal-london.html: PROTECT — query "asbestos artex removal london" improved strongly in the later period
- asbestos-pipe-removal-london.html: PROTECT — overall avg position about 17.68; "pipe lagging removal london" about 5.88
- asbestos-floor-removal-london.html: PROTECT
- Kingston + Kingston upon Thames: PROTECT pending cannibalisation resolution
- Chiswick / Teddington / Putney / Surbiton / Wandsworth: page-one/page-two opportunity cluster

## Technical findings
- Current canonical host is non-www.
- .htaccess forces www -> non-www.
- Search Console still shows both hosts during 2–17 Sep; treat as migration/history and verify live/indexed canonical before any hostname reversal.
- /home.html is legacy only; absent from current repo.
- /asbestos8203-roof-removal8203-8203london.html is legacy only; absent from repo.
- /asbestos8203-8203disposal8203-8203in8203-8203london.html is CURRENT, indexable, self-canonical and in sitemap. It has no clicks and weak rankings. Do not remove until a clean redirect target/content plan is mapped.
- 9 crawlable backup HTML pages were present in deployable repo root; removed on working branch.

## Current execution point
Phase 1 GSC forensic audit: COMPLETE
Phase 2 technical/URL audit: IN PROGRESS
Phase 3 site inventory/protection map: STARTED — base inventory exists
Phase 4 quick-win execution: pipe-lagging page selected as first surgical page
Phase 5 location execution: pending
Phase 6 full V3 image/schema/local treatment: pending
Phase 7 final line-by-line V3 + live QA: pending

## First page selected
/asbestos-pipe-removal-london.html

Why:
- 363 impressions in current GSC window
- avg position ~17.68
- "pipe lagging removal london" avg ~5.88
- "asbestos pipe lagging removal kingston upon thames" avg ~9.68
- 0 clicks: strong CTR/content/conversion opportunity
- Existing URL, canonical, H1 and primary intent are protected

Current page weaknesses:
- about 738 visible words
- current JSON-LD is disconnected/legacy: separate Service, BreadcrumbList, FAQPage and a minimal WebPage image block
- anonymous Organization duplicated in Service provider instead of root graph @id
- primary image is not represented as a full page-specific ImageObject
- form wording says within an hour; current V3 permitted line is "we normally reply within 30 minutes or less"
- no Formspree honeypot on this page
- buyer detail around survey/register, shutdown, plant-room access, sequencing and what to send can be improved without changing core intent
- image system needs final visual/metadata/primary-image verification before page can be called V3 complete

## Image library checked for pipe page
Primary asbestos image library:
https://drive.google.com/drive/folders/1KU-MPF0akefdCvkwUgMWtwL8_gMWKRUT?usp=drive_link

Potential visually reviewed supporting images:
- suspected-asbestos-pipe-insulation-loft-19.jpg — visibly shows insulated pipework in a loft; exact asbestos subtype is NOT confirmed from photo alone
- suspected-asbestos-pipe-insulation-service-area-04.jpg — visibly shows insulated service pipework; exact asbestos subtype is NOT confirmed from photo alone

Do not relabel either as confirmed asbestos pipe lagging unless job/survey context confirms it.

## Next actions
1. Finish query ownership/cannibalisation map.
2. Complete surgical pipe-page content + connected graph upgrade on working branch.
3. Re-read current V3 master and run page-level PASS/FAIL/N/A audit.
4. Do not merge to main until diff, technical checks and image/schema checks pass.
