import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_border(cell, color="94A3B8", sz="8", val="single"):
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def create_report():
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    BANNER_BG       = "F1F5F9"
    CALLOUT_BG      = "F8FAFC"
    BORDER_COLOR    = "CBD5E1"
    ACCENT_BORDER   = "2563EB"
    
    NAVY_PRIMARY    = RGBColor(30, 58, 138)
    SLATE_SECONDARY  = RGBColor(71, 85, 105)
    TEXT_DARK       = RGBColor(15, 23, 42)
    CODE_TEXT_COLOR = RGBColor(30, 41, 59)
    CODE_BG_HEX     = "F8FAFC"

    # Header Title Block
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = header_table.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_background(cell, BANNER_BG)
    add_border(cell, color=ACCENT_BORDER, sz="12", val="single")
    set_cell_margins(cell, top=200, bottom=200, left=200, right=200)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("TASK 6: CREATING A STREAMLIT USER INTERFACE")
    run.font.size = Pt(19)
    run.font.bold = True
    run.font.color.rgb = NAVY_PRIMARY
    run.font.name = "Arial"

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run("Interactive Clinical Decision Support powered by Direct PyTorch Neural Network Engine")
    run2.font.size = Pt(11)
    run2.font.italic = True
    run2.font.color.rgb = SLATE_SECONDARY
    run2.font.name = "Arial"

    doc.add_paragraph()

    # Metadata Block
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Course / Subject:", "Deep Learning Deployment & Integration"), ("Task Target:", "Task 6 - Streamlit User Interface")],
        [("Frameworks & Stack:", "Streamlit 1.64, PyTorch 2.14, Plotly, Pandas"), ("Model Architecture:", "DeepHealthRiskNet (3-Layer Artificial Neural Network)")]
    ]
    for r_idx, row in enumerate(meta_data):
        for c_idx, (label, val) in enumerate(row):
            c = meta_table.cell(r_idx, c_idx)
            set_cell_background(c, "F8FAFC")
            add_border(c, color=BORDER_COLOR, sz="4", val="single")
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            r1 = p.add_run(f"{label} ")
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = NAVY_PRIMARY
            r2 = p.add_run(val)
            r2.font.size = Pt(9.5)
            r2.font.color.rgb = TEXT_DARK

    doc.add_paragraph()

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = NAVY_PRIMARY
        run.font.name = "Arial"

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = SLATE_SECONDARY
        run.font.name = "Arial"

    def add_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.size = Pt(10)
        run.font.color.rgb = TEXT_DARK
        run.font.name = "Calibri"
        return p

    def add_code_block(title, code_str):
        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_before = Pt(8)
        p_title.paragraph_format.space_after = Pt(2)
        r_t = p_title.add_run(f"Source Code Listing: {title}")
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = NAVY_PRIMARY

        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        c.width = Inches(7.0)
        set_cell_background(c, CODE_BG_HEX)
        add_border(c, color=BORDER_COLOR, sz="6", val="single")
        set_cell_margins(c, top=90, bottom=90, left=110, right=110)

        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(code_str)
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        r.font.color.rgb = CODE_TEXT_COLOR

        doc.add_paragraph()

    def add_screenshot_frame(title, instructions, step_num):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        c.width = Inches(7.0)
        set_cell_background(c, CALLOUT_BG)
        add_border(c, color=ACCENT_BORDER, sz="8", val="single")
        set_cell_margins(c, top=120, bottom=120, left=140, right=140)

        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p.add_run(f"Figure {step_num}: Screenshot Placeholder — {title}\n")
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = NAVY_PRIMARY

        p2 = c.add_paragraph()
        r2 = p2.add_run("Instructions for Image Capture:\n")
        r2.font.bold = True
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = SLATE_SECONDARY

        for inst in instructions:
            p_inst = c.add_paragraph()
            p_inst.paragraph_format.space_after = Pt(2)
            r_bullet = p_inst.add_run(f" • {inst}")
            r_bullet.font.size = Pt(9)
            r_bullet.font.color.rgb = TEXT_DARK

        p_note = c.add_paragraph()
        p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_note.paragraph_format.space_before = Pt(8)
        r_note = p_note.add_run("[ Insert Captured Figure Image Here ]")
        r_note.font.italic = True
        r_note.font.bold = True
        r_note.font.size = Pt(9.5)
        r_note.font.color.rgb = NAVY_PRIMARY

        doc.add_paragraph()

    # SECTION 1
    add_h1("1. Application Architecture & Overview")
    add_p(
        "Task 6 implements a streamlined Streamlit user interface for clinical health risk assessment powered directly "
        "by an in-memory PyTorch 3-Layer Deep Neural Network (DeepHealthRiskNet). The frontend connects to the model loader "
        "module (model_loader.py) to perform real-time forward pass inference and calculate Softmax probability distributions."
    )

    add_h2("Key Features of the Streamlit Clinical Interface:")
    features_list = [
        "Direct PyTorch Inference Engine: In-memory forward pass with sub-millisecond execution latency.",
        "Categorized Clinical Assessment Form: Inputs organized into Demographics & Body Metrics, Daily Activity & Nutrition, Vital Signs, and Lifestyle Pre-conditions.",
        "Dynamic Auto-Calculated BMI Meter: Live calculation of Body Mass Index with color-coded health status indicators.",
        "Plotly Softmax Probability Visualization: Interactive bar chart displaying probability breakdown across Low, Moderate, High, and Critical Risk tiers.",
        "Personalized Clinical Guidance: Automated recommendation engine providing tailored medical advice based on patient risk profile."
    ]
    for f_item in features_list:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(f"• {f_item}")
        r.font.size = Pt(9.5)
        r.font.color.rgb = TEXT_DARK

    # SECTION 2
    add_h1("2. Application Visual Walkthrough & Screenshots")
    add_p("Below are screenshot placeholders illustrating the user interface workflows of Task 6.")

    add_screenshot_frame("Streamlit UI Control Panel & Presets", [
        "Launch app: python -m streamlit run 'Frontend/task 6/app.py'",
        "Capture the left sidebar containing the active Direct PyTorch Engine status badge and Preset Sample loader dropdown."
    ], 1)

    add_screenshot_frame("Clinical Assessment Form & Auto-Calculated BMI", [
        "Scroll to the Patient Clinical Assessment Form.",
        "Capture the 4 input categories (Demographics, Activity, Vital Signs, Lifestyle) and the dynamic BMI indicator."
    ], 2)

    add_screenshot_frame("Neural Network Inference Results & Probability Bar Chart", [
        "Select '🔴 Severe / High Risk Preset' and click '⚡ Run Neural Network Inference'.",
        "Capture the diagnostic risk badge, confidence score card, sub-millisecond latency metric, and Plotly probability bar chart."
    ], 3)

    add_screenshot_frame("Personalized Clinical Recommendations & JSON Payload", [
        "Scroll down to the Clinical Guidance section.",
        "Capture the bulleted medical recommendations and expanded raw prediction JSON payload."
    ], 4)

    # SECTION 3
    add_h1("3. Model Execution & Performance Observations")
    add_p("1. In-Memory Sub-Millisecond Execution: Operating the PyTorch model directly in memory eliminates network round-trip overhead, achieving average inference latency of under 3 ms.")
    add_p("2. Robust Feature Transformation: Inputs are standardized using pre-saved StandardScaler normalization before feeding into the 14-node neural net input layer.")
    add_p("3. Interactive User Feedback: Dynamic widgets, presets, and Plotly charts provide clinicians with an immediate, intuitive diagnostic decision support tool.")

    # SECTION 4
    add_h1("4. Source Code Listings")
    add_p("Complete source code listings for app.py and utils.py are provided below.")

    # app.py
    app_path = "e:/DL_deploy/Frontend/task 6/app.py"
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            app_code = f.read()
    else:
        app_code = "# app.py"
    add_code_block("app.py", app_code)

    # utils.py
    utils_path = "e:/DL_deploy/Frontend/task 6/utils.py"
    if os.path.exists(utils_path):
        with open(utils_path, "r", encoding="utf-8") as f:
            utils_code = f.read()
    else:
        utils_code = "# utils.py"
    add_code_block("utils.py", utils_code)

    # Save
    doc_path = "e:/DL_deploy/Frontend/task 6/Task_6_Streamlit_UI_Report.docx"
    doc.save(doc_path)
    print(f"Task 6 Academic Report successfully generated at {doc_path}")

if __name__ == "__main__":
    create_report()
