import logging
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, Product
from .utils import generate_invoice_pdf
from .forms import InvoiceForm, ProductFormSet, UserProfileForm

logger = logging.getLogger(__name__)


def main(request):
    return render(request, 'main.html')


def overview(request):
    if not request.user.is_authenticated:
        return redirect('login')
    invoices = Invoice.objects.filter(user=request.user)
    for invoice in invoices:
        if not invoice.total_price:
            invoice.total_price = 0
    return render(request, 'overview.html', {'invoices': invoices})


def invoice_pdf_view(request, invoice_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        invoice = Invoice.objects.get(pk=invoice_id, user=request.user)
    except Invoice.DoesNotExist:
        return redirect('overview')
    pdf = generate_invoice_pdf(invoice)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.number}.pdf"'
    return response


def invoice_detail(request, invoice_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if invoice_id:
        invoice = get_object_or_404(Invoice, pk=invoice_id, user=request.user)
    else:
        invoice = Invoice(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            billing_address=request.user.billing_address,
            bank_account=request.user.bank_account,
            date=date.today()
        )
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        product_formset = ProductFormSet(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            form.save()
        if product_formset.is_valid():
            products = product_formset.save(commit=False)
            for product in products:
                if not product.name or not product.count or not product.price:
                    product.delete()
                else:
                    product.invoice = invoice
                    product.save()
            return redirect('modify_invoice', invoice.id)
    else:
        form = InvoiceForm(instance=invoice)
        product_formset = ProductFormSet(instance=invoice)
    return render(request, 'invoice.html', {
        'form': form,
        'product_formset': product_formset,
        'invoice': invoice
    })

def delete_invoice(request, invoice_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        invoice = Invoice.objects.get(pk=invoice_id, user=request.user)
        invoice.delete()
    except Invoice.DoesNotExist:
        pass
    return redirect('overview')

def delete_product(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, pk=product_id, invoice__user=request.user)
    product.delete()
    referrer = request.META.get('HTTP_REFERER')
    if referrer:
        return HttpResponseRedirect(referrer)

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_profile = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'user_profile.html', {'form': form})
