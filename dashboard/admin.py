# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Contact,Customer,Product,Service

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Service)
