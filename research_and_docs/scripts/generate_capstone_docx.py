# -*- coding: utf-8 -*-
"""
generate_capstone_docx.py
=========================
Generates the complete VIT-AP Capstone Project Report Word document (.docx)
for AgriLink directly from the markdown report.
"""

import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"
MD_PATH = os.path.join(DOCS_DIR, "AGRILINK_CAPSTONE_PROJECT_REPORT.md")
OUT_DOCX = os.path.join(DOCS_DIR, "AGRILINK_CAPSTONE_PROJECT_REPORT.docx")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_background(cell, color_hex="F0F4F8"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="CCCCCC", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_docx():
    doc = Document()
    
    # 1-inch standard margins
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)

    # Base normal style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(17, 17, 17)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)

    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Split by page breaks
    pages = md_text.split('<div style="page-break-after: always;"></div>')
    print(f"Total markdown sections: {len(pages)}")

    for p_idx, page_content in enumerate(pages):
        lines = page_content.strip().split('\n')
        in_table = False
        table_rows = []
        in_code = False
        code_lines = []

        for line in lines:
            stripped = line.strip()

            # Code blocks
            if stripped.startswith('```'):
                if in_code:
                    in_code = False
                    p_code = doc.add_paragraph()
                    p_code.paragraph_format.left_indent = Inches(0.2)
                    p_code.paragraph_format.space_before = Pt(4)
                    p_code.paragraph_format.space_after = Pt(4)
                    r = p_code.add_run('\n'.join(code_lines))
                    r.font.name = 'Courier New'
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(30, 41, 59)
                    code_lines = []
                else:
                    in_code = True
                    code_lines = []
                continue

            if in_code:
                code_lines.append(line)
                continue

            # Tables in markdown
            if stripped.startswith('|') and stripped.endswith('|'):
                if '---' in stripped:
                    continue  # Separator line
                cells = [c.strip() for c in stripped.strip('|').split('|')]
                table_rows.append(cells)
                in_table = True
                continue
            else:
                if in_table and table_rows:
                    # Flush table
                    num_cols = max(len(r) for r in table_rows)
                    tbl = doc.add_table(rows=len(table_rows), cols=num_cols)
                    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                    set_table_borders(tbl, color="B0C4DE", sz="4")
                    
                    for r_i, row_data in enumerate(table_rows):
                        is_header = (r_i == 0)
                        for c_i, cell_text in enumerate(row_data):
                            if c_i < num_cols:
                                cell = tbl.cell(r_i, c_i)
                                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                                if is_header:
                                    set_cell_background(cell, "002855")
                                else:
                                    if r_i % 2 == 1:
                                        set_cell_background(cell, "F8FAFC")
                                    else:
                                        set_cell_background(cell, "FFFFFF")
                                p = cell.paragraphs[0]
                                p.paragraph_format.space_after = Pt(0)
                                p.paragraph_format.space_before = Pt(0)
                                p.paragraph_format.line_spacing = 1.15
                                clean_t = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_text)
                                r = p.add_run(clean_t)
                                r.font.name = 'Times New Roman'
                                if is_header:
                                    r.font.bold = True
                                    r.font.size = Pt(9.5)
                                    r.font.color.rgb = RGBColor(255, 255, 255)
                                else:
                                    r.font.size = Pt(9)
                                    if '**' in cell_text:
                                        r.font.bold = True
                    table_rows = []
                    in_table = False

            if not stripped or stripped == '---' or stripped.startswith('<'):
                continue

            # Headings
            if stripped.startswith('# '):
                h_text = stripped[2:].strip()
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(14)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.keep_with_next = True
                if p_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r = p.add_run(h_text)
                    r.font.name = 'Arial'
                    r.font.size = Pt(16)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 40, 85)
                else:
                    r = p.add_run(h_text)
                    r.font.name = 'Arial'
                    r.font.size = Pt(14)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 40, 85)

            elif stripped.startswith('## '):
                h_text = stripped[3:].strip()
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.keep_with_next = True
                if p_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(h_text)
                r.font.name = 'Arial'
                r.font.size = Pt(12)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 40, 85)

            elif stripped.startswith('### '):
                h_text = stripped[4:].strip()
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.keep_with_next = True
                if p_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(h_text)
                r.font.name = 'Arial'
                r.font.size = Pt(11)
                r.font.bold = True
                r.font.color.rgb = RGBColor(30, 41, 59)

            elif stripped.startswith('#### '):
                h_text = stripped[5:].strip()
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.keep_with_next = True
                r = p.add_run(h_text)
                r.font.name = 'Arial'
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 40, 85)

            # Bullet points
            elif stripped.startswith('- ') or stripped.startswith('* '):
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.space_before = Pt(1)
                b_text = stripped[2:].strip()
                # Parse bold spans
                parts = re.split(r'(\*\*.*?\*\*)', b_text)
                r_bullet = p.add_run("• ")
                r_bullet.font.bold = True
                r_bullet.font.color.rgb = RGBColor(0, 40, 85)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        r = p.add_run(part[2:-2])
                        r.font.bold = True
                    else:
                        r = p.add_run(part)

            # Normal paragraphs
            else:
                p = doc.add_paragraph()
                if p_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.space_after = Pt(4)
                parts = re.split(r'(\*\*.*?\*\*)', stripped)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        r = p.add_run(part[2:-2])
                        r.font.bold = True
                    else:
                        r = p.add_run(part)

        # Flush any remaining table on page
        if in_table and table_rows:
            num_cols = max(len(r) for r in table_rows)
            tbl = doc.add_table(rows=len(table_rows), cols=num_cols)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(tbl, color="B0C4DE", sz="4")
            for r_i, row_data in enumerate(table_rows):
                is_header = (r_i == 0)
                for c_i, cell_text in enumerate(row_data):
                    if c_i < num_cols:
                        cell = tbl.cell(r_i, c_i)
                        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                        if is_header:
                            set_cell_background(cell, "002855")
                        else:
                            if r_i % 2 == 1:
                                set_cell_background(cell, "F8FAFC")
                            else:
                                set_cell_background(cell, "FFFFFF")
                        p = cell.paragraphs[0]
                        clean_t = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_text)
                        r = p.add_run(clean_t)
                        r.font.name = 'Times New Roman'
                        if is_header:
                            r.font.bold = True
                            r.font.size = Pt(9.5)
                            r.font.color.rgb = RGBColor(255, 255, 255)
                        else:
                            r.font.size = Pt(9)
            table_rows = []
            in_table = False

        # Add page break between pages except for the very last page
        if p_idx < len(pages) - 1:
            doc.add_page_break()

    doc.save(OUT_DOCX)
    print(f"SUCCESS: Generated complete Capstone Report DOCX: {OUT_DOCX}")

if __name__ == '__main__':
    build_docx()
