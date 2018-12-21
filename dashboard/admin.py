# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Contact,Customer,Product_Service,DBUser,MasterCompany,Tax,Unit,UserTax,UserUnit

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Product_Service)
admin.site.register(DBUser)
admin.site.register(MasterCompany)
admin.site.register(Tax)
admin.site.register(Unit)
admin.site.register(UserUnit)
admin.site.register(UserTax)
