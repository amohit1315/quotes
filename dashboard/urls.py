from . import views
from django.conf.urls  import *

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^customer/', views.view_customer, name='view_customer'),
    url(r'addcustomer/',views.add_customer,name='add_customer'),
    url(r'^view_credit_notes/', views.view_credit_notes, name='view_credit_notes'),
    url(r'^view_delivery_notes/', views.view_delivery_notes, name='view_delivery_notes'),
    url(r'^view_invoices/', views.view_invoices, name='view_invoices'),
    url(r'^view_preference/', views.view_preference, name='view_preference'),
    url(r'^view_product/', views.view_product, name='view_product'),
    url(r'^view_purchase_order/', views.view_purchase_order, name='view_purchase_order'),
    url(r'^view_quotes/', views.view_quotes, name='view_quotes'),
    url(r'^view_report/', views.view_report, name='view_report'),
    url(r'^new_invoice/', views.new_invoice, name='new_invoice'),
    url(r'^new_product', views.new_product, name='new_product')
]
