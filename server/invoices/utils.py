from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO


def generate_invoice_pdf(invoice):
    html_string = render_to_string('invoice_pdf.html', {'invoice': invoice})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    return BytesIO(pdf_file)
