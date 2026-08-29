"""Test the Markdown to PDF pipeline.

These tests exercise the Markdown class and the command-line Markdown
mode without rasterizing: they check the generated HTML, the document
structure (pages, metadata) and the generated PDF bytes.
"""


from weasyprint import HTML, Markdown, __version__
from weasyprint.markdown import (
    MARKDOWN_EXTENSIONS,
    build_html,
    parse_front_matter,
    render_markdown,
)

from .testing_utils import assert_no_logs

SAMPLES = 'tests/resources/markdown'


def render_string(source, **kwargs):
    return Markdown(string=source, **kwargs).render()


def test_version():
    assert __version__


@assert_no_logs
def test_front_matter_parsing():
    text = '---\ntitle: My Doc\nauthor: "Jane"\n# comment\nlang: fr\n---\nBody'
    body, metadata = parse_front_matter(text)
    assert body == 'Body'
    assert metadata['title'] == 'My Doc'
    assert metadata['author'] == 'Jane'
    assert metadata['lang'] == 'fr'


def test_front_matter_unclosed():
    body, metadata = parse_front_matter('---\ntitle: No end\n\nBody')
    assert 'title' in body
    assert metadata == {}


def test_front_matter_invalid_line():
    body, metadata = parse_front_matter('---\nnot a pair\n---\nBody')
    assert metadata == {}


@assert_no_logs
def test_first_h1_becomes_title():
    body, title = render_markdown('# Hello\n\nWorld')
    assert title == 'Hello'
    assert '<h1' not in body
    assert '<p>World</p>' in body


@assert_no_logs
def test_markdown_features_html():
    source = (
        '# T\n\n'
        '**bold** *italic* ~~gone~~ `code`\n\n'
        '- a\n- b\n  - c\n\n'
        '1. one\n2. two\n\n'
        '[link](https://example.org)\n\n'
        '> quote\n\n'
        '---\n\n'
        '| a | b |\n|---|:-:|\n| 1 | 2 |\n\n'
        '```python\nif x:\n    return 1\n```\n\n'
        '- [ ] todo\n- [x] done\n\n'
        '<div class="x">html</div>\n')
    markdown = Markdown(string=source, base_url='.')
    html = markdown.html_string
    for expected in (
            '<strong>bold</strong>',
            '<em>italic</em>',
            '<s>gone</s>',
            '<code>code</code>',
            '<li>a</li>',
            '<li>b\n<ul>\n<li>c</li>',
            '<ol>\n<li>one</li>',
            '<a href="https://example.org">link</a>',
            '<blockquote>\n<p>quote</p>',
            '<hr />',
            '<table>',
            '<th style="text-align:center">b</th>',
            '<div class="x">html</div>',
            '<span class="checkbox checked"></span>',
            '<span class="checkbox"></span>'):
        assert expected in html, expected
    assert '<input' not in html
    assert 'class="k"' in html  # Pygments keyword token


@assert_no_logs
def test_unknown_code_language_is_plain():
    markdown = Markdown(string='# T\n\n```nope\nx < 1\n```', base_url='.')
    assert '<pre><code class="language-nope">x &lt; 1\n</code></pre>' \
        in markdown.body_html


@assert_no_logs
def test_table_alignment_propagates():
    markdown = Markdown(string=(
        '| a | b |\n|:-:|---|\n| 1 | 2 |\n\n'
        '<table><thead><tr><th>x</th></tr></thead><tbody><tr><td>y</td>'
        '</tr></tbody></table>'), base_url='.')
    assert '<td style="text-align:center">1</td>' in markdown.body_html
    # Hand-written tables are left untouched.
    assert '<td>y</td>' in markdown.body_html


@assert_no_logs
def test_compact_first_page():
    # Short documents keep the title block on the first page.
    markdown = Markdown(string='# Note\n\nShort body.')
    assert 'cover compact' in markdown.html_string
    document = markdown.render()
    assert len(document.pages) == 1


@assert_no_logs
def test_full_cover_for_long_documents():
    source = '# Report\n\n' + 'A paragraph.\n\n' * 100
    markdown = Markdown(string=source, base_url='.')
    assert '<div class="cover">' in markdown.html_string
    assert 'cover compact' not in markdown.html_string
    assert len(markdown.render().pages) >= 2


def test_cover_mode_override():
    source = '---\ncover: full\n---\n\n# Small\n\nBody.'
    markdown = Markdown(string=source, base_url='.')
    assert '<div class="cover">' in markdown.html_string


@assert_no_logs
def test_cover_metadata():
    markdown = Markdown(string=(
        '---\n'
        'title: The Title\n'
        'subtitle: The Subtitle\n'
        'author: Jane Doe\n'
        'date: 2026-08-29\n'
        'kicker: Report\n'
        '---\n\nBody'))
    html = markdown.html_string
    assert '<title>The Title</title>' in html
    assert '<meta name="author" content="Jane Doe">' in html
    assert '<meta name="dcterms.created" content="2026-08-29">' in html
    assert 'cover-kicker">Report' in html
    assert 'cover-subtitle">The Subtitle' in html
    assert markdown.metadata['title'] == 'The Title'
    document = markdown.render()
    assert document.metadata.title == 'The Title'
    assert document.metadata.authors == ['Jane Doe']
    assert document.metadata.created == '2026-08-29'


def test_cover_metadata_escaping():
    markdown = Markdown(string=(
        '---\ntitle: <script>alert(1)</script>\n---\n\nBody'))
    assert '<script>' not in markdown.html_string
    assert '&lt;script&gt;' in markdown.html_string


def test_title_from_filename():
    markdown = Markdown(filename=f'{SAMPLES}/pattern.md')
    assert markdown.title == 'Pixel the Axolotl'
    document = render_string('# Only Heading')
    assert document.metadata.title == 'Only Heading'


@assert_no_logs
def test_full_document_pages():
    markdown = Markdown(filename=f'{SAMPLES}/kitchen-sink.md')
    document = markdown.render()
    assert len(document.pages) >= 3
    pdf = markdown.write_pdf()
    assert pdf.startswith(b'%PDF')


@assert_no_logs
def test_long_document_pagination():
    document = Markdown(filename=f'{SAMPLES}/long-document.md').render()
    assert len(document.pages) >= 8


@assert_no_logs
def test_image_base_url():
    markdown = Markdown(
        string='# Chart\n\n![chart](chart.png)', base_url=f'{SAMPLES}/chart.png')
    document = markdown.render()
    assert len(document.pages) == 1
    # The image is drawn: look for an image stream in the PDF.
    pdf = markdown.write_pdf()
    assert b'/Subtype /Image' in pdf or b'/Subtype/Image' in pdf


def test_missing_image_still_renders(caplog):
    markdown = Markdown(string='![gone](missing.png)', base_url='.')
    document = markdown.render()
    assert len(document.pages) == 1
    assert 'missing.png' in caplog.text


def test_deterministic_output():
    source = open(f'{SAMPLES}/kitchen-sink.md', encoding='utf-8').read()
    first = Markdown(string=source, base_url=SAMPLES).write_pdf()
    second = Markdown(string=source, base_url=SAMPLES).write_pdf()
    assert first == second


def test_unicode_document():
    markdown = Markdown(filename=f'{SAMPLES}/unicode.md')
    pdf = markdown.write_pdf()
    assert pdf.startswith(b'%PDF')
    assert len(markdown.render().pages) >= 2


def test_markdown_extensions_detection():
    for extension in MARKDOWN_EXTENSIONS:
        assert extension.startswith('.')
    assert '.md' in MARKDOWN_EXTENSIONS


def test_html_option_still_works():
    # The HTML path is untouched.
    document = HTML(string='<p>fine</p>').render()
    assert len(document.pages) == 1


def test_build_html_lang():
    html = build_html('<p>x</p>', 'T', {'lang': 'de'})
    assert '<html lang="de">' in html
    assert '<html lang="en">' not in html
