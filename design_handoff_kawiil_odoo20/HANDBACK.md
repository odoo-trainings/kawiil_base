# K'awiil Motors: design handback for the Odoo 20 build

Direction: **2a Night Jade**. Page designs, desktop (1440 px) and mobile (390 px):
`KAwiil Home` · `KAwiil Raijin` · `KAwiil Ukko` · `KAwiil Indra` · `KAwiil Financing` · `KAwiil About` · `KAwiil Test Ride` (all `.dc.html`). Each section is tagged with its Odoo block.

---

## 1. Design tokens

| Token | Value |
|---|---|
| o-color-1 (primary) | #0B7A64 |
| o-color-2 (secondary) | #9FF0D0 |
| o-color-3 (light background) | #EEF3F1 |
| o-color-4 (page background) | #FFFFFF |
| o-color-5 (dark / text) | #0A0F1F |
| Body font | Barlow 400, 500, 600 |
| Headings font | Barlow Condensed 600, 700 |
| Navigation and button font | Headings (Barlow Condensed 600 / 700) |
| Base font size | 17 px |
| Button radius | 0 |
| Button padding (vertical / horizontal) | 12 / 28 (large buttons: 16 / 34) |
| Header layout + link style | default + border-bottom |
| Header background | o-color-5 |
| Footer background | o-color-5 |
| Page width | full |
| Image corner radius | 0 |
| Bike colour names and hex | Jade Arc #0B7A64 · Night Strike #0A0F1F · Storm White #E8ECEA. Strike line on every bike: Strike Yellow #F2C818 (images only) |

**Colour rules**
- Primary button: o-color-1 with white text (5.3:1).
- Secondary button: o-color-2 with o-color-5 text (14:1).
- On o-color-1 sections, the button is o-color-5 with white text.
- On dark sections, all text is white. Accents use o-color-2, which is never used as text on white.
- Header link active state: 3 px o-color-2 border-bottom. Header CTA button: o-color-1, "Book a test ride".

**Type sizes (desktop / mobile)**
- H1: 104–144 / 56–88 px, Barlow Condensed 700, uppercase, line-height 0.9.
- H2: 56 / 38 px, 700, uppercase, line-height 1.
- H3: 26–32 / 22–28 px, 700, uppercase.
- Eyebrow labels: 15–16 px, 600, uppercase, letter-spacing 0.2 em, o-color-1 (o-color-2 on dark).
- Body: 17–18 px Barlow 400, line-height 1.5.
- Small print: 14–15 px.

**Spacing:** sections have 112 px vertical padding (96 on dark bands) on desktop and 56 px on mobile. Container width is 1140.

---

## 2. Logo and favicon (folder `logo/`)

The type is converted to outlines, so no font is needed to display these files.
- `kawiil-logo-on-dark.svg` / `-600x160.png`: Mint Arc strike, white wordmark. **Use this in the header and footer.**
- `kawiil-logo-on-light.svg` / `-600x160.png`: Jade strike, Night wordmark.
- `kawiil-logo-mono-night.svg` / `.png` and `kawiil-logo-mono-white.svg` / `.png`: one-colour versions.
- `kawiil-favicon-256.png` (and `.svg`): Mint Arc strike on a Night square.

All PNG logos have transparent backgrounds. Recommended logo height is 28–32 px in the header and 22 px on mobile.

---

## 3. Images (folder `uploads/`, plus `images/`)

| Where | File |
|---|---|
| Home hero (s_cover) | h-1.jpeg |
| Home line-up | P-R1.jpeg, P-U1.jpeg, P-I1.jpeg |
| Home charging (s_image_text) | H-5.jpeg |
| Raijin hero / colours | b-r1.jpeg · P-R1 (Jade Arc), P-R2 (Night Strike), P-R3 (Storm White) |
| Ukko hero / colours | Gemini_Generated_Image_9obpw29obpw29obp.jpeg · images/P-U1-right.png (Jade Arc), P-U2, P-U3 |
| Indra hero / colours | Gemini_Generated_Image_ch3xizch3xizch3x.jpeg · P-I1 (Jade Arc), P-I2, P-I3 |
| About story (s_text_image) | Gemini_Generated_Image_s7it03s7it03s7it.jpeg |
| About team | itzel.jpeg, tomas.jpeg, diego.jpeg, arjun.jpeg |
| **Still missing** | Financing banner (F-1) and About intro workshop (A-1) |

Before launch, remove the brand text still visible on some images: "brembo" and "Pirelli" on the Raijin images, and "E-Commuter" on the Indra battery. Rename the files to their IDs when uploading to Odoo.

**Shop and product pages:** use the Odoo eCommerce layout as it is. Product images are the Mist-background side views, one per colour variant. Keep them square with the bike centred and the whole bike in frame. Prices are set in Barlow Condensed 700, and the Add to cart button is o-color-1.

---

## 4. Copy: headlines and button labels

**Header (all pages):** Models (Raijin, Ukko, Indra) · Financing · Shop · About · button **Book a test ride**

**Footer:**
- Tagline: "Electric motorcycles, designed, assembled and financed in San Francisco."
- Columns: Models (Raijin, Ukko, Indra) · Company (Financing, Shop, About) · Showroom (4100 Thunderbird Road, San Francisco, CA 94107, +1 555-0100, Book a test ride)
- Bottom line: © 2026 K'awiil Motors · Privacy · Terms

### Home
1. **Hero.** Eyebrow: "Electric motorcycles · San Francisco". H1: "Silent. Sudden. Electric." Line: "Raijin, Ukko and Indra, sold direct with in-house financing. From $11,500." Buttons: **Explore models** / **Book a test ride**.
2. **Line-up.** H2: "Three bikes. One charge cable." Link: **Compare models**.
   - Raijin: From $24,000 · "The flagship sport bike. 15 or 20 kWh." · **View Raijin →**
   - Ukko: From $21,000 · "All-terrain adventure, tarmac to gravel. 17 or 23 kWh." · **View Ukko →**
   - Indra: From $11,500 · "The urban commuter, light and quick. 7 or 11 kWh." · **View Indra →**
3. **Numbers.** 215 mi "City range, Raijin Extended" · 25 min "20–80% DC fast charge, Raijin Standard" · 150 mph "Top speed, Raijin" · 0 g "Tailpipe emissions".
4. **Charging.** Eyebrow: "Charging at home". H2: "Your garage is the fuel station." Points:
   - **Full in 2.5 hours.** Raijin Standard, 0–100% on a 6.6 kW Level 2 wall charger.
   - **No garage? No problem.** Indra's battery comes out and charges indoors from a 120 V household outlet.
   - **Fast charge on the road.** Raijin and Ukko go from 20–80% in 25–35 minutes at public DC chargers.
5. **Financing teaser.** Eyebrow: "In-house financing". H2: "Ride from $215/month". Small print: "Indra Standard, $11,500. 8.99% APR, 60 months, 10% down. Example only, subject to credit approval." Button: **See financing**.
6. **Quotes.** 3 testimonials. Currently sample copy: "Twenty years on petrol bikes. One ride on the Raijin and I sold my old one." Marcus T. · Raijin owner, Oakland. **Replace with real quotes.**
7. **Closing call to action.** H2: "Ride one before you decide." Line: "Test rides at our Dogpatch showroom, 4100 Thunderbird Road, San Francisco." Button: **Book a test ride**.

### Bike pages (Raijin / Ukko / Indra)
1. **Hero.** Eyebrow: Flagship sport bike / All-terrain adventure / Urban commuter. H1: model name. Line:
   - Raijin: "Thunder, without the noise. From $24,000."
   - Ukko: "Sky and thunder, on any road. From $21,000."
   - Indra: "Lightning for the city. From $11,500."
   
   Buttons: **Buy [Model]** / **Book a test ride**.
2. **Specs at a glance.**
   - Raijin: 215 mi · 147 hp (110 kW) · 2.9 s · 25 min DC
   - Ukko: 210 mi · 121 hp (90 kW) · 3.6 s · 30 min DC
   - Indra: 145 mi · 34 hp (25 kW) · 5.9 s · 2.3 h Level 2
3. **Features.** H2:
   - Raijin: "Built for the fast line."
   - Ukko: "Built to leave the pavement."
   - Indra: "Built for the daily ride."
   
   Six features per bike, as shown in each page.
4. **Battery options.** H2: "Choose your battery." Standard / Extended tables. Buttons: **Buy Standard** / **Buy Extended**.
5. **Colours.** H2: "Three colours." Jade Arc · Night Strike · Storm White.
6. **Finance.** H2: "Finance this bike from $448/month" (Raijin), "$392/month" (Ukko) or "$215/month" (Indra). Small print: "[Model] Standard, $[price]. 8.99% APR, 60 months, 10% down. Example only, subject to credit approval." Button: **See financing**.
7. **FAQ.** H2: "Questions". Five questions:
   - How far does [Model] go on a charge?
   - How long does charging take?
   - What does the warranty cover?
   - Can I ride one before I buy?
   - Can I finance [Model]?
   
   The answers are written out at the bottom of each bike page file.

### Financing
1. **Banner.** Eyebrow: "K'awiil Financing". H1: "Ride now. Pay monthly." Line: "K'awiil Financing offers fixed-rate loans from $215 a month, with 10% down." Plus the disclosure.
2. **How it works.** H2: "How it works". Steps: Choose your bike · Apply online · Get a decision · Ride (step text as in the brief).
3. **Example plans.** H2: "Example plans". Raijin Standard, $2,400 down: 36 months $667 (6.99%) · 48 months $527 (7.99%) · 60 months $448 (8.99%). Badge: "Lowest monthly".
4. **What you need.** H2: "What you need" (the 4 points from the brief).
5. **FAQ.** H2: "Questions". Five questions:
   - How quickly will I get a decision?
   - What are the interest rates?
   - How much can I borrow?
   - Can I pay the loan off early?
   - Can I include gear or a service plan?
6. **Apply.** H2: "Apply in 10 minutes." Line: "Online application, decision within 1 business day." Button: **Apply for financing**.

### About
1. **Intro.** Eyebrow: "About K'awiil". H1: "Lightning is the one force every culture has a god for." Then the rest of the intro as written.
2. **Story.** Eyebrow: "Our story". H2: "From a Mission District garage to Thunderbird Road." Then the 5 paragraphs as written.
3. **Milestones.** H2: "Milestones" (2018–2026, as written).
4. **What we stand for** (optional). H2: "What we stand for". Performance first · Built and serviced here · Ownership made simple.
5. **Team.** H2: "The team". Four people, as written.

### Book a test ride
1. **Form.** Eyebrow: "Test rides". H1: "Book a test ride."
   - Line: "Pick a bike and a day. We'll confirm your slot by email and have the bike charged and ready at the Dogpatch showroom."
   - Note: "Bring your motorcycle licence or endorsement."
   - Fields: Name *, Email *, Phone *, Model * (Raijin / Ukko / Indra), Preferred date *, Message.
   - Button: **Book my test ride**.
2. **Showroom.** H2: "The showroom".
   - Address: 4100 Thunderbird Road, San Francisco, CA 94107
   - Hours: Mon–Sat, 10 am – 5 pm
   - Phone and email: +1 555-0100 · info@kawiil.example.com
3. **Map.** s_google_map centred on the showroom address.

---

## 5. Deviations and things to check

Every section uses its listed block. These details go beyond the theme options:

1. **Uppercase headings, nav and buttons.** Odoo's theme options have no text-transform setting. Either add a few lines of custom CSS (h1–h4, .nav-link, .btn, uppercase with 0.08 em letter-spacing), or type the text in capitals.
2. **FAQ layout, bike pages and Financing.** The design puts the heading in a 4-column block on the left and the questions in 8 columns on the right. If the s_faq_collapse variant in 20.0 can't split like this, put the heading above the questions.
3. **Map.** The design shows the map in greyscale. s_google_map uses Google's default colours, so accept those.
4. **Mobile menu icon.** The design shows the third line of the icon in Mint Arc. Use Odoo's default hamburger icon; this is not worth custom code.
5. **Header button on the Book a test ride page.** The design shows it in Mint Arc on that page only. Keep it o-color-1 on every page, since the header is shared.
6. **About hero bottom band.** The workshop image sits on a dark band that runs into the next section. Build it as s_hero_about with an o-color-5 background, then start the next section on white.
7. **Bike page template.** Build Raijin once, save it as a custom block or page template, and duplicate it for Ukko and Indra. Only the text and images change.

Everything else uses standard options: column borders for the number rules, the icon background shape for the feature tiles, and s_hr for the thin Mint Arc line in the heroes.
