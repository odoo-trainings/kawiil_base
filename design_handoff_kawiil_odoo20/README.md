# Handoff: K'awiil Motors website (Odoo 20)

## Overview
This package contains the website designs for K'awiil Motors, a San Francisco maker of electric motorcycles that sells direct and offers in-house financing. There are 7 pages: Home, the three bike pages (Raijin, Ukko, Indra), Financing, About, and Book a test ride / contact. Each page is designed at desktop and mobile size.

The target is the **Odoo 20 website builder**, so K'awiil staff can keep editing the site after handover.

## About the design files
The `.dc.html` files are **design references built in HTML**. They show the intended look, content and layout. They are not production code to copy.

The job is to rebuild them in Odoo 20: a theme module (palette, fonts and options) plus pages built from Odoo's standard building blocks (snippets). Every section is tagged in the design with the snippet it maps to, for example `s_cover` or `s_numbers`.

To view a design, open any `.dc.html` file in a browser, served from this folder so the relative paths work (for example `npx serve .`). Each file shows the desktop frame (1440 px) next to the mobile frame (390 px). `support.js`, `image-slot.js` and `_ds/` are only needed to render the previews.

## Fidelity
**High fidelity.** Colours, type, spacing, copy and images are final unless marked otherwise in HANDBACK.md §3 (Images) and §5 (Deviations). Where Odoo can't reproduce a detail, follow the fallback listed in HANDBACK.md §5 rather than writing custom code.

## Files
| File | What it contains |
|---|---|
| `HANDBACK.md` | **Source of truth.** Design tokens, logo files, image map, all headlines and button labels, and deviations. |
| `KAwiil Home.dc.html` | Home: s_cover → s_three_columns → s_numbers → s_image_text → s_cta_box → s_quotes_carousel → s_call_to_action |
| `KAwiil Raijin.dc.html` | Bike template: s_cover → s_numbers → s_features_grid → s_comparisons → s_three_columns → s_cta_box → s_faq_collapse |
| `KAwiil Ukko.dc.html`, `KAwiil Indra.dc.html` | The same template with each bike's own figures and images |
| `KAwiil Financing.dc.html` | s_banner → s_process_steps → s_comparisons → s_key_benefits → s_faq_collapse → s_call_to_action |
| `KAwiil About.dc.html` | s_hero_about → s_text_image → s_timeline → s_three_columns (optional) → s_company_team |
| `KAwiil Test Ride.dc.html` | s_website_form → s_contact_info → s_google_map |
| `logo/` | Logo as outlined SVG and 600 × 160 PNG (on-dark, on-light, mono-night, mono-white), plus the favicon as 256 × 256 PNG and SVG |
| `uploads/`, `images/` | All page images. See the image map in HANDBACK.md §3 |

## Design tokens (summary; full table in HANDBACK.md §1)
- **Palette:**
  - o-color-1 `#0B7A64` Jade (primary)
  - o-color-2 `#9FF0D0` Mint Arc (secondary)
  - o-color-3 `#EEF3F1` Mist (light sections)
  - o-color-4 `#FFFFFF` (page)
  - o-color-5 `#0A0F1F` Night (text, dark sections)
- **Fonts (Google):** Barlow 400/500/600 for body. Barlow Condensed 600/700 for headings, navigation and buttons.
- **Sizes:** base font 17 px, button radius 0, button padding 12/28 px (large 16/34).
- **Layout:** image radius 0, full page width, container 1140.
- **Header:** default layout, border-bottom link style, background o-color-5, CTA button "Book a test ride" in o-color-1.
- **Footer:** built-in links template, background o-color-5.
- **Section padding:** 112 px desktop, 56 px mobile.
- **Contrast:** white on Jade is 5.3:1, Night on Mint is 14:1. Mint is never used as text on white.

## Suggested implementation
1. **Theme module** (`theme_kawiil`). Put these in `static/src/scss/primary_variables.scss`:
   - a K'awiil entry in `$o-color-palettes` with the 5 colours;
   - a `$o-website-values-palettes` entry with: fonts (body Barlow; headings, navbar and buttons Barlow Condensed), header template `default`, header links style `border-bottom`, the links footer template, button radius 0 and button padding, and the base font size.
   
   Register both Google fonts in `$o-theme-font-configs`. Check the exact variable and key names against `website/static/src/scss/primary_variables.scss` in 20.0.
2. **A small custom stylesheet**, the only custom CSS needed. It makes h1–h4, `.nav-link` and `.btn` uppercase, with letter-spacing 0.08 em on buttons and nav links. Headings use line-height 0.92 for h1 and 1 for h2.
3. **Pages** as QWeb page records, or built in the editor, using the snippets listed in the Files table and the copy in HANDBACK.md §4. Build the Raijin page once, then duplicate it for Ukko and Indra.
4. **Logo and favicon:** set them from `logo/`. Use the on-dark logo in the header and footer.
5. **Shop:** keep Odoo's standard eCommerce layout. Product variants are the three colours (Jade Arc, Night Strike, Storm White), and product images are the Mist-background side views.

## Interactions and behaviour
All behaviour is standard Odoo:
- The header's Models item is a dropdown (Raijin, Ukko, Indra).
- The FAQ items are collapsible, with the first one open.
- The quotes carousel shows 3 slides with indicators.
- The test ride form uses s_website_form with these fields:
  - Name, Email and Phone (required);
  - Model, required, a select with Raijin, Ukko and Indra;
  - Preferred date, required, a date field;
  - Message, optional.
  
  Send submissions to a CRM lead or an email, as the client prefers.
- The Financing page's **Apply for financing** button links to the loan application, which will be built later. Use a placeholder URL.
- On mobile, every section stacks into one column and the header collapses into the standard hamburger menu.

## Rules that must not be broken
- The fourth model, **Xolotl**, must not appear anywhere on the site.
- Every monthly payment shown must have its APR, term and down payment next to it. Example: "8.99% APR, 60 months, 10% down. Example only, subject to credit approval."
- Bikes are never cropped at the wheels.

## Open items
- Two images are still missing: the Financing banner (F-1) and the About intro workshop shot (A-1).
- The home page rider quotes are sample copy.
- Remove the brand text on some bike images before launch ("brembo" and "Pirelli" on Raijin, "E-Commuter" on the Indra battery).
