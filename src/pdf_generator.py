from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def create_pdf(transcript, analysis, output_path):

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "MeetMind",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI Audio & Video Intelligence Report",
            styles["Heading3"]
        )
    )

    story.append(Spacer(1, 20))

    # -----------------------------
    # AI Analysis
    # -----------------------------

    story.append(
        Paragraph(
            "AI Analysis",
            heading_style
        )
    )

    story.append(Spacer(1, 10))

    # Convert analysis lines into paragraphs
    for line in analysis.split("\n"):

        line = line.strip()

        if line:

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

            story.append(
                Spacer(1, 5)
            )

    # -----------------------------
    # Transcript
    # -----------------------------

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "Transcript",
            heading_style
        )
    )

    story.append(Spacer(1, 10))

    for line in transcript.split("\n"):

        line = line.strip()

        if line:

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

    # -----------------------------
    # Build PDF
    # -----------------------------

    document.build(story)