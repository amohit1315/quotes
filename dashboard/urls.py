from . import views
from django.conf.urls  import *

urlpatterns = [
    url(r'^$', views.home, name='home'),
]