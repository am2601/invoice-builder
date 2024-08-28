from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO


def generate_invoice_pdf(invoice):
    # Render HTML template with context data
    html_string = render_to_string('invoice.html', {'invoice': invoice})

    # Convert HTML to PDF
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    # Return PDF as a BytesIO object
    return BytesIO(pdf_file)
