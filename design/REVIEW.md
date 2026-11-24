# Design review, November 24, 2026

*An expert walkthrough of the rebuilt site, written before showing it to scientists. Each finding is tied to published usability research or to a measurement, not to taste. Sources are at the end.*

## Method

Three people who will actually land on this site were walked through it with a task each, on desktop (1440px) and phone (390px):

| Who | Arrives from | Task | What decides it for them |
|---|---|---|---|
| **A pediatric sarcoma researcher** | A cold email link | Decide within a minute whether this is worth their time, then find the strongest lead and its evidence | Credibility, speed to evidence, whether claims can be checked |
| **A nonprofit science director** (the MIB Agents case) | An email reply, preparing for a meeting | Understand what this is and what is being asked of them | A clear ask, who is behind it, a way to get in touch |
| **A family member** | A text message | Understand what this is and why it exists | Plain language, the human reason |

Every screen they would see was captured, and page text, line length and link targets were measured.

## What the research says matters

- **First impressions are visual and fast.** People rate a page's visual appeal after 50 milliseconds, and those ratings match the ones they give after a longer look (Lindgaard et al., 2006).
- **On health sites, design drives rejection and content drives trust.** In studies of people searching for health information, 83% of comments about rejecting a site concerned design, while trust and choosing a site depended on content such as source credibility (Sillence et al., 2004 and 2005).
- **Trust has four signals:** design quality, up-front disclosure, comprehensive and current content, and connection to the rest of the web (Nielsen, 1999; still observed by Nielsen Norman Group). Stanford's credibility guidelines add: make it easy to verify the information, and show that there is a real organisation behind the site.
- **People scan.** They read headings and the start of lines, in an F shape or a "layer-cake" of headings; good headings and descriptive links are what let them scan well (Nielsen Norman Group).
- **Links need scent.** Link text should say what the reader will get; file names and "read more" give weak scent (Nielsen Norman Group).
- **Line length.** Body text reads best at about 45–75 characters a line (Bringhurst; Baymard puts it at 50–75).
- **Homepage.** State the value proposition with a descriptive tagline and hero content; limit prose (Nielsen Norman Group; usability.gov).
- **Audience-based navigation** ("For researchers / For families") usually fails: people don't know which group they belong to, and content overlaps (Nielsen Norman Group). It was considered here and rejected for that reason.

## Findings

Ranked by how much each one would cost the site with these three readers.

### Fixed in this pass

| # | Problem | Who it hurt | Evidence | Fix |
|---|---|---|---|---|
| 1 | **The Summary page rendered broken.** Nested lists showed as raw text ("Labels: - Confirmed: …"), and the Auditor's Guide showed stray "bash" text instead of code blocks. The Summary is the main button on the home page. | All three | Design quality is the first trust signal; visible breakage drives early rejection (Sillence) | Report pages are now built with a CommonMark parser, the standard GitHub uses, so they render as the source files do on GitHub |
| 2 | **Report text ran 91–93 characters a line.** | Researcher, family | 45–75 recommended (Bringhurst, Baymard) | Report text is 18px in a 600px column, now 67–71 characters a line; home page text 68–76. Tables still use the full width |
| 3 | **File names were the link text** ("HOW_THIS_WAS_MADE.md") and file paths appeared as dead code ("reports/Whats new … .md"). | Researcher, director | Weak information scent (NN/g) | File-name links show the page title; file paths written as code now link to the page or the file |
| 4 | **The top of every report showed a repository path** ("Report · reports/Ranked leads and research partners.md"). | Director, family | Plumbing, not content | Now reads "Report · Updated November 23, 2026 · 26 min read". The source link stays at the foot of the page |
| 5 | **The first screen had no up-front disclosure.** Nothing said this is version 1.0, open, not peer-reviewed. | Researcher | Up-front disclosure is a core trust signal (Nielsen) | A status line under the buttons: "Version 1.0 · Updated November 23, 2026 · Open data and code · Not yet peer-reviewed · Not medical advice" |
| 6 | **The ranking table hid the lead names.** Five number columns took equal width, so each lead wrapped across three lines, and a lead could not be clicked through to its explanation. | Researcher | Scanning and scent (NN/g) | Number columns are narrow and right-aligned; each lead now links to its section further down |
| 7 | **The hero chart had no plain statement of what it shows.** Its caption said only "One finding from the pooled trial record." | Family, director | Hero content should carry the value proposition (NN/g) | The caption now states the finding in one sentence, using the project's existing wording |
| 8 | **A "Theme" button sat in the main navigation**, looking like a second call to action. None of the ten reference sites put one there. | All | One clear main action (DESIGN.md) | Moved to the footer as "Dark mode / Light mode" |
| 9 | **The Explorer's search box started 560px down**, below a long introduction and a disclaimer. | Researcher | Tools should lead with the tool (Our World in Data puts search in the first screen) | The disclaimer moved into "How to read this" below the tool, with a one-line pointer kept at the top; the box now starts at 379px |
| 10 | **Page titles repeated the name** ("For John: One-Page Summary · For John"). | All | Front-loading the distinctive words helps scanning (NN/g) | Leading "For John:" removed from page titles |

### For Michael to decide

These touch his own words or personal details, so they are not changed without him.

| # | Issue | Evidence | Recommendation |
|---|---|---|---|
| A | **There is no way to contact a person.** The only route is a GitHub issue. Scientists and nonprofit staff will not open one; Kat replied by email. | Stanford: show there is a real organisation behind the site. NN/g: people expect an email address, not only a form | Publish a contact email. Best: an address at the new domain, such as michael@forjohnresearch.org, so a personal address is not exposed |
| B | **No photograph on the first screen.** Every charity in the reference set leads with a face. | Sillence: early judgments are visual. DESIGN.md rule 2 | The photo of Michael and John, when ready. The slot is built |
| C | **The introduction repeats itself.** "In memory of my little brother and best friend, John" is followed by "For John was created in honor of John Gegen", and the paragraph restates the headline ("connect the dots"). It is 60 words before the buttons. | Limit prose on a homepage (usability.gov, NN/g) | A tighter version for approval, keeping his phrases: "Researchers have spent decades building knowledge about osteosarcoma, often in separate labs, trials and journals. I'm leveraging frontier AI models to connect that work and carry it to the people who can test it." |
| D | **The headline** is still a draft. | Value proposition as a descriptive tagline (NN/g) | Approve or reword |
| E | **"Review This Work" opens with git commands.** Right for a scientist, wrong for anyone else who presses the brightest button on the page. | Scent: the label should predict the destination | Either keep it (the main audience is reviewers) or put the 18 key claims above the setup steps in the Auditor's Guide |

### Not yet tested

- **Real people.** This review is expert inspection, not a test with users. The meeting with MIB Agents is the first real test; watching Kat use the site for two minutes would outweigh this whole document.
- **Screen readers** were checked structurally (landmarks, headings, link names), not with an actual screen reader.
- **Every report in dark mode** shares one stylesheet; three pages were checked by eye.

## Sources

- Lindgaard, G., Fernandes, G., Dudek, C. and Brown, J. (2006). Attention web designers: you have 50 milliseconds to make a good first impression! *Behaviour & Information Technology* 25(2), 115–126. https://doi.org/10.1080/01449290500330448
- Sillence, E., Briggs, P., Fishwick, L. and Harris, P. (2004). Trust and mistrust of online health sites. *CHI 2004*. https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p663.pdf
- Sillence, E., Briggs, P., Fishwick, L. and Harris, P. (2005). Guidelines for developing trust in health websites. *WWW 2005*. https://archives.iw3c2.org/www2005/proceedings/docs/p1026.pdf
- Fogg, B. J. (2002). Stanford Guidelines for Web Credibility. https://credibility.stanford.edu/guidelines
- Nielsen Norman Group. Trustworthiness in web design: 4 credibility factors. https://www.nngroup.com/articles/trustworthy-design/
- Nielsen Norman Group. F-shaped pattern of reading on the web. https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- Nielsen Norman Group. Information scent. https://www.nngroup.com/articles/information-scent/ and Writing hyperlinks. https://www.nngroup.com/articles/writing-links/
- Nielsen Norman Group. Homepage design principles. https://www.nngroup.com/articles/homepage-design-principles/
- Nielsen Norman Group. Audience-based website navigation. https://www.nngroup.com/articles/audience-based-navigation/
- Nielsen Norman Group. Inverted pyramid. https://www.nngroup.com/articles/inverted-pyramid/
- Baymard Institute. Readability: the optimal line length. https://baymard.com/blog/line-length-readability
- Bringhurst, R. *The Elements of Typographic Style* (45–75 characters per line), as summarised at https://en.wikipedia.org/wiki/Line_length
- usability.gov (archived). Research-Based Web Design & Usability Guidelines, chapter 5: the homepage. https://webarchive.library.unt.edu/eot2008/20080916111221/http:/usability.gov/pdfs/chapter5.pdf
