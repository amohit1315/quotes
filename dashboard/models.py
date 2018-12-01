from __future__ import unicode_literals
from django.db import models


class Contact(models.Model):
    name = models.CharField(blank=True,null=True,max_length=500)
    phone = models.CharField(blank=True,null=True,max_length=500)
    email = models.CharField(blank=True,null=True,max_length=500)

    def __str__(self):
        return self.name

class Customer(models.Model):
    cust_name = models.CharField(primary_key=True,max_length=500)
    cust_type = models.CharField(blank=True, null=True, max_length=500)
    cust_phone = models.CharField(blank=True, null=True, max_length=500)
    cust_email = models.CharField(blank=True,null=True,max_length=500)
    cust_gstin = models.CharField(blank=True,null=True,max_length=500)
    cust_pan = models.CharField(blank=True,null=True,max_length=500)
    cust_tin = models.CharField(blank=True,null=True,max_length=500)
    cust_vat = models.CharField(blank=True, null=True, max_length=500)
    cust_website = models.CharField(blank=True,null=True,max_length=500)
    cust_sez = models.CharField(blank=True,null=True,max_length=500)
    cust_company_address = models.CharField(blank=True, null=True, max_length=500)
    cust_country = models.CharField(blank=True, null=True, max_length=500)
    cust_state = models.CharField(blank=True, null=True, max_length=500)
    cust_city = models.CharField(blank=True, null=True, max_length=500)
    cust_pincode = models.CharField(blank=True, null=True, max_length=500)
    cust_shipping_address = models.CharField(blank=True, null=True, max_length=500)
    cust_shiiping_country = models.CharField(blank=True, null=True, max_length=500)
    cust_shipping_state = models.CharField(blank=True, null=True, max_length=500)
    cust_shipping_city = models.CharField(blank=True, null=True, max_length=500)
    cust_shipping_pincode = models.CharField(blank=True, null=True, max_length=500)
    cust_shipping_gstin = models.CharField(blank=True, null=True, max_length=500)
    cust_facebook = models.CharField(blank=True, null=True, max_length=500)
    cust_lst = models.CharField(blank=True, null=True, max_length=500)
    cust_cst = models.CharField(blank=True, null=True, max_length=500)
    cust_service_tax_no = models.CharField(blank=True, null=True, max_length=500)
    cust_notes = models.TextField(blank=True,null=True)
    cust_contact = models.ManyToManyField(Contact)

    def __str__(self):
        return self.cust_name

