from django.urls import path
from .views import invoice_pdf_view, main

urlpatterns = [
    path('', main, name='main'),
    path('invoice/<int:invoice_id>/pdf/', invoice_pdf_view, name='invoice_pdf'),
]
