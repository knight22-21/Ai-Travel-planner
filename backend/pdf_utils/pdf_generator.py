from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_from_chat(chat_history: list) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    for msg in chat_history:
        role = msg.get("role", "Unknown").capitalize()
        text = msg.get("content", "")
        paragraph = Paragraph(f"<b>{role}:</b> {text}", styles["Normal"])
        elements.append(paragraph)
        elements.append(Spacer(1, 12))

    doc.build(elements)
    buffer.seek(0)
    return buffer
