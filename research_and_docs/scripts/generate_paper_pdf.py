import os
import re
import base64
import subprocess
import markdown

DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"
FIGURES_DIR = r"d:\zz2\AgriLink\research_and_docs\results\figures"
MD_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER.md")
HTML_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER.html")
PDF_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER.pdf")

print("Reading Markdown...")
with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

# Replace image markdown with base64 data URIs
def img_replacer(match):
    alt = match.group(1)
    rel_path = match.group(2)
    filename = os.path.basename(rel_path)
    full_path = os.path.join(FIGURES_DIR, filename)
    if os.path.exists(full_path):
        with open(full_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode("utf-8")
        return f'<div class="figure-container"><img src="data:image/png;base64,{b64_data}" alt="{alt}" /><div class="figure-caption">{alt}</div></div>'
    return match.group(0)

# Replace Markdown image syntax: ![alt](path)
md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', img_replacer, md_content)

# Math protection to prevent markdown from turning underscores/asterisks into <em> tags
math_tokens = []

def protect_disp(m):
    idx = len(math_tokens)
    math_tokens.append(m.group(0))
    return f"XRXEQNDISP{idx}XRX"

def protect_inl(m):
    idx = len(math_tokens)
    math_tokens.append(m.group(0))
    return f"XRXEQNINL{idx}XRX"

# Protect display math $$ ... $$
md_protected = re.sub(r'\$\$(.*?)\$\$', protect_disp, md_content, flags=re.DOTALL)
# Protect inline math $ ... $
md_protected = re.sub(r'(?<!\$)\$(?!\$)([^\n]+?)(?<!\$)\$(?!\$)', protect_inl, md_protected)

# Convert Markdown to HTML
html_body = markdown.markdown(md_protected, extensions=['tables', 'fenced_code'])

# Restore pristine math
for idx, raw_math in enumerate(math_tokens):
    disp_placeholder = f"XRXEQNDISP{idx}XRX"
    inl_placeholder = f"XRXEQNINL{idx}XRX"
    html_body = html_body.replace(disp_placeholder, raw_math)
    html_body = html_body.replace(inl_placeholder, raw_math)

# HTML document with MathJax 3 configuration
html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AgriLink: A Logistics-Aware Framework for Agricultural Market Selection</title>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    tags: 'none'
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }},
  svg: {{
    fontCache: 'global'
  }}
}};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<style>
@page {{
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {{
        content: counter(page);
        font-family: 'Times New Roman', Times, serif;
        font-size: 10pt;
        color: #555;
    }}
}}

body {{
    font-family: 'Times New Roman', 'Cambria', 'Georgia', serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #1a1a1a;
    background-color: #ffffff;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}}

/* Header styling */
h1 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 20pt;
    font-weight: 700;
    text-align: center;
    color: #0d233a;
    line-height: 1.3;
    margin-top: 15px;
    margin-bottom: 12px;
}}

.article-meta {{
    text-align: center;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 10.5pt;
    color: #444;
    margin-bottom: 25px;
    line-height: 1.4;
}}

.article-meta strong {{
    color: #111;
}}

/* Section Headings */
h2 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 13.5pt;
    font-weight: 700;
    color: #0d233a;
    border-bottom: 1.5px solid #0d233a;
    padding-bottom: 4px;
    margin-top: 28px;
    margin-bottom: 12px;
    page-break-after: avoid;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

h3 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 11.5pt;
    font-weight: 700;
    color: #1a446c;
    margin-top: 20px;
    margin-bottom: 8px;
    page-break-after: avoid;
}}

p {{
    text-align: justify;
    margin-top: 0;
    margin-bottom: 10px;
    text-indent: 1.5em;
}}

p.no-indent, .figure-caption, blockquote p, table p, td p, th p {{
    text-indent: 0;
}}

/* Abstract Box */
blockquote {{
    background-color: #f8fafc;
    border-left: 4px solid #1a446c;
    border-right: 1px solid #e2e8f0;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    margin: 15px 0 25px 0;
    padding: 12px 18px;
    border-radius: 4px;
    font-size: 10.5pt;
    line-height: 1.5;
}}

/* Tables (Classic Booktabs style) */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 20px 0;
    font-size: 9.5pt;
    line-height: 1.4;
    page-break-inside: avoid;
}}

th, td {{
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
}}

thead tr:first-child th {{
    border-top: 2px solid #111;
    border-bottom: 1.5px solid #111;
    font-weight: 700;
    color: #0d233a;
    background-color: #f1f5f9;
}}

tbody tr:last-child td {{
    border-bottom: 2px solid #111;
}}

tbody tr:nth-child(even) {{
    background-color: #fbfcfd;
}}

tbody tr td {{
    border-bottom: 0.5px solid #e2e8f0;
}}

/* Code & Preformatted */
pre {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 10px 14px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    line-height: 1.35;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 14px 0;
}}

code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 9.5pt;
    background-color: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
}}

/* Figures */
.figure-container {{
    text-align: center;
    margin: 20px 0;
    page-break-inside: avoid;
}}

.figure-container img {{
    max-width: 95%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

.figure-caption {{
    font-size: 9.5pt;
    font-style: italic;
    color: #334155;
    margin-top: 8px;
    line-height: 1.4;
    text-align: center;
}}

/* Lists */
ul, ol {{
    margin-top: 4px;
    margin-bottom: 12px;
    padding-left: 28px;
}}

li {{
    margin-bottom: 5px;
    text-align: justify;
}}

/* Horizontal rules */
hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 22px 0;
}}

/* Print overrides */
@media print {{
    body {{
        padding: 0;
        max-width: 100%;
    }}
    .figure-container img {{
        max-width: 90% !important;
    }}
    table {{
        font-size: 9pt;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

print(f"Writing HTML to {HTML_PATH}...")
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_doc)

print("HTML generated successfully!")

# Run Microsoft Edge to compile PDF
edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
print("Invoking Microsoft Edge headless print to PDF...")
cmd = [
    edge_bin,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--virtual-time-budget=8000",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if os.path.exists(PDF_PATH):
    size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
    print(f"SUCCESS: Generated PDF at {PDF_PATH} ({size_mb:.2f} MB)")
else:
    print("PDF generation failed or file not found.")
