"""
Master Documentation Builder for AgriLink LTIMindtree Interview
Combines all documentation sections, converts Markdown to styled HTML,
and compiles into high-grade PDF via Microsoft Edge.
"""

import os
import sys
import re
import subprocess
import markdown

# Ensure sections directory is importable
SECTIONS_DIR = os.path.join(os.path.dirname(__file__), "sections")
sys.path.insert(0, SECTIONS_DIR)

import sec01_meta_overview
import sec02_tech_stack
import sec03_architecture
import sec04_code_features
import sec05_recommendation_logic
import sec06_database_api
import sec07_challenges_testing
import sec08_security_scalability
import sec09_interview_prep
import sec10_limitations_revision

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DOC_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOC_DIR, "AgriLink_Complete_Project_Documentation_LTIMindtree_Interview.md")
HTML_PATH = os.path.join(DOC_DIR, "AgriLink_Complete_Project_Documentation_LTIMindtree_Interview.html")
PDF_PATH = os.path.join(DOC_DIR, "AgriLink_Complete_Project_Documentation_LTIMindtree_Interview.pdf")

print("=" * 70)
print("[AgriLink Documentation Builder] Compiling All Sections...")
print("=" * 70)

# Assemble Markdown content
sections = [
    sec01_meta_overview.get_content(),
    sec02_tech_stack.get_content(),
    sec03_architecture.get_content(),
    sec04_code_features.get_content(),
    sec05_recommendation_logic.get_content(),
    sec06_database_api.get_content(),
    sec07_challenges_testing.get_content(),
    sec08_security_scalability.get_content(),
    sec09_interview_prep.get_content(),
    sec10_limitations_revision.get_content(),
]

full_md_content = "\n\n<div class=\"page-break\"></div>\n\n".join(sections)

print(f"Writing complete Markdown document to: {MD_PATH}")
with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(full_md_content)

print(f"[OK] Markdown document successfully saved! (Size: {len(full_md_content):,} characters)")

# Convert Markdown to HTML with math protection
print("Converting Markdown to styled HTML...")

math_tokens = []

def protect_disp(m):
    idx = len(math_tokens)
    math_tokens.append(m.group(0))
    return f"XRXEQNDISP{idx}XRX"

def protect_inl(m):
    idx = len(math_tokens)
    math_tokens.append(m.group(0))
    return f"XRXEQNINL{idx}XRX"

md_protected = re.sub(r'\$\$(.*?)\$\$', protect_disp, full_md_content, flags=re.DOTALL)
md_protected = re.sub(r'(?<!\$)\$(?!\$)([^\n]+?)(?<!\$)\$(?!\$)', protect_inl, md_protected)

# Convert Markdown to HTML
html_body = markdown.markdown(md_protected, extensions=['tables', 'fenced_code'])

# Restore math
for idx, raw_math in enumerate(math_tokens):
    disp_placeholder = f"XRXEQNDISP{idx}XRX"
    inl_placeholder = f"XRXEQNINL{idx}XRX"
    # Format nicely for HTML display
    clean_math = raw_math.strip()
    if clean_math.startswith("$$") and clean_math.endswith("$$"):
        eq_content = clean_math[2:-2].strip()
        html_eq = f'<div class="math-display"><code>{eq_content}</code></div>'
        html_body = html_body.replace(disp_placeholder, html_eq)
    elif clean_math.startswith("$") and clean_math.endswith("$"):
        eq_content = clean_math[1:-1].strip()
        html_eq = f'<span class="math-inline"><code>{eq_content}</code></span>'
        html_body = html_body.replace(inl_placeholder, html_eq)
    else:
        html_body = html_body.replace(disp_placeholder, raw_math)
        html_body = html_body.replace(inl_placeholder, raw_math)

# Embed High-Grade Enterprise HTML Template
html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AgriLink: Complete Project Documentation & LTIMindtree Interview Defense Guide</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

@page {{
    size: A4;
    margin: 18mm 15mm 20mm 15mm;
    @bottom-right {{
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8.5pt;
        font-weight: 500;
        color: #64748b;
    }}
    @bottom-left {{
        content: "AgriLink Platform | LTIMindtree Technical Interview Documentation";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
    }}
}}

*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 9.8pt;
    line-height: 1.55;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}}

.page-break {{
    page-break-before: always;
    break-before: page;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Inter', sans-serif;
    color: #0f172a;
    font-weight: 700;
    line-height: 1.25;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
    break-after: avoid;
}}

h1 {{
    font-size: 19pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2.5px solid #10b981;
    padding-bottom: 6px;
    margin-top: 0;
}}

h2 {{
    font-size: 14pt;
    font-weight: 700;
    color: #1e293b;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 4px;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #047857;
    margin-top: 1.1em;
}}

h4 {{
    font-size: 10.2pt;
    font-weight: 600;
    color: #334155;
}}

p {{
    margin-top: 0;
    margin-bottom: 0.8em;
    text-align: justify;
}}

strong {{
    font-weight: 600;
    color: #0f172a;
}}

em {{
    font-style: italic;
}}

hr {{
    border: none;
    height: 1px;
    background-color: #e2e8f0;
    margin: 20px 0;
}}

/* Clean Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 8.4pt;
    line-height: 1.4;
    page-break-inside: avoid;
    break-inside: avoid;
}}

th, td {{
    padding: 6px 9px;
    text-align: left;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}}

th {{
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 600;
    letter-spacing: 0.02em;
}}

tr:nth-child(even) {{
    background-color: #f8fafc;
}}

tr:hover {{
    background-color: #f1f5f9;
}}

/* Code Blocks & Inlines */
code {{
    font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
    font-size: 8.6pt;
    background-color: #f1f5f9;
    color: #0f172a;
    padding: 1.5px 4.5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
}}

pre {{
    font-family: 'JetBrains Mono', 'Consolas', 'Monaco', monospace;
    font-size: 8.1pt;
    line-height: 1.45;
    background-color: #0f172a;
    color: #f8fafc;
    padding: 12px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 12px 0;
    border: 1px solid #1e293b;
    page-break-inside: avoid;
    break-inside: avoid;
}}

pre code {{
    background-color: transparent;
    color: #f8fafc;
    padding: 0;
    border: none;
    font-size: inherit;
}}

/* Callouts & Quotes */
blockquote {{
    border-left: 4px solid #10b981;
    background-color: #f0fdf4;
    margin: 12px 0;
    padding: 8px 14px;
    border-radius: 0 6px 6px 0;
    color: #166534;
    font-size: 9.2pt;
}}

ul, ol {{
    margin-top: 0;
    margin-bottom: 0.8em;
    padding-left: 20px;
}}

li {{
    margin-bottom: 3.5px;
}}

/* Math styling */
.math-display {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #0284c7;
    padding: 8px 12px;
    margin: 10px 0;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.2pt;
    color: #0369a1;
}}

.math-display code {{
    background: transparent;
    border: none;
    color: inherit;
    font-size: inherit;
}}

.math-inline {{
    background-color: #f0f9ff;
    color: #0284c7;
    padding: 1px 4px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.8pt;
}}

.math-inline code {{
    background: transparent;
    border: none;
    color: inherit;
    font-size: inherit;
}}

/* Print Optimization */
@media print {{
    body {{
        padding: 0;
        max-width: 100%;
    }}
    h1, h2, h3, h4 {{
        page-break-after: avoid;
        break-after: avoid;
    }}
    table, pre, blockquote {{
        page-break-inside: avoid;
        break-inside: avoid;
    }}
    .page-break {{
        page-break-before: always;
        break-before: page;
    }}
}}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

print(f"Writing complete HTML document to: {HTML_PATH}")
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_document)

print(f"[OK] HTML document successfully saved! (Size: {len(html_document):,} characters)")

# Compile PDF using Microsoft Edge Headless
edge_bin = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
print("Invoking Microsoft Edge headless print to compile PDF...")

cmd = [
    edge_bin,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Microsoft Edge process return code:", res.returncode)

if os.path.exists(PDF_PATH):
    size_mb = os.path.getsize(PDF_PATH) / (1024 * 1024)
    print("=" * 70)
    print("[SUCCESS] Generated Master PDF Documentation!")
    print(f"Location: {PDF_PATH}")
    print(f"File Size: {size_mb:.2f} MB")
    print("=" * 70)
else:
    print("[ERROR] PDF was not generated. Stderr:", res.stderr)
