from django.urls import path
from .views import invoice_pdf_view, main, overview, invoice_detail, delete_invoice, delete_product, user_profile

urlpatterns = [
    path('', main, name='main'),
    path('overview/', overview, name='overview'),
    path('user_profile/', user_profile, name='user_profile'),
    path('invoice/', invoice_detail, name='create_invoice'),
    path('invoice/<int:invoice_id>', invoice_detail, name='modify_invoice'),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf_view, name='invoice_pdf'),
    path('invoice/<int:invoice_id>/delete/', delete_invoice, name='delete_invoice'),
    path('product/<int:product_id>/delete/', delete_product, name='delete_product'),
]
