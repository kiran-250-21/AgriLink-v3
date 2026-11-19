# -*- coding: utf-8 -*-
"""
build_capstone_report_docx.py
=============================
Generates the complete VIT-AP Capstone Project Report for AgriLink
matching the exact structure, chapters, sections, tables, and pagination
of the reference document provided by the user.
"""

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = r"d:\zz2\AgriLink\research_and_docs\docs"
FIGS_DIR = r"d:\zz2\AgriLink\research_and_docs\results\figures"
OUT_DOCX = os.path.join(DOCS_DIR, "AGRILINK_CAPSTONE_PROJECT_REPORT.docx")

def create_report():
    doc = Document()
    
    # Page setup - Standard 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    print("Initialized document setup.")
    return doc

if __name__ == '__main__':
    doc = create_report()
    doc.save(OUT_DOCX)
    print("Saved basic docx.")
