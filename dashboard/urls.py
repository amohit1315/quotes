from . import views
from django.conf.urls  import *

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^customer/', views.view_customer, name='view_customer')
]