Markdown documents
==================

WeasyPrint converts Markdown files into polished PDF documents with a
minimalist, premium editorial design — no configuration required::

    weasyprint report.md report.pdf

Markdown inputs are detected automatically from the file extension
(``.md``, ``.markdown``, ``.mdown``, ``.mkd``).  The ``--markdown``
option forces the Markdown mode for other inputs (such as URLs or
standard input), and ``--no-markdown`` disables the detection.

.. currentmodule:: weasyprint.markdown

The pipeline is Markdown → styled HTML → PDF:

1. an optional flat *front matter* block provides document metadata;
2. `markdown-it-py <https://github.com/hoffstadt/markdown_it_py>`_
   renders the body (CommonMark, plus GFM tables, strikethrough and
   task lists, typographic quotes), with
   `Pygments <https://pygments.org/>`_ syntax highlighting for fenced
   code blocks and raw HTML passed through;
3. the result is wrapped in a dedicated template and print stylesheet
   bundled with WeasyPrint;
4. the regular :class:`weasyprint.HTML` machinery lays out and writes
   the PDF.

The same steps are available from Python with the
:class:`~weasyprint.Markdown` class::

    from weasyprint import Markdown

    Markdown('report.md').write_pdf('report.pdf')

Supported constructs include headings, paragraphs, emphasis, ordered,
unordered and nested lists, links, images, tables, blockquotes, inline
code, fenced code blocks with syntax highlighting, horizontal rules,
task lists, strikethrough and embedded HTML.


Front matter
------------

A flat ``key: value`` block between ``---`` markers sets the document
metadata::

    ---
    title: Quarterly Report
    subtitle: Consolidated results
    author: Jane Doe
    date: 2026-08-29
    kicker: Finance
    description: Results for the second quarter.
    lang: en
    ---

- ``title`` is used on the cover and in the PDF metadata; when absent,
  the first level-1 heading — or the filename — is used instead.
- ``subtitle``, ``author`` and ``kicker`` (a short label above the
  title) are shown on the cover.
- ``date`` is displayed on the cover and, when it is an ISO date,
  stored as the PDF creation date, keeping the output deterministic.
- ``description`` becomes the PDF subject.
- ``lang`` (a BCP-47 tag) sets the document language.
- ``cover`` selects the first-page layout: ``auto`` (default) uses a
  full cover page unless the document is short, ``full`` and
  ``compact`` force a layout.

Unknown keys and richer YAML (lists, nesting) are ignored.


Page layout
-----------

- A4 pages with consistent margins.
- A minimalist cover page — or a compact letterhead-style title block
  for short documents.
- A quiet header with the document title on every content page.
- Page numbers in the footer, starting at 1 on the first content page.
- Headings never appear alone at the bottom of a page, table rows and
  code blocks are kept together when possible, and table headers
  repeat when a table spans pages.

The design uses the IBM Plex Sans and IBM Plex Mono typefaces, bundled
with WeasyPrint in ``weasyprint/resources/markdown/fonts`` alongside
compact fallback fonts, so that Unicode text, symbols and emoji render
consistently even on machines with few fonts installed.


Customising the design
----------------------

The template is driven by CSS custom properties.  A user stylesheet is
enough to change the accent color, for example::

    weasyprint report.md report.pdf \
        -s <(echo ':root { --accent: #b3261e; }')

All the tokens are defined at the top of
``weasyprint/resources/markdown/markdown.css``: ``--ink`` (body text),
``--muted``, ``--line``, ``--code-bg`` and ``--accent``.  The whole
stylesheet can also be overridden by copying it and adjusting the
``-s`` option.
