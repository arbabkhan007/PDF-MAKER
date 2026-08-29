---
title: Markdown Rendering Reference
subtitle: Every block-level and inline construct, in one document
author: The WeasyPrint Team
date: 2026-08-29
kicker: Reference
description: A complete tour of the Markdown to PDF pipeline.
---

# Markdown Rendering Reference

This document exercises every Markdown construct the pipeline supports.
Use it as a rendering reference and as a visual smoke test.

## Inline formatting

Text can be **bold**, *italic*, ***bold italic***, ~~struck through~~,
and `monospaced`. There are special characters: «guillemets», em-dashes
— like this —, ellipses…, and math: Ω ≈ 3.14, ∑x², ∀ε > 0.

Links look like [ordinary links](https://example.com/docs) and bare
URLs stay plain: https://example.com.

## Headings

### Level-three heading

A short paragraph under the level-three heading.

#### Level-four heading

Another one, one level deeper.

## Lists

An unordered list:

- First bullet item
- Second bullet item with *italic* and **bold**
  - A nested bullet
    - A doubly nested bullet
- Third item

An ordered list:

1. Prepare the ingredients
2. Mix thoroughly
   1. Whisk the eggs
   2. Fold in the flour
3. Bake for 30 minutes

A task list:

- [x] Design the template
- [x] Write the stylesheet
- [ ] Print it on paper
- [ ] Frame it

Definition-style content can be embedded as HTML:

<dl>
  <dt>A4</dt>
  <dd>210 × 297 millimetres, the page size of this document.</dd>
  <dt>Orphan</dt>
  <dd>A line left alone at the bottom of a page.</dd>
</dl>

## Blockquotes

> A blockquote draws the eye with a thin accent line on its left,
> nothing more.

> It can also hold multiple paragraphs, and other elements:
>
> - like a list
> - or `inline code`
>
> > Blockquotes can be nested, too.

## Code

Inline code such as `weasyprint report.md report.pdf` blends into the
sentence. Fenced blocks get syntax highlighting:

```python
from dataclasses import dataclass

@dataclass
class Report:
    """A quarterly report."""
    title: str
    pages: int = 0

    def add_page(self) -> None:
        self.pages += 1
        return None

for quarter, pages in (("Q1", 12), ("Q2", 18)):
    report = Report(f"Report {quarter}", pages)
    print(f"{report.title}: {report.pages} pages")
```

A JavaScript block:

```javascript
const delay = (ms) => new Promise((resolve) => {
  setTimeout(resolve, ms);
});

async function main() {
  console.log("Waiting…");
  await delay(250);
  return "done";
}
```

A shell block:

```bash
pip install weasyprint
weasyprint --markdown README.md README.pdf
```

Unknown languages render as plain code, still nicely framed:

```
not a real language
  just indentation ~~~ ###
```

## Tables

| Feature      | Supported | Notes                                  |
|--------------|:---------:|----------------------------------------|
| Headings     | ✓         | H1–H6, with break control              |
| Tables       | ✓         | Header repeats across pages            |
| Code blocks  | ✓         | Pygments highlighting, rounded corners |
| Images       | ✓         | Scaled to the page width               |
| Unicode      | ✓         | Emoji 🚀, CJK 汉字, Arabic ﷲ           |

A right-aligned column: alignment set from the delimiter row is
honoured.

## Images

![A minimal bar chart drawn for the test suite](chart.png)

## Horizontal rules

Above the rule.

---

Below the rule.

## Embedded HTML

Markdown passes raw HTML through, and the stylesheet styles common
elements: <mark>highlighted text</mark>, <kbd>Ctrl</kbd> + <kbd>S</kbd>,
and <small>small print</small>.

<div style="border-left: 1.8pt solid #0e7568; padding-left: 12pt; color: #4d5561">
  Hand-written HTML blocks keep working, for the rare cases where
  Markdown is not expressive enough.
</div>

## The end

That is everything. If this document looks right, the pipeline is
healthy. 🎉
