from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from sample_data import invoice_data
import os

def generate_invoice(data):
    os.makedirs("output", exist_ok=True)
    filename = f"output/{data['invoice_number']}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # — Header —
    c.setFillColor(colors.HexColor("#2563eb"))
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(2 * cm, height - 50, "INVOICE")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 2 * cm, height - 35, f"Invoice #: {data['invoice_number']}")
    c.drawRightString(width - 2 * cm, height - 50, f"Date: {data['date']}")
    c.drawRightString(width - 2 * cm, height - 65, f"Due: {data['due_date']}")

    # — From / To —
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2 * cm, height - 110, "FROM")
    c.drawString(10 * cm, height - 110, "TO")
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 125, data["from"]["name"])
    c.drawString(2 * cm, height - 140, data["from"]["email"])
    c.drawString(2 * cm, height - 155, data["from"]["phone"])
    c.drawString(10 * cm, height - 125, data["to"]["name"])
    c.drawString(10 * cm, height - 140, data["to"]["email"])
    c.drawString(10 * cm, height - 155, data["to"]["address"])

    # — Table Header —
    y = height - 200
    c.setFillColor(colors.HexColor("#f1f5f9"))
    c.rect(2 * cm, y - 5, width - 4 * cm, 20, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(2.5 * cm, y, "Description")
    c.drawString(12 * cm, y, "Qty")
    c.drawString(14 * cm, y, "Rate")
    c.drawString(17 * cm, y, "Total")

    # — Table Rows —
    c.setFont("Helvetica", 10)
    y -= 25
    subtotal = 0
    for item in data["items"]:
        total = item["quantity"] * item["rate"]
        subtotal += total
        c.drawString(2.5 * cm, y, item["description"])
        c.drawString(12 * cm, y, str(item["quantity"]))
        c.drawString(14 * cm, y, f"${item['rate']:.2f}")
        c.drawString(17 * cm, y, f"${total:.2f}")
        y -= 20

    # — Totals —
    y -= 10
    c.line(2 * cm, y, width - 2 * cm, y)
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(14 * cm, y, "TOTAL:")
    c.drawString(17 * cm, y, f"${subtotal:.2f}")

    # — Notes —
    y -= 50
    c.setFont("Helvetica-Bold", 9)
    c.drawString(2 * cm, y, "Notes:")
    c.setFont("Helvetica", 9)
    c.drawString(2 * cm, y - 15, data["notes"])

    c.save()
    print(f"✅ Invoice saved to {filename}")

generate_invoice(invoice_data)