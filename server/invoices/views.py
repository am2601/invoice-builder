from django.http import HttpResponse
from django.shortcuts import render
from .models import Invoice
from .utils import generate_invoice_pdf


def main(request):
    return render(request, 'main.html')

def invoice_pdf_view(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    pdf = generate_invoice_pdf(invoice)

    # Create the HTTP response with the PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.number}.pdf"'

    return response
