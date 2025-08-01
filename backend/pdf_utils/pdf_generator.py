from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO


# Custom style for chat messages
chat_style = ParagraphStyle(
    name="ChatStyle",
    fontSize=11,
    leading=14,
    spaceAfter=10
)

def generate_pdf_from_chat(chat_history: list) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    for msg in chat_history:
        role = msg.get("role", "Unknown").capitalize()
        text = msg.get("content", "")
        timestamp = msg.get("time", "")  # Optional timestamp

        display_text = f"<b>{role}</b>: {text}"
        if timestamp:
            display_text += f"<br/><font size=8 color='grey'>{timestamp}</font>"

        paragraph = Paragraph(display_text, chat_style)
        elements.append(paragraph)
        elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)
    return buffer
