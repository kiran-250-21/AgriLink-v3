import os
import subprocess
import shutil
import pypdf

DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"
DELIV_DIR = r"d:\zz2\AgriLink\research_and_docs\deliverables"

src_html_path = os.path.join(DELIV_DIR, "AGRILINK_RESEARCH_PAPER_REVISED.html")
with open(src_html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove running header "Mounika et al.: "
html = html.replace(
    'content: "Mounika et al.: AgriLink: An Empirical, Logistics-Aware Decision Framework for Wholesale Market Selection";',
    'content: "AgriLink: An Empirical, Logistics-Aware Decision Framework for Wholesale Market Selection";'
)

# 2. Remove banner text
old_banner_td = """                <td class="banner-left">
                    Date of current draft October 31, 2026. Pre-publication manuscript.<br>
                    Digital Object Identifier will be assigned upon publication.
                </td>"""
new_banner_td = """                <td class="banner-left">
                </td>"""
if old_banner_td in html:
    html = html.replace(old_banner_td, new_banner_td)
    print("Replaced banner TD")
else:
    # Try more flexible replacement
    import re
    html = re.sub(r'<td class="banner-left">.*?</td>', '<td class="banner-left"></td>', html, flags=re.DOTALL)
    print("Replaced banner TD via regex")

# 3. Remove Author Line, Affil Block, and Footnote Line
author_block_pattern = r'<div class="author-line">.*?</div>\s*<div class="affil-block">.*?</div>\s*<div class="footnote-line">.*?</div>'
import re
match = re.search(author_block_pattern, html, flags=re.DOTALL)
if match:
    html = html[:match.start()] + html[match.end():]
    print("Removed author block, affil block, and footnote line successfully.")
else:
    print("WARNING: author block pattern not matched!")

# 4. Remove Biographies table at the end
bio_pattern = r'<div class="full-width">\s*<table class="bio-table">.*?</table>\s*</div>'
match_bio = re.search(bio_pattern, html, flags=re.DOTALL)
if match_bio:
    html = html[:match_bio.start()] + html[match_bio.end():]
    print("Removed author biographies successfully.")
else:
    print("WARNING: bio table pattern not matched!")

# Save rsp.html in docs/ and deliverables/
rsp_html_docs = os.path.join(DOCS_DIR, "rsp.html")
with open(rsp_html_docs, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Written: {rsp_html_docs}")

rsp_html_deliv = os.path.join(DELIV_DIR, "rsp.html")
shutil.copyfile(rsp_html_docs, rsp_html_deliv)

# Compile rsp.pdf using Chrome Headless
chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
rsp_pdf_docs = os.path.join(DOCS_DIR, "rsp.pdf")
rsp_pdf_deliv = os.path.join(DELIV_DIR, "rsp.pdf")

if os.path.exists(chrome_bin):
    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={rsp_pdf_docs}",
        rsp_html_docs
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Chrome exit code:", res.returncode)
    if os.path.exists(rsp_pdf_docs):
        shutil.copyfile(rsp_pdf_docs, rsp_pdf_deliv)
        reader = pypdf.PdfReader(rsp_pdf_docs)
        print(f"SUCCESS: Generated {rsp_pdf_docs} ({len(reader.pages)} pages, {os.path.getsize(rsp_pdf_docs)/(1024*1024):.2f} MB)")
    else:
        print("ERROR: Failed to generate rsp.pdf")

