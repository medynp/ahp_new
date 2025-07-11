from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO

def export_ranking_to_pdf(data, filename="ranking_guru.pdf"):
    """
    data: list of dict, setiap dict berisi data guru dan total_score
    filename: nama file pdf yang dihasilkan
    """

    # Urutkan data berdasarkan total_score descending
    sorted_data = sorted(data, key=lambda x: x["total_score"], reverse=True)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Hasil Perangkingan Guru")

    table_data = [["Peringkat", "Nama Guru", "Total Skor"]]
    for i, d in enumerate(sorted_data, 1):
        table_data.append([str(i), d["nama_guru"], f"{d['total_score']:.4f}"])

    table = Table(table_data, colWidths=[50, 250, 100])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a90e2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    table_width, table_height = table.wrapOn(c, width - 100, height)
    table.drawOn(c, 50, height - 100 - table_height)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
