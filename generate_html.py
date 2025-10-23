import os
import glob
import markdown2
from pathlib import Path

EXTRAS = ["fenced-code-blocks", "tables", "toc", "strike", "task_list"]

# Directories
md_dirs = [
    r"c:\Analysis_10_21\reports\reports\reports\Team_Share_Package\Markdown_Reports",
    r"c:\Analysis_10_21\reports\reports\reports\Team_Share_Package\Summary_Reports"
]
site_dir = r"c:\Analysis_10_21\reports\reports\reports\Team_Share_Package\site"

# HTML template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{page_title}</title>
    <link rel="stylesheet" href="style.css" />
    <meta name="description" content="Automated evaluation report" />
</head>
<body>
    <header>
        <h1>{heading}</h1>
        <p class="subtitle">{subtitle}</p>
    </header>
    <main>
        {pair_links}
        {toc}
        {content}
    </main>
    <footer>Generated on {generated_date}</footer>
</body>
</html>'''

def rewrite_md_links_to_html(html_text):
    """Rewrite internal links so they target generated HTML in the same folder.

    Rules:
      - Any href ending in .md becomes .html
      - Strip leading absolute Windows file paths (file:///C:/.../Markdown_Reports/ or Summary_Reports/)
      - Strip directory prefixes 'Markdown_Reports/' or 'Summary_Reports/' for local report links
      - Preserve query/hash fragments
    """
    import re

    def replace_ext(url: str) -> str:
        # split off fragment/query
        main, frag = re.match(r'([^#?]+)([?#].*)?$', url).groups()
        if main.endswith('.md'):
            main = main[:-3] + '.html'
        # Remove path segments pointing to source directories or absolute paths
        main = re.sub(r'.*?(Markdown_Reports|Summary_Reports)/', '', main)
        main = re.sub(r'^file:/+([A-Za-z]:/).*?(Markdown_Reports|Summary_Reports)/', '', main)
        return (main + (frag or ''))

    def repl(match):
        url = match.group(1)
        # Only adjust if it looks like a local report link (contains evaluation_report_ or endswith .md/.html)
        if ('evaluation_report_' in url or url.endswith('.md') or url.endswith('.html') or 'all_runs_summary' in url or 'comprehensive_summary' in url):
            url = replace_ext(url)
        return f'href="{url}"'

    # First pass: convert md->html
    updated = re.sub(r'href="([^"]+)"', repl, html_text)
    return updated

def derive_titles(md_path, md_content):
    filename = Path(md_path).stem
    # Break components: evaluation_report_ado_<build>_<timestamp>_(report|bugs_analysis)
    parts = filename.split('_')
    # Attempt build id after 'ado'
    build = None
    if 'ado' in parts:
        idx = parts.index('ado')
        if idx + 1 < len(parts):
            build = parts[idx + 1]
    # Find first markdown heading
    import re
    m = re.search(r'^#\s+(.+)', md_content, re.MULTILINE)
    first_heading = m.group(1).strip() if m else 'Evaluation Report'
    is_analysis = filename.endswith('bugs_analysis')
    kind = 'Bugs & Analysis' if is_analysis else 'Evaluation Summary'
    # Human-readable date from any 14-digit timestamp pattern
    date_part = None
    for p in parts:
        if len(p) == 14 and p.isdigit():
            date_part = p
            break
    run_date = ''
    if date_part:
        run_date = f"{date_part[0:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[8:10]}:{date_part[10:12]}:{date_part[12:14]}"
    page_title = f"{kind} | Build {build}" if build else kind
    heading = f"{kind} - Build {build}" if build else kind
    if run_date:
        heading += f" (Run {run_date})"
    subtitle = first_heading
    return page_title, heading, subtitle

def convert_md_to_html(md_path, html_path, all_pairs, all_html_files):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # Preprocess bugs analysis files to ensure label newlines
    if md_path.endswith('_bugs_analysis.md'):
        import re
        # Format per-test-case blocks more cleanly.
        # Detect blocks starting with **N. test_case_XXX** pattern or **N. test_case_XXX** variants.
        def format_case(match):
            header = match.group(0)
            return f'\n\n{header}\n'
        md_content = re.sub(r'\*\*\d+\. test_case_\d+\*\*', format_case, md_content)

        # Clean stray emphasis markers '* ' patterns causing <em>* artifacts
        md_content = re.sub(r'\*\*\s*', '**', md_content)
        md_content = re.sub(r'\n- \*\*', '\n- **', md_content)

        # Ensure labels Category/Description/Analysis/Tools Called each on new bullet line with bold label
        label_map = {
            'Category': 'Category',
            'Description': 'Description',
            'Analysis': 'Analysis',
            'Tools Called': 'Tools Called'
        }
        for label, disp in label_map.items():
            # Normalize existing formatting lines beginning with '- **<label>' or '- <label>'
            md_content = re.sub(rf'-\s*\**{label}\**:', f'- **{disp}:**', md_content)
        # Ensure newline after bold label so value appears below
        md_content = re.sub(r'(\- \*\*[^\n:]+:\*\*)\s*', r'\1\n', md_content)
        # If a line has multiple labels merged, split them
        md_content = re.sub(r'(\*\*Tools Called:\*\*)([^\n])', r'\1\n\2', md_content)
        # Insert blank line BEFORE bold test case headers and labels if missing
        md_content = re.sub(r'(?<!\n\n)(\n\*\*\d+\. test_case_\d+\*\*)', r'\n\1', md_content)
        md_content = re.sub(r'(?<!\n\n)(\n- \*\*[A-Za-z ]+:\*\*)', r'\n\1', md_content)
        # Collapse >2 consecutive blank lines to exactly two
        md_content = re.sub(r'\n{3,}', '\n\n', md_content)
        # Remove malformed emphasis resulting in <em>*
        md_content = re.sub(r'<em>\*', '<em>', md_content)
        # Prevent underscores in identifiers from italicizing by wrapping test_case_ tokens in backticks
        md_content = re.sub(r'(test_case_\d+)', r'`\1`', md_content)
        # Collapse excessive spaces before line breaks
        md_content = re.sub(r'[ \t]+\n', '\n', md_content)
    html = markdown2.markdown(md_content, extras=EXTRAS)
    toc_html = html.toc_html if hasattr(html, 'toc_html') and html.toc_html else ''
    page_title, heading, subtitle = derive_titles(md_path, md_content)
    title = Path(md_path).stem  # legacy reference (not used for display now)
    # Pair links logic
    base = title
    pair_links = ''
    if base.endswith('_report'):
        pair = base.replace('_report', '_bugs_analysis') + '.html'
        if pair in all_pairs:
            pair_links = f'<div class="pair-links"><span class="badge">Related</span><a href="{pair}">Bugs Analysis</a></div>'
    elif base.endswith('_bugs_analysis'):
        pair = base.replace('_bugs_analysis', '_report') + '.html'
        if pair in all_pairs:
            pair_links = f'<div class="pair-links"><span class="badge">Related</span><a href="{pair}">Main Report</a></div>'

    # navigation removed
    html_converted = rewrite_md_links_to_html(str(html))
    import datetime
    gen_dt = datetime.datetime.fromtimestamp(os.path.getmtime(md_path)).strftime('%Y-%m-%d %H:%M:%S')
    rendered = HTML_TEMPLATE.format(
        page_title=page_title,
        heading=heading,
        subtitle=subtitle,
        toc=f'<div class="toc"><h2>Contents</h2>{toc_html}</div>' if toc_html else '',
        content=html_converted,
        pair_links=pair_links,
        generated_date=gen_dt
    )
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

def main():
    all_html_files = []
    md_files = []
    for md_dir in md_dirs:
        md_files.extend(glob.glob(os.path.join(md_dir, '*.md')))
    # Precompute list for navigation
    for f in md_files:
        base = Path(f).stem
        all_html_files.append((base + '.html', base))
    all_pairs = {name for name, _ in all_html_files}
    # Generate individual pages
    for md_file in md_files:
        base = Path(md_file).stem
        html_file = os.path.join(site_dir, base + '.html')
        convert_md_to_html(md_file, html_file, all_pairs, all_html_files)
    # Generate index.html with improved layout
    index_path = os.path.join(site_dir, 'index.html')
    links = '\n'.join([f'<li><a href="{fname}">{title}</a></li>' for fname, title in all_html_files])
    content = f'<div class="toc"><h2>All Reports</h2><ul class="report-index">{links}</ul></div>'
    index_rendered = HTML_TEMPLATE.format(page_title="Report Index", heading="Report Index", subtitle="All generated reports", toc='', content=content, pair_links='', generated_date='')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_rendered)

if __name__ == "__main__":
    main()
