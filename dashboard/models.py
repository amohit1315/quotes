from __future__ import unicode_literals
from django.db import models
from uuid import uuid4

class MasterCompany(models.Model):
    phone_number = models.CharField(blank=True, null=True,max_length=45)
    company_name = models.CharField(max_length=255,primary_key=True)
    effective_date = models.DateField(blank=True, null=True)
    effective_enddate = models.DateField(blank=True, null=True)
    active = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.company_name


class DBUser(models.Model):
    first_name = models.CharField(blank=True, null=True,max_length=200)
    last_name = models.CharField(blank=True, null=True, max_length=200)
    email = models.CharField(max_length=500,primary_key=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(blank=True, null=True,max_length=200)
    designation = models.CharField(max_length=200, blank=True, null=True)
    effective_date = models.DateField(blank=True,null=True)
    effective_enddate = models.DateField(blank=True, null=True)
    master_company = models.ForeignKey(MasterCompany, blank=True, null=True,on_delete=models.SET_NULL)
    active = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    name = models.CharField(blank=True,null=True,max_length=500)
    phone = models.CharField(blank=True,null=True,max_length=500)
    email = models.CharField(blank=True,null=True,max_length=500)

    def __str__(self):
        return self.name

class Customer(models.Model):

    cust_name = models.CharField(primary_key=True,max_length=500)
    cust_phone = models.CharField(blank=True, null=True, max_length=500)
    cust_email = models.CharField(blank=True,null=True,max_length=500)
    cust_gstin = models.CharField(blank=True,null=True,max_length=500)
    cust_pan = models.CharField(blank=True,null=True,max_length=500)
    cust_tin = models.CharField(blank=True,null=True,max_length=500)
    cust_vat = models.CharField(blank=True, null=True, max_length=500)
    cust_website = models.CharField(blank=True,null=True,max_length=500)
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
    cust_facebook = models.CharField(blank=True, null=True, max_length=500)
    cust_lst = models.CharField(blank=True, null=True, max_length=500)
    cust_cst = models.CharField(blank=True, null=True, max_length=500)
    cust_service_tax_no = models.CharField(blank=True, null=True, max_length=500)
    cust_notes = models.TextField(blank=True,null=True)
    master_company = models.ForeignKey(MasterCompany, blank=True, null=True, on_delete=models.SET_NULL)
    cust_contact = models.ManyToManyField(Contact)

    def __str__(self):
        return self.cust_name

class Product_Service(models.Model):
    name = models.CharField(primary_key=True, max_length=500)
    description = models.CharField(blank=True, null=True, max_length=1000)
    quantity = models.CharField(blank=True, null=True, max_length=500)
    unit = models.CharField(max_length=500, blank=True, null=True)
    tax = models.CharField(blank=True, null=True, max_length=500)
    hsn = models.CharField(blank=True, null=True, max_length=500)
    sales_unit_price = models.CharField(blank=True, null=True, max_length=500)
    sales_currency = models.CharField(blank=True, null=True, max_length=500)
    sales_cess_percent = models.CharField(blank=True, null=True, max_length=500)
    sales_cess = models.CharField(blank=True, null=True, max_length=500)
    purchase_unit_price = models.CharField(blank=True, null=True, max_length=500)
    puchase_currency = models.CharField(blank=True, null=True, max_length=500)
    purchase_cess_percent = models.CharField(blank=True, null=True, max_length=500)
    purchase_cess = models.CharField(blank=True, null=True, max_length=500)
    master_company = models.ForeignKey(MasterCompany, blank=True, null=True, on_delete=models.SET_NULL)
    type = models.CharField(null=True,blank=True,max_length=500)
    sac = models.CharField(null=True,blank=True,max_length=500)
    def __str__(self):
        return self.name

class Tax(models.Model):
    tax_category = models.CharField(primary_key=True,max_length=500)

    def __str__(self):
        return self.tax_category

class UserTax(models.Model):
    tax_category = models.CharField(primary_key=True,max_length=500)
    master_company = models.ForeignKey(MasterCompany, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tax_category


class Unit(models.Model):
    unit_type = models.CharField(primary_key=True,max_length=500)

    def __str__(self):
        return self.unit_type

class UserUnit(models.Model):
    unit_type = models.CharField(primary_key=True,max_length=500)
    master_company = models.ForeignKey(MasterCompany, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.unit_type






