import os
import re
import base64
import subprocess
import markdown

DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"
FIGURES_DIR = r"d:\zz2\AgriLink\research_and_docs\results\figures"
MD_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER_12PAGES.md")
HTML_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER_12PAGES.html")
PDF_PATH = os.path.join(DOCS_DIR, "AGRILINK_RESEARCH_PAPER_12PAGES.pdf")

def build_pdf():
    print(f"Reading Markdown from {MD_PATH}...")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Base64 image replacer
    def img_replacer(match):
        alt = match.group(1)
        rel_path = match.group(2)
        filename = os.path.basename(rel_path)
        full_path = os.path.join(FIGURES_DIR, filename)
        if os.path.exists(full_path):
            with open(full_path, "rb") as img_f:
                b64_data = base64.b64encode(img_f.read()).decode("utf-8")
            return f'<div class="figure-container"><img src="data:image/png;base64,{b64_data}" alt="{alt}" /><div class="figure-caption"><strong>{alt}</strong></div></div>'
        return match.group(0)

    md_content = re.sub(r'!\[(.*?)\]\((.*?)\)', img_replacer, md_content)

    # Math token protection
    math_tokens = []
    def protect_disp(m):
        idx = len(math_tokens)
        math_tokens.append(m.group(0))
        return f"XRXEQNDISP{idx}XRX"

    def protect_inl(m):
        idx = len(math_tokens)
        math_tokens.append(m.group(0))
        return f"XRXEQNINL{idx}XRX"

    md_protected = re.sub(r'\$\$(.*?)\$\$', protect_disp, md_content, flags=re.DOTALL)
    md_protected = re.sub(r'(?<!\$)\$(?!\$)([^\n]+?)(?<!\$)\$(?!\$)', protect_inl, md_protected)

    html_body = markdown.markdown(md_protected, extensions=['tables', 'fenced_code'])

    for idx, raw_math in enumerate(math_tokens):
        html_body = html_body.replace(f"XRXEQNDISP{idx}XRX", raw_math)
        html_body = html_body.replace(f"XRXEQNINL{idx}XRX", raw_math)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AgriLink: A Logistics-Aware Decision-Support Framework for Agricultural Market Selection</title>
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
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
        content: counter(page);
        font-family: 'Times New Roman', Times, serif;
        font-size: 9.5pt;
        color: #444;
    }}
}}

body {{
    font-family: 'Times New Roman', 'Cambria', serif;
    font-size: 10.2pt;
    line-height: 1.48;
    color: #111;
    background-color: #fff;
    max-width: 860px;
    margin: 0 auto;
    padding: 10px;
}}

/* Header styling */
h1 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 18pt;
    font-weight: 700;
    text-align: center;
    color: #0b2545;
    line-height: 1.25;
    margin-top: 10px;
    margin-bottom: 8px;
}}

.article-meta {{
    text-align: center;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 9.5pt;
    color: #333;
    margin-bottom: 18px;
    line-height: 1.35;
}}

.article-meta strong {{
    color: #0b2545;
}}

h2 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #0b2545;
    border-bottom: 1.2px solid #0b2545;
    padding-bottom: 3px;
    margin-top: 20px;
    margin-bottom: 8px;
    page-break-after: avoid;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}}

h3 {{
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 10.8pt;
    font-weight: 700;
    color: #134074;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}}

p {{
    text-align: justify;
    margin-top: 0;
    margin-bottom: 8px;
    text-indent: 1.2em;
}}

p.no-indent, .figure-caption, blockquote p, table p, td p, th p {{
    text-indent: 0;
}}

blockquote {{
    background-color: #f7f9fb;
    border-left: 3.5px solid #134074;
    border-right: 1px solid #e2e8f0;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    margin: 10px 0 16px 0;
    padding: 10px 14px;
    border-radius: 3px;
    font-size: 9.8pt;
    line-height: 1.44;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 14px 0;
    font-size: 9pt;
    line-height: 1.35;
    page-break-inside: avoid;
}}

th, td {{
    padding: 5px 7px;
    text-align: left;
    vertical-align: middle;
}}

thead tr:first-child th {{
    border-top: 1.5px solid #111;
    border-bottom: 1.2px solid #111;
    font-weight: 700;
    background-color: #f1f5f9;
}}

tbody tr {{
    border-bottom: 0.5px solid #e2e8f0;
}}

tbody tr:last-child {{
    border-bottom: 1.5px solid #111;
}}

.figure-container {{
    text-align: center;
    margin: 14px 0;
    page-break-inside: avoid;
}}

.figure-container img {{
    max-width: 82%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}

.figure-caption {{
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    font-size: 8.8pt;
    color: #334155;
    margin-top: 5px;
    line-height: 1.3;
}}

code {{
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.8pt;
    background-color: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
}}

ol, ul {{
    margin-top: 2px;
    margin-bottom: 8px;
    padding-left: 20px;
}}

li {{
    margin-bottom: 4px;
    text-align: justify;
    font-size: 10pt;
}}

hr {{
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 16px 0;
}}

@media print {{
    body {{
        padding: 0;
        max-width: 100%;
    }}
    .figure-container img {{
        max-width: 85% !important;
    }}
    table {{
        font-size: 8.8pt;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"HTML written to {HTML_PATH}")

    edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    print("Compiling PDF via Microsoft Edge...")
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
    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            pdf_bytes = f.read()
        pages = len(re.findall(rb'/Type\s*/Page(?=[^s]|$)', pdf_bytes))
        size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
        print(f"SUCCESS: Generated PDF at {PDF_PATH} ({size_mb:.2f} MB, {pages} pages)")
        return pages
    else:
        print("PDF compilation failed.")
        return 0

if __name__ == "__main__":
    build_pdf()
