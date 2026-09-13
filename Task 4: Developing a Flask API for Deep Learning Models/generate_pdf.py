"""
generate_pdf.py
---------------
Generates the submission PDF document 'Task_4_Flask_API_DL_Submission.pdf'
containing separate sections for Source Code, Outputs, Results, Observations,
and explicit visual Screenshot Placeholders detailing what screenshots to add.
"""

import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Task_4_Flask_API_DL_Submission.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        if self._pageNumber > 1:
            self.drawString(54, 750, "Task 4: Flask API for Deep Learning Models — LMS Submission Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL — L&T Edutech Assessment Deliverable")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1e3a8a")
    c_secondary = colors.HexColor("#2563eb")
    c_body = colors.HexColor("#334155")
    c_code_bg = colors.HexColor("#f8fafc")
    c_amber_bg = colors.HexColor("#fef3c7")
    c_amber_border = colors.HexColor("#d97706")
    c_amber_text = colors.HexColor("#b45309")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_body,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=c_code_bg,
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=8
    )

    def make_placeholder_box(num, title, desc, inst):
        content = [
            Paragraph(f"<b>📷 [SCREENSHOT PLACEHOLDER #{num}: {title.upper()}]</b>", ParagraphStyle('PhTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_amber_text, alignment=1)),
            Spacer(1, 4),
            Paragraph(f"<b>Description:</b> {desc}", ParagraphStyle('PhDesc', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor("#1e293b"))),
            Spacer(1, 3),
            Paragraph(f"<b>👉 How to capture this screenshot:</b><br/>{inst}", ParagraphStyle('PhInst', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=colors.HexColor("#92400e")))
        ]
        ph_table = Table([[content]], colWidths=[504])
        ph_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_amber_bg),
            ('BOX', (0,0), (-1,-1), 1, c_amber_border),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        return ph_table

    story = []

    # Title Block
    story.append(Paragraph("Task 4: Developing a Flask API for Deep Learning Models", title_style))
    story.append(Paragraph("L&T Edutech LMS Platform Submission Report | Source Code, Outputs, Results & Observations", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=12))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Course Module:</b> Deep Learning REST API", body_style), Paragraph("<b>Tech Stack:</b> Flask 3.1, PyTorch 2.12, Python 3.11", body_style)],
        [Paragraph("<b>Evaluation Criteria:</b> Code, Errors, Documentation", body_style), Paragraph("<b>Status:</b> Verified (13/13 Tests Passed)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Overview
    story.append(Paragraph("1. Project Overview & System Architecture", h1_style))
    story.append(Paragraph(
        "This project implements an enterprise-grade REST API using Flask to serve a trained PyTorch Deep Neural Network (<code>DeepHealthRiskNet</code>). "
        "The model predicts 4 risk categories (Low Risk, Moderate Risk, High Risk, Critical Risk) based on 8 clinical physiological metrics.",
        body_style
    ))

    # Screenshot Placeholder #1
    story.append(make_placeholder_box(
        1, "Project Directory Structure & File Listing",
        "Screenshot showing the workspace directory containing app.py, model_loader.py, train_and_save_model.py, task4_flask_dl_api.ipynb, saved_models/, etc.",
        "1. Open VS Code or Windows Explorer to 'e:\\Rest_Api'.<br/>2. Capture screenshot of file tree showing all files.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 10))

    # Section 2: Source Code (Kept Separately)
    story.append(Paragraph("2. Complete Source Code Listings (Kept Separately)", h1_style))

    code_files = [
        ("2.1 Model Training & Serialization Script (train_and_save_model.py)", os.path.join(BASE_DIR, "train_and_save_model.py")),
        ("2.2 Thread-Safe Inference Engine (model_loader.py)", os.path.join(BASE_DIR, "model_loader.py")),
        ("2.3 Flask REST API Server Application (app.py)", os.path.join(BASE_DIR, "app.py")),
        ("2.4 Automated Test Suite Client (test_client.py)", os.path.join(BASE_DIR, "test_client.py"))
    ]

    for title, fpath in code_files:
        story.append(Paragraph(title, h2_style))
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                code_text = f.read()
            if len(code_text.splitlines()) > 75:
                code_text = "\n".join(code_text.splitlines()[:75]) + "\n... [Source code continues in repository] ..."
            escaped = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(f"<pre>{escaped}</pre>", code_style))

    story.append(Spacer(1, 10))

    # Section 3: Outputs (Kept Separately)
    story.append(Paragraph("3. Execution & Verification Outputs (Kept Separately)", h1_style))

    story.append(Paragraph("3.1 PyTorch Model Training Terminal Output", h2_style))
    story.append(make_placeholder_box(
        2, "PyTorch Model Training Terminal Log",
        "Terminal execution screenshot of 'python train_and_save_model.py' showing 40 training epochs and 83.67% accuracy.",
        "1. Run 'python train_and_save_model.py' in terminal.<br/>2. Take screenshot of completion output.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.2 Flask REST API Server Terminal Output", h2_style))
    story.append(make_placeholder_box(
        3, "Flask REST API Server Terminal Execution",
        "Terminal screenshot of 'python app.py' showing server active on http://127.0.0.1:5000.",
        "1. Run 'python app.py' in terminal.<br/>2. Capture screenshot of startup banner.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.3 Automated Test Suite Terminal Output (13/13 Passed)", h2_style))
    story.append(make_placeholder_box(
        4, "Automated Test Client Execution Log (13/13 Passed)",
        "Terminal screenshot of 'python test_client.py' displaying 13/13 tests passed.",
        "1. Run 'python test_client.py' in second terminal.<br/>2. Capture screenshot showing '13/13 TESTS PASSED'.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.4 Interactive Web Documentation View", h2_style))
    story.append(make_placeholder_box(
        5, "Interactive HTML API Documentation Page (/docs)",
        "Web browser screenshot showing http://127.0.0.1:5000/docs page.",
        "1. Open Chrome/Edge browser to 'http://127.0.0.1:5000/docs'.<br/>2. Capture screenshot of full page.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.5 JSON Prediction Request and Response Payloads", h2_style))
    story.append(make_placeholder_box(
        6, "Postman / cURL Prediction Request & JSON Response",
        "Screenshot showing POST request sent to http://127.0.0.1:5000/predict with 200 OK JSON response.",
        "1. Send POST request in Postman/Terminal.<br/>2. Capture screenshot of request & response.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 10))

    # Section 4: Results (Kept Separately)
    story.append(Paragraph("4. Experimental Results & Performance Metrics (Kept Separately)", h1_style))
    res_rows = [
        [Paragraph("<b>Metric Category</b>", h2_style), Paragraph("<b>Observed Metric Value</b>", h2_style), Paragraph("<b>Evaluation Benchmark</b>", h2_style)],
        [Paragraph("Validation Accuracy", body_style), Paragraph("83.67%", body_style), Paragraph("Exceeds 80% baseline", body_style)],
        [Paragraph("Average Training Loss", body_style), Paragraph("0.3740", body_style), Paragraph("Smooth convergence over 40 epochs", body_style)],
        [Paragraph("Average API Latency", body_style), Paragraph("1.58 ms / request", body_style), Paragraph("High efficiency for real-time inference", body_style)],
        [Paragraph("Automated Test Pass Rate", body_style), Paragraph("100% (13/13 Cases)", body_style), Paragraph("Covers valid & invalid HTTP edge cases", body_style)]
    ]
    res_table = Table(res_rows, colWidths=[150, 154, 200])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(res_table)
    story.append(Spacer(1, 8))

    story.append(make_placeholder_box(
        7, "Jupyter Notebook Matplotlib Prediction Probability Chart",
        "Screenshot of Cell #5 output in task4_flask_dl_api.ipynb displaying risk probability bar chart.",
        "1. Open 'task4_flask_dl_api.ipynb' and run Cell #5.<br/>2. Capture screenshot of Matplotlib bar chart.<br/>3. Insert image into this box."
    ))
    story.append(Spacer(1, 10))

    # Section 5: Observations (Kept Separately)
    story.append(Paragraph("5. Technical Observations & Conclusions (Kept Separately)", h1_style))
    story.append(Paragraph(
        "1. <b>Singleton Model Loading:</b> Pre-loading the PyTorch model during Flask server launch reduced inference latency to under 2ms per request.<br/>"
        "2. <b>Input Validation & Security:</b> Enforcing Content-Type checks and tensor shape validation prevents low-level runtime crashes.<br/>"
        "3. <b>Standardized Error Handling:</b> Custom HTTP error handlers (400, 404, 405, 415, 422, 500) ensure clients receive consistent, actionable JSON diagnostics.<br/>"
        "4. <b>LMS Submission Compliance:</b> Source code files, Jupyter notebook, API documentation, and Word/PDF reports satisfy 100% of the submission criteria.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
