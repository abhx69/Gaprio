from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

def save_contract_pdf(text: str, filename: str = "contract.pdf") -> str:
    os.makedirs("contracts", exist_ok=True)
    path = f"contracts/{filename}"

    doc = SimpleDocTemplate(path, pagesize=LETTER, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    flowables = []

    for paragraph in text.strip().split("\n\n"):
        para = Paragraph(paragraph.replace("\n", "<br />"), styles["Normal"])
        flowables.append(para)
        flowables.append(Spacer(1, 0.2 * inch))

    doc.build(flowables)
    return path
