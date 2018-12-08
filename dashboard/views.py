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
