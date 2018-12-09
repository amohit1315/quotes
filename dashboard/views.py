# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, "home.html")


def view_customer(request):
    return render(request, "view_customer.html")


def add_customer(request):
    return render(request, "add_customer.html")

def view_credit_notes(request):
    return render(request, "view_credit_notes.html")


def view_delivery_notes(request):
    return render(request, "view_delivery_notes.html")


def view_invoices(request):
    return render(request, "view_invoices.html")


def view_preference(request):
    return render(request, "view_preferences.html")


def view_product(request):
    return render(request, "view_product.html")


def view_purchase_order(request):
    return render(request, "view_purchase_order.html")


def view_quotes(request):
    return render(request, "view_quotes.html")


def view_report(request):
    return render(request, "view_report.html")


def new_invoice(request):
    return render(request, "new_invoice.html")


def new_product(request):
    return render(request, "new_product.html")


