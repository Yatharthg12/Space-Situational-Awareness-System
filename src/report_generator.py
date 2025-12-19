from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import pandas as pd
from datetime import datetime
import os

def generate_pdf_report(
    csv_path="outputs/conjunction_events.csv",
    output_pdf="outputs/SSA_Report.pdf",
    total_objects=50,
    horizon_hours=48
):
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    def footer(page_num):
        c.setFont("Helvetica", 9)
        c.setFillGray(0.4)
        c.drawRightString(width - 2 * cm, 1.5 * cm, f"Page {page_num}")

    page = 1

    # -------------------------
    # TITLE PAGE
    # -------------------------
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(
        width / 2,
        height - 4 * cm,
        "Space Situational Awareness Report"
    )

    c.setFont("Helvetica", 12)
    c.drawCentredString(
        width / 2,
        height - 5.5 * cm,
        f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )

    c.setFont("Helvetica", 11)
    c.drawCentredString(
        width / 2,
        height - 7 * cm,
        "Short-Horizon Conjunction Monitoring Summary"
    )

    footer(page)
    c.showPage()
    page += 1

    # -------------------------
    # LOAD DATA
    # -------------------------
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame()

    total_events = len(df)
    high_risk = len(df[df["risk"] == "HIGH"]) if not df.empty else 0
    medium_risk = len(df[df["risk"] == "MEDIUM"]) if not df.empty else 0

    # -------------------------
    # EXECUTIVE SUMMARY
    # -------------------------
    c.setFont("Helvetica-Bold", 15)
    c.drawString(2 * cm, height - 3 * cm, "Executive Summary")

    c.setFont("Helvetica", 11)
    text = c.beginText(2 * cm, height - 4.2 * cm)

    if total_events == 0:
        text.textLine(
            "No conjunction events exceeding alert thresholds were detected"
        )
        text.textLine(
            f"within the {horizon_hours}-hour monitoring horizon."
        )
        text.textLine(
            "The orbital environment is assessed as nominal for the"
        )
        text.textLine(
            "tracked object set during this period."
        )
    else:
        text.textLine(
            f"A total of {total_events} conjunction events were detected"
        )
        text.textLine(
            f"within the {horizon_hours}-hour monitoring horizon."
        )
        text.textLine(
            "Events were classified based on deterministic distance thresholds."
        )

    c.drawText(text)

    footer(page)
    c.showPage()
    page += 1

    # -------------------------
    # SYSTEM OVERVIEW
    # -------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 3 * cm, "1. System Overview")

    c.setFont("Helvetica", 11)
    text = c.beginText(2 * cm, height - 4.2 * cm)
    text.textLine(
        "This report summarizes short-horizon Space Situational Awareness (SSA)"
    )
    text.textLine(
        "analysis performed using physics-based orbit propagation."
    )
    text.textLine(
        "Public Two-Line Element (TLE) data was used as input."
    )
    text.textLine(
        "All objects were propagated using the SGP4 model in an"
    )
    text.textLine(
        "Earth-Centered Inertial (ECI) reference frame."
    )
    c.drawText(text)

    footer(page)
    c.showPage()
    page += 1

    # -------------------------
    # MONITORING SUMMARY
    # -------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 3 * cm, "2. Monitoring Summary")

    c.setFont("Helvetica", 11)
    c.drawString(
        2 * cm, height - 4.5 * cm,
        f"Total objects monitored: {total_objects}"
    )
    c.drawString(
        2 * cm, height - 5.5 * cm,
        f"Monitoring horizon: {horizon_hours} hours"
    )
    c.drawString(
        2 * cm, height - 6.5 * cm,
        f"Total conjunction events detected: {total_events}"
    )
    c.drawString(
        2 * cm, height - 7.5 * cm,
        f"High risk events (< 2 km): {high_risk}"
    )
    c.drawString(
        2 * cm, height - 8.5 * cm,
        f"Medium risk events (2–10 km): {medium_risk}"
    )

    footer(page)
    c.showPage()
    page += 1

    # -------------------------
    # CONJUNCTION EVENTS
    # -------------------------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2 * cm, height - 3 * cm, "3. Detected Conjunction Events")

    c.setFont("Helvetica", 11)
    y = height - 4.5 * cm

    if df.empty:
        c.drawString(
            2 * cm, y,
            "No conjunction events met the alerting thresholds."
        )
        c.drawString(
            2 * cm, y - 1 * cm,
            "This indicates adequate spatial separation for the monitored objects."
        )
    else:
        c.setFont("Helvetica", 10)
        for _, row in df.iterrows():
            line = (
                f"{row['object_1']} vs {row['object_2']} | "
                f"Distance: {row['distance_km']} km | "
                f"Risk: {row['risk']}"
            )
            c.drawString(2 * cm, y, line)
            y -= 0.7 * cm
            if y < 3 * cm:
                footer(page)
                c.showPage()
                page += 1
                y = height - 3 * cm

    footer(page)
    c.save()
