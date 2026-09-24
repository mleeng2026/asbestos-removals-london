# Production verification — 24 September 2026

- PR #27 merged as `7996b9cb3ef5e3cbc9893e591826594071c14a9e` and Hostinger automatically deployed it from GitHub. A cache-busted browser read showed the quote section touching the bottom of the hero on both Bromley and Barnet; the next content section followed the quote section. The form action stayed `https://formspree.io/f/xppaoyqd`, with no horizontal overflow in the 1363px desktop viewport.
- All 32 borough HTML URLs returned HTTP 200 and exact bytes matching the reviewed repository files on fresh HTTP requests with `Cache-Control: no-cache`. The prior 23 editorial repairs and sitemap were also verified live with exact byte comparisons. No test lead was submitted.
- A previously opened browser tab could briefly show its old cached HTML on the clean URL while the query-busted URL and fresh server request returned the updated version. A fresh request verified the intended production bytes. Mobile visual testing remains outstanding because this cloud browser did not change viewport when its device shortcut was tried.
- Google-selected canonicals and indexing status remain for Search Console review. Start with Bromley, Brent, Bexley, Merton, Newham and Westminster after normal recrawl. The earlier notes below describing deployment as pending are historical and superseded by this section.

---

# Live deployment and borough quote position — 24 September 2026

- PR #26 merged to main as `25ea771ff302770f084049aca57f151fc54d4216`. Hostinger's GitHub connection automatically deployed it. All 23 revised borough HTML files and the sitemap returned HTTP 200 and matched the reviewed repository bytes exactly. Bexley, Brent, Bromley, Merton, Newham and Westminster showed three distinct briefs, five FAQs, unchanged Formspree action and correct HTTPS non-www canonical in the live desktop browser, with no horizontal overflow at 1363px.
- A live visual check exposed a pre-existing CSS `order:3` on `.quote-section`. Despite the form following the hero in HTML, this places it after borough content on all 32 borough pages, including Barnet. A 32-page inline override `main.borough-page > section.quote-section{order:0}` is prepared to keep the quote form directly under the hero without changing form markup or the globally cached CSS file. Static comparison confirmed this one style element is the only change to the 32 HTML files.
- Next: merge and deploy the quote-order fix via GitHub, then verify browser layout on at least Bromley and Barnet, check all 32 live files match the repo, and update this checkpoint. A test form submission was not made. Mobile viewport visual QA remains a separate limit if this browser cannot change viewport.
- Earlier notes lower in this file describing the 23-page repair as undeployed refer to the state before PR #26 was merged and are superseded by this entry.

---

# 22 discovered-page V3 repair — 23 September 2026

User authorised all 22 important discovered pages, excluding other-helpful-links. Latest governing master: MATTHEW_1141_21_SEPTEMBER_2026_LOCAL_SEO_V3_MEGA_MEGA_MASTER_LATEST_LATEST.txt, sections 1–128.

Implemented in this batch:
- Distinct buyer-led content for all 22 URLs listed in discovered-repair/manifest.json; four native expandable sections, six exact visible/JSON-LD FAQs and three page-specific images per page.
- Editorial copy including captions: 1,058–1,263 words; maximum pairwise five-word overlap 7.29% including repeated photographic subjects and labels. Draft prose alone maximum 2.7%. These are internal similarity measures, not Google scores.
- Removed visitor-facing SEO planning language. Preserved useful service coverage and project guidance, with protected H1s, titles, canonical URLs, form markup, analytics, consent, header and footer unchanged.
- 66 approved-photo derivatives, visually classified by subject, metadata-remuxed with verified local points; decoded pixels unchanged. Primary image, Open Graph, Twitter, Service, WebPage, ImageObject and sitemap aligned.
- Added direct hub links to South London and West London; contextual service links and local coverage links checked against real files. No homepage change or resubmission.
- Sitemap dates updated only for changed pages and the locations hub. No redirect or server-rule change.

Verification complete: PR #24 merged as f5e81409d0324160297a0003a9cd7de4ee520d39 and deployed through Hostinger. All 91 checked public HTML/image/CSS/sitemap responses returned HTTP 200, had no redirects and matched the reviewed local bytes. All 22 desktop layouts (1363px viewport) and all 22 phone-width layouts (390px frame, 375px content area) passed overflow checks. All 66 images loaded in the mobile review; native content panels and FAQs opened. Desktop and mobile quote links reached visible forms; no test enquiry submitted. Evidence: discovered-repair/live-qa.json, browser-qa.json and live-preview.jpg. Temporary noindex review page is removed in the QA follow-up commit. No homepage or indexing submission was performed. Google indexing status still requires a later Search Console check; publishing does not guarantee indexing.

Evidence: geodata URLs are recorded with each image in LOCATION-IMAGE-MAP.csv and discovered-repair/geo-*.json. Local research used the councils’ published conservation, centre and employment-area information (Islington, Haringey, Hackney, Croydon, Kingston, Ealing, RBKC, Havering, Harrow, Waltham Forest and Richmond). Technical scope was checked against HSE survey, licensed, non-licensed and notifiable non-licensed work guidance. No completed local job, customer review, fixed price or removal date invented.

Previous Sutton checkpoint retained below.

---

# Asbestos London repair checkpoint — 23 September 2026

Current batch: Sutton town and Sutton borough, preserving both protected URLs.
Master: MATTHEW_1141_21_SEPTEMBER_2026_LOCAL_SEO_V3_MEGA_MEGA_MASTER_LATEST_LATEST.txt (Drive), sections 1–128 read; earlier Library copy stopped at section 124.

## Implemented
- Replaced visitor-facing SEO notes and generic filler with distinct buyer journeys.
- Sutton town: ceiling/floor refurbishment, purchase, shop/flat access, garage scope.
- Sutton borough: survey schedules, managed/occupied sites, Beddington commercial roofs, multi-property work.
- Eight visible/schema-matched FAQs per page; approximately 1,600 editorial words each; pairwise five-word phrase overlap 1.63% (excluding forms and breadcrumbs).
- Existing H1s, canonicals, URLs, form markup, tracking scripts, shared CSS and consent preserved.
- Existing imagery visually inspected; no photograph content changed. Page-specific copies and GPS/title/description metadata remuxed without recompressing pixels. Correct intrinsic dimensions added.
- All primary image signals, postcode/Place/GEO and image sitemap aligned. Site inventory and image map included.

## Verification
Static checks passed: internal file targets, canonical, one H1, unique IDs, JSON-LD, exact FAQ parity, form/tracking unchanged; image decode/GPS/pixel equality.
Published through PR #20, main deployment commit 69118a3d41612d341121fd5ed7daaf58223a9612. Live HTML for both pages, sitemap and all six page images returned HTTP 200 and matched local bytes. Desktop browser verified both heroes, quote links reaching rendered forms, and opening FAQs; town gallery images render. No horizontal overflow at 1363px viewport. No test lead submitted. Mobile visual verification remains outstanding: the supported cloud browser has no viewport controls, and browser UI shortcuts did not change it. Do not call full V3 completion before mobile verification. Local preview access was blocked; no workaround after policy denial.

## Sources
Local points: UK City Map Sutton, Sutton Station, West Sutton Station, Sutton Common Station and Sutton Head Post Office stop on Grove Road (URLs in LOCATION-IMAGE-MAP).
Local context: Sutton Council loading/unloading; parking restrictions; 2023 Employment Land and Economic Needs Assessment; asbestos disposal page.
Technical scope: HSE non-licensed work, notifiable non-licensed work and asbestos material guidance.
No completed Sutton job history invented. Existing regional enquiry patterns are explicitly London-wide.
Primary Drive asbestos image folder checked; only Teesside subfolder exposed and no direct photographs returned there. Retained established website photographs after visual review.

## Remaining
Carshalton, Wallington, Cheam and remaining borough/town pages need their own source-based repairs. Barnet second-last and Croydon last as agreed.
Search Console duplicate-canonical investigation paused by Matthew: no Google-selected canonical evidence acquired; no canonical or redirect changes made. Browser sign-in unavailable without correct credentials; Windsor lacks URL Inspection fields.

## Readability update requested by Matthew
Both Sutton pages now retain all original content within four native expandable sections after the visible introduction. Town gallery moved above the panels; borough adds two relevant existing Sutton secondary images with connected page-specific ImageObject/Place/GEO IDs. Existing filenames, embedded metadata, assigned coordinates and primary-image signals retained. No new location slots or source photographs introduced. Static content preservation, forms/tracking/canonical checks passed. Live verification follows deployment.
# Borough comparison and editorial repair — 24 September 2026

## Source and checkpoint

- Governing master: `MATTHEW_1141_21_SEPTEMBER_2026_LOCAL_SEO_V3_MEGA_MEGA_MASTER_LATEST_LATEST.txt` (Drive; sections 1–128). Existing handoff `ASBESTOS-LONDON-FULL-WORK-MODE-HANDOFF.txt` read.
- Starting repository main: `49783d39918c6df5d7ecb08d4df11da789a5b27c`. This is a protected baseline. Work prepared on a separate repair branch; see branch/PR status below when published.
- All 32 borough URLs (`asbestos-removal-*-london.html`, excluding four regional pages) were compared. Strong/different: Barnet, Croydon, Ealing, Islington, Kensington and Chelsea, Kingston upon Thames, Richmond upon Thames, Sutton and Wandsworth. The other 23 had roughly 440–480 editorial words and 71–73% five-word phrase overlap with another page after common forms/navigation were excluded. This is an internal diagnostic, not a Google score or penalty finding.

## Changes prepared

- Repaired 23 short borough pages: Barking and Dagenham, Bexley, Brent, Bromley, Camden, Enfield, Greenwich, Hackney, Hammersmith and Fulham, Haringey, Harrow, Havering, Hillingdon, Hounslow, Lambeth, Lewisham, Merton, Newham, Redbridge, Southwark, Tower Hamlets, Waltham Forest and Westminster.
- Each has three separately written local buyer briefs, material and access distinctions, a direct quote path, relevant town/service links and five visible questions with matching FAQPage JSON-LD. These are hypothetical buyer situations, not completed-job claims. Shared homepage/area/service hierarchy and protected slugs remain.
- Removed the generic six-borough carousel on those pages. Changed the generic hero alt to describe the enclosure without falsely presenting it as work photographed in the borough. Kept the existing generic primary image; no unverified local photo metadata or fabricated geocoordinates were added. Existing Formspree markup, analytics, consent, canonical, business entity and navigation were preserved.
- Titles retained; descriptions/OG copy updated where necessary. Updated `SITE-INVENTORY.csv` and sitemap `lastmod` only for the 23 changed pages. Robots and `.htaccess` unchanged.

## Technical diagnosis

- Browser navigation of live representative paths on HTTP non-www, HTTP www and HTTPS www all ended on HTTPS non-www with current page content. The HTTPS www East London path also ended at the current HTTPS non-www version. The repository `.htaccess` includes a www-to-non-www 301 rule; HTTP-to-HTTPS appears to be supplied upstream. Exact status and hop count were not measurable in this environment.
- Search results still showed the older www/Hatton Garden snippets with crawl ages of one to five months. Live East London and homepage content was current after redirect. This supports stale indexing, not evidence of a second live document root. Search Console URL inspection remains necessary before declaring Google's selected canonicals. No speculative mass redirects or slugs changed.
- Sitemap parses and contains 192 unique URLs. The only root HTML file omitted is `index.html`, represented by `/`; the other omitted file is the deliberately redirected Sutton legacy alias. No missing or noindex sitemap destination was found in the local repository audit.

## QA and limits

- 23/23: one H1, canonical unchanged, Formspree form byte-equivalent in parsed HTML to the baseline, JSON-LD parses, visible/structured FAQs exactly match, internal links/images point to tracked files, and no noindex. Maximum pairwise five-word overlap among repaired pages is 18.5% with shared contact/quote facts included. This measures text overlap only and is not a ranking prediction.
- Desktop/mobile live visual QA and live byte verification of the new edits remain pending because the edited files are not deployed. The Hostinger browser displayed a Cloudflare security verification page after one reload; no bypass attempted. An automatic approval review rejected inspection of that challenge as a possible browser-security bypass. The shell has no GitHub write credentials, so connector publication is the safe repository route.
- Existing repeated generic hero imagery remains a quality limitation; source photos need separate visual review before location-specific identities can truthfully be assigned. No production change should be claimed from this checkpoint alone.
- After deployment, inspect Bromley, Brent, Bexley, Merton, Newham and Westminster first in Search Console, then the remaining revised borough URLs as quota permits. Check Google's selected canonical and live content; do not claim indexing merely from submission. Review old www examples only after a fresh crawl or URL inspection.

---
