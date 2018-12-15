from . import views
from django.conf.urls  import *
from django.contrib.auth import views as v

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^loginpage/$', views.gologin, name='gologin'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^sigin/', views.loginpage, name='signin'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^home/', views.gohome, name='gohome'),
    url(r'^dashboard/', views.home, name='home'),
    url(r'^view_customer/', views.view_customer, name='view_customer'),
    url(r'^new_customer/',views.new_customer,name='new_customer'),
    url(r'^save_customer',views.save_customer,name='save_customer'),
    url(r'^view_credit_notes/', views.view_credit_notes, name='view_credit_notes'),
    url(r'^view_delivery_notes/', views.view_delivery_notes, name='view_delivery_notes'),
    url(r'^view_invoices/', views.view_invoices, name='view_invoices'),
    url(r'^view_preference/', views.view_preference, name='view_preference'),
    url(r'^view_product/', views.view_product, name='view_product'),
    url(r'^view_purchase_order/', views.view_purchase_order, name='view_purchase_order'),
    url(r'^view_quotes/', views.view_quotes, name='view_quotes'),
    url(r'^view_report/', views.view_report, name='view_report'),
    url(r'^new_invoice/', views.new_invoice, name='new_invoice'),
    url(r'^new_product', views.new_product, name='new_product'),
    url(r'^save_product', views.save_product, name='save_product'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate')
]
