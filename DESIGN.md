# For John design guide

*Written November 23, 2026. Every page on the site follows this guide. It is built from ten real websites in or next to our field, each visited and measured, not from memory. Change the guide first, then the pages.*

## How this was made, and its limits

- **What was done.** Sixteen sites were visited once each with an ordinary headless browser at 1440 × 900. Ten rendered properly and are the references below. For each one a first-screen and a full-length screenshot were taken, and the fonts, sizes, colours, widths and section padding were read from the live page.
- **What failed.** The Osteosarcoma Institute and Sarcoma Foundation of America did not connect. The Bone Cancer Research Trust, Alex's Lemonade Stand and the Broad Institute refused automated visits. MIB Agents loaded without its stylesheet, so it could not be judged. These six are not in the guide.
- **What to distrust.** Cookie banners were left in place, so they cover part of some first screens. A few images served from blocked hosts are missing (the Cancer Research UK logo, one Arc and one Simons image). Measurements are of the home page only.
- **Judgement.** "Looks great" is our call. Nine of the ten are strong. Children's Cancer Research Fund is the weakest visually and is included because it is the closest peer: a Minneapolis childhood-cancer charity that funds osteosarcoma research.
- **Screenshots** are in `design/references/` on the machine that made them and are not published in this repository, because they are other organisations' work. Raw measurements are in `design/references/_measurements.json` and `_layout.json`.

## The ten references

Sizes are `font-size / line-height`. Colours are the ones that carry the most text or area.

### 1. St. Jude Children's Research Hospital — stjude.org

- **Layout.** A white top bar with five menu items and two filled buttons on the right. The first screen is one photograph of a doctor and a child, with the headline in a white box laid over it. Directly beneath sit three equal action buttons. After that the page alternates photo-led story blocks with plain white sections. Content width 1,185px.
- **Type.** One custom sans (SJ Sans) for everything. Headline 62 / 72, bold. Section headings 27 / 31, bold, in blue. Body 23 / 34, which is large, on a 527px line.
- **Colours.** White page, black text, one blue (#135cb0) for headings, links and the main button, and one red for "Donate". Nothing else.
- **Spacing.** Roomy. Each story block is its own screen-height band with a soft grey divider.
- **Why it works.** A person's face comes before any claim. The headline is four words. There are exactly three things to do next.

### 2. Children's Cancer Research Fund — childrenscancer.org

- **Layout.** A fixed green column on the left holds the logo, a "Donate Now" button and seven links. The rest is a full-width photograph of a child with a campaign headline, then rows of three: story cards, then circular photos with a short caption and a button each.
- **Type.** One serif (Adobe Text Pro) throughout, at regular weight, even for headings (75 / 83 for the top line, 34 / 38 for section heads). Body 20 / 34 on a narrow 329px line.
- **Colours.** Olive green (#8fa143), a teal for links (#3f8da7), near-black text (#212121), light grey bands (#efefef).
- **Spacing.** Tight between cards, loose between sections. Three-across rows everywhere.
- **Why it works, and where it doesn't.** It is emotionally direct: a child, a sentence, one button. The single serif gives it warmth. The fixed side column, the dated green and the overlapping text on the photo are what not to copy.

### 3. CureSearch for Children's Cancer — curesearch.org

- **Layout.** A black top bar with six links and one outlined "Give" button. The first screen is split: headline and two buttons on the left, a photograph of a child on the right, cut on a slight diagonal. Then a purple band, a white band, a black quotation band, a pale lilac band. Content width 960px, with text columns held to 608px.
- **Type.** Montserrat only. Headline 70 / 72 at weight 800 with tight spacing (−2.1px), and the second half of the headline set at a lighter weight. Section headings 28 / 33, weight 800, in capitals. Body 17 / 27.
- **Colours.** One purple (#652872) used for nearly all text, with black (#14081a) and pale lilac (#f6f5fa, #e0d9e5) bands. A brighter purple (#a238ba) for accents.
- **Spacing.** Section padding 96px top and bottom, very consistent (64 / 96 / 96 / 96 / 115).
- **Why it works.** The line under the headline says exactly what they do: "We find the science most likely to become a treatment. Then we fund it." One colour, used with confidence, and a steady 96px rhythm.

### 4. Cancer Research UK — cancerresearchuk.org

- **Layout.** A white bar with a logo, "Search" and a filled "Donate", then a second row of six menus. The first screen is a full-width photograph of a scientist at a bench with a three-sentence headline over it. Below are plain white sections, each a heading, one line of text and two or three picture cards with a thin black outline and square corners.
- **Type.** A custom headline face (Progress) at 72 / 92, medium weight; section headings 42 / 58; card headings 22 / 32. Body in Poppins, 28 / 40 in the hero and smaller below. Menu items 18px at weight 600.
- **Colours.** White page, black text, navy (#00007e) and one magenta (#e60079) for buttons and links.
- **Spacing.** Very open: around 120px between sections, text held to 640–768px.
- **Why it works.** Three short sentences as the headline ("Making discoveries. Driving progress. Bringing hope."). Square outlined cards instead of soft shadowed ones. Two colours only.

### 5. Arc Institute — arcinstitute.org

- **Layout.** No big hero. The first screen is a headline, four short paragraphs on the left, and a scientific illustration (a DNA helix drawn in dots) on the right. Then "Featured Research": a list where each row is a date and journal in small monospace, topic tags, a thumbnail, a paper title and one line of summary. Then a solid blue band, then a white band, then a blue sign-up band.
- **Type.** A light serif (Tiempos Headline, weight 300) at 40 / 48 for headings, in blue or navy. IBM Plex Sans 16 / 24 for body on a 660px line, and 24 / 34 for paper titles. Monospace for dates and tags.
- **Colours.** Warm off-white page (#fbf8f2), navy text (#0c2043), one bright blue (#0073e6) for links and full-width bands, grey secondary text (#525b6b).
- **Spacing.** Dense text, wide margins. Text column 720px inside a 1,440px page.
- **Why it works.** It reads like a serious paper, not an advert. Headings are light, not bold. The research list is the centre of the page, and the metadata (date, journal, topic) is set apart in monospace so the eye can scan it.

### 6. Wellcome — wellcome.org

- **Layout.** A dark bar with the logo and five menus. First screen: headline, a short paragraph and one button on the left, one photograph with rounded corners on the right. Then story cards three across, a dark green "Wellcome in numbers" band with three large figures, a full-width photo band, three more cards, and a lilac newsletter band. Content width 1,344px.
- **Type.** A custom headline face (Wellcome) 44 / 57 at weight 600. Inter for section headings (26 / 39, weight 600) and body (16 / 24).
- **Colours.** Dark green-black (#223438), off-white (#f5f6ee), and lilac (#cac3fa, #edebfa) for buttons and bands. A small orange rule under the headline.
- **Spacing.** Sections padded 64px. Bands change colour instead of using lines.
- **Why it works.** Headline, one paragraph, one button, one image: nothing else on the first screen. The numbers sit as plain large figures on a colour band, not in boxes.

### 7. Our World in Data — ourworldindata.org

- **Layout.** A navy bar, then a row of topic chips. The first screen is a navy band with a two-line headline in gold, a large search box, and four small counters ("14,037 charts", "126 topic pages"). Below are small cards with a thumbnail chart each, then a wide row of four real charts, then a table of key indicators, then every topic listed as plain links.
- **Type.** Playfair Display for headings (32 / 40, weight 600) and Lato for everything else (body 14 / 21, menu 20 / 24). Small and dense by design.
- **Colours.** Navy (#002147, #1d3d63), gold (#f7c020), pale blue bands (#dbe5f0, #f0f4fa, #e7f2ff), red for "Donate".
- **Spacing.** Tight: 24px gutters, many items per screen. Content width 1,280px.
- **Why it works.** The data is the decoration. Real charts appear on the first scroll. The headline states the purpose in one sentence, and a line beneath says "All free: open access and openly licensed". This is the closest model for an open research project.

### 8. Simons Foundation — simonsfoundation.org

- **Layout.** A navy first screen with the logo top left, a menu row, and a mission paragraph set large. A short "Explore" list of four links sits at the left edge. Below: white sections titled with a small dot and label, each a grid of plain links or outlined cards; an "At a Glance" section of six large figures with captions, no boxes; then a yellow block on navy for funding.
- **Type.** A light serif (Tiempos Headline) at 41 / 45 for the mission paragraph, and a grotesque (Founders Grotesk) at 19.5px for menus and labels and 32px for card titles.
- **Colours.** Navy (#1d2954), warm off-white (#fcf6f1), white, and a single yellow accent.
- **Spacing.** Text columns 684–800px; outer width 1,252px. Large gaps between sections, thin rules inside them.
- **Why it works.** The mission paragraph is the hero: no slogan, no image needed. Navy and yellow with nothing else. Outlined square cards and plain figures.

### 9. Howard Hughes Medical Institute — hhmi.org

- **Layout.** A black first screen filled with a microscope image in green and blue. The headline sits over it on the left with three green action buttons; a white panel with a rounded top holds a short "about" text on the right. Lower sections alternate a photo on one side and a text panel on the other, then two news stories side by side, then a black footer.
- **Type.** A serif headline around 40px at regular weight; a heavy sans for panel headings; body around 15–16px. (The page builds its text in a way our reader could not measure, so these are read from the screenshot.)
- **Colours.** Black, white, one green for buttons, and the colours of the science imagery itself.
- **Spacing.** Full-height bands; text panels about 300px wide beside large images.
- **Why it works.** Real scientific imagery carries the page. The headline is a full sentence. Only three choices are offered on the first screen.

### 10. Distill — distill.pub

- **Layout.** A thin dark bar with three links. The whole page is one list of articles. Each row has a date and a small "peer-reviewed" tag on the left, the title, authors and a two-line summary in the middle, and a diagram from the article on the right. A hairline separates rows.
- **Type.** System sans. Titles 26 / 31 at weight 700; summaries 16 / 24 on a 394px line; dates and tags around 11px.
- **Colours.** White, black, one dark teal (#0f2e3d) for the bar and tags. Colour comes only from the diagrams.
- **Spacing.** About 40px of padding per row; content held to roughly 1,000px.
- **Why it works.** It is the best model for a list of research reports: date, status, title, authors, summary and a figure, in that order, every time. Nothing else is on the page.

## What the ten have in common

These are the rules the references agree on. Each one is followed on every For John page.

1. **A sentence comes first, not a name.** Eight of ten open with a statement of what the organisation does. The name lives in the top bar as a small wordmark.
2. **A real image is on the first screen.** A person (St. Jude, CureSearch, Cancer Research UK, Children's Cancer Research Fund) or real science (Arc, HHMI, Our World in Data, Distill). None uses abstract decoration.
3. **One main colour and one accent.** Navy with gold (Our World in Data, Simons), purple (CureSearch), blue with red (St. Jude), navy with magenta (Cancer Research UK). Colour is used in large flat areas. No gradients.
4. **Sections are colour bands.** Background changes mark a new section. Lines are used only inside lists.
5. **A top bar with four to six links and one filled button.** Every site has a single obvious main action.
6. **Research is shown as a list with metadata.** Arc and Distill: date, type or status, title, one line, a figure.
7. **Numbers are plain large figures.** Simons, Wellcome and Our World in Data set them directly on the page or on a band with a caption beneath. None boxes them.
8. **Corners are square or barely rounded.** Outlined cards with 0–4px corners (Cancer Research UK, Simons, CureSearch). Fully rounded shapes appear only on buttons, and only on some sites.
9. **Research institutes use a light serif for headings.** Arc and Simons both use Tiempos Headline at weight 300, around 40px. Charities use a heavy sans at 60–75px. Body text is 16–23px with a line-height of about 1.5.
10. **Text lines stay short.** 530–720px for body text, inside a page 960–1,344px wide.

## The For John system

For John is an open research project with a personal reason behind it. It sits between the institutes (Arc, Simons, Our World in Data, Distill) and the charities (St. Jude, CureSearch). The system takes its structure from the institutes and its directness from the charities.

### Colour

| Role | Value | Source |
|---|---|---|
| Navy, main colour | `#14264a` | Simons `#1d2954`, Our World in Data `#002147`, Arc `#0c2043` |
| Gold, the one accent | `#f7c020` | Our World in Data; also the sarcoma awareness colour |
| Page | `#fbf8f2` | Arc |
| Paper, for cards and alternate bands | `#ffffff` | all |
| Pale band | `#eef2f7` | Our World in Data `#f0f4fa` |
| Ink, body text | `#14181f` | Arc `#11181c` |
| Secondary text | `#525b6b` | Arc |
| Link | `#1c5cab` on light, `#f7c020` on navy | St. Jude blue; gold on navy as Our World in Data |
| Confirmed / Lead / Hypothesis | `#0e6b4a` / `#1a5494` / `#a3401a` | ours; always shown with the word |

- Navy and gold only. Gold is for the main button, key figures and the active menu item, never for body text on a light background.
- Colour goes on in flat bands. No gradients, no glows, no shadows deeper than a hairline.
- Chart colours stay as they are (blue `#2a78d6`, orange `#eb6834`), because they were checked for colour-blind readers.

### Type

| Use | Face | Size / line-height | Weight |
|---|---|---|---|
| Statement headline | Source Serif 4 | 52 / 60 desktop, 34 / 40 phone | 300 |
| Section heading | Source Serif 4 | 36 / 44 desktop, 27 / 34 phone | 300 |
| Report or card title | IBM Plex Sans | 22 / 30 | 500 |
| Lede paragraph | IBM Plex Sans | 20 / 31 | 400 |
| Body | IBM Plex Sans | 17 / 27 | 400 |
| Small text, captions | IBM Plex Sans | 14.5 / 22 | 400 |
| Dates, labels, metadata | IBM Plex Mono | 13 / 18 | 400 |
| Large figures | Source Serif 4 | 56 / 60 | 300 |

- Source Serif 4 at light weight is the free face closest to the Tiempos Headline used by Arc and Simons. IBM Plex Sans is what Arc uses for body text.
- Headings are light, not bold. No capitals for headings. No italic or coloured word inside a headline.
- Title case for headings, titles, menus and buttons. Sentence case for everything else.
- Body text runs about 65–75 characters a line: 18px in a 600px column on report pages, 17px in 560–580px on the home page. Measure it; the `ch` unit overstates the width in this typeface.

### Spacing and layout

- **Scale:** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px. Nothing in between.
- **Sections:** 96px top and bottom on desktop, 56px on phones (CureSearch's rhythm).
- **Page width:** 1,200px, with 32px side padding (20px on phones). Text columns 680px.
- **Grid:** 12 columns, 24px gutters. Lists use a narrow metadata column (2 of 12) beside the content.
- **Corners:** 4px on buttons and cards. Nothing fully rounded.
- **Borders:** 1px `#d9dde5` for outlined cards and list rows.

### Parts

- **Top bar.** Navy, on every page. "For John" wordmark on the left in the serif. Four links: Findings, Reports, Evidence Explorer, Methods. One gold button on the right: "Review This Work".
- **First screen.** Navy band. A one-sentence statement headline, the dedication beneath it, a short paragraph, and two buttons (gold "Read the Summary", outlined "See the Ranked Leads"). The right half holds a real image: a photograph of John if the family wants one there, otherwise the project's own chart.
- **Figures.** A single row of plain large numerals on the page with a caption under each, as Simons does. No boxes, no icons.
- **Findings and reports.** The Arc and Distill list: a mono column with the label or date, then the title, one line of text and a link. A figure on the right where one exists.
- **Bands.** Alternate page colour, white and pale blue. One navy band per page at most besides the top bar and first screen.
- **Buttons.** Filled gold with navy text for the main action; outlined for the second. 4px corners, 16px text at weight 500, 14px by 24px padding.
- **Report pages.** Top bar, a title in the serif, a mono line of metadata (type, date, source file), a 680px text column, and the contents list on the left.
- **Footer.** Navy, two short lines, the licence and "Not medical advice".

### Do not

- Use gradients, glows, glass panels or decorative shapes.
- Put statistics in a row of cards.
- Use a small capitalised label above a heading.
- Use more than two typefaces plus the mono, or more than navy and gold.
- Open a page with the project's name as the headline.
- Use stock photography or generated images. Real photos, real charts, or nothing.
- Round corners past 4px.

### Before a page ships

1. First screen: one sentence, one image, one main button.
2. Only navy, gold and the neutrals appear, apart from charts and the three evidence labels.
3. Headings are Source Serif 4 at weight 300; everything else is Plex.
4. Every gap is a value from the spacing scale.
5. Body text is 65–75 characters a line (measure it).
6. Works at 320, 390, 768 and 1,440px wide with no sideways scrolling.
7. Light and dark versions both checked, text contrast 4.5:1 or better.
8. No item on the "Do not" list is present.

## Where the system lives

- `docs/site.css` holds the shared colours, type, top bar, buttons and footer. Every page loads it.
- `docs/index.html` (home), `docs/doc.css` with `tools/build_site.py` (report pages) and `docs/explorer.html` add only what is particular to them.
- A left-margin section list appears on the home page on very wide screens (1,680px and up). It is an addition to the references, kept because it helps on a long page.

*A research-backed review of the rebuilt site, with what was fixed and what is left, is in `design/REVIEW.md`.*

## Pending

These are waiting on a decision or on something only the family can supply. The site works without them.

| Item | Status | What happens meanwhile |
|---|---|---|
| A photograph on the first screen | Done November 24, 2026: John on Michael's shoulders (`docs/john-and-michael.jpg`); John's portrait is in About John | The chart is back in its own section. A sharper original of the photo would help on large screens. |
| The headline sentence | Settled November 24, 2026: "Turning decades of osteosarcoma research into new ideas, tested and published." | — |
| A short web address (for example forjohn.org) | Not bought | The site stays at mgegen15-dev.github.io/For_John. |
| An outside review of the design | Not run | An AI usability test (TheySaid) is connected and can be run on the live site once approved. |
| Dark-mode check of every report page | Home, one report and the explorer checked | The rest share the same stylesheet. |
| A contact email on the site | Waiting for a decision on which address | Contact is a GitHub issue only. An address at the new domain would avoid publishing a personal one. |
| Tighter homepage introduction | Done November 24, 2026 | — |
