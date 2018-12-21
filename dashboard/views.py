# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from models import DBUser,MasterCompany,Customer,Product_Service,Contact,Tax,Unit,UserUnit,UserTax
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password


# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, "landingpage.html")


def gologin(request):
    return render(request, 'loginpage.html')

def loginpage(request):
    return render(request, "signuppage.html")

def gohome(request):
    return  redirect('index')


def signup(request):
    if request.method == 'POST':
        user = User()
        dbuser = DBUser()
        master_company = MasterCompany()
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        company = request.POST['company']
        phone = request.POST['phone']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        user.username = email
        user.set_password(password)
        user.email = email
        user.is_active = False
        user.save()
        print user.password

        master_company.company_name = company
        master_company.phone_number = phone
        master_company.country = country
        master_company.city = city
        master_company.state = state
        master_company.effective_date = user.date_joined
        master_company.effective_enddate = user.date_joined + timedelta(days=30)
        master_company.save()

        dbuser.first_name = fname
        dbuser.last_name = lname
        dbuser.email = email
        dbuser.password = password
        mas_company = MasterCompany.objects.get(company_name=company)
        dbuser.master_company = mas_company
        dbuser.effective_date = user.date_joined
        dbuser.effective_enddate = user.date_joined + timedelta(days=30)
        dbuser.active = "Inactive"
        dbuser.save()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        username = user.username
        db_user = DBUser.objects.get(pk=username)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        db_user.active = "Active"
        db_user.save()
        login(request, user)
        return redirect('home')
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signin(request):
    if request.method == 'POST':
        username = request.POST['usern']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        #user = User.objects.get(username=username,password=password)
        #user.backend = 'django.contrib.auth.backends.ModelBackend'
        print username, password
        print user

        if user is not None:
            login(request, user)
            return redirect('home')
        else:

            return HttpResponse("INVALID LOGIN DETAILS")

@login_required(login_url="/")
def home(request):
    return render(request, "home.html")


def view_customer(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    print m
    customers = Customer.objects.filter(master_company=m)
    print customers

    return render(request, "view_customer.html",{'customers':customers})


def new_customer(request):
    return render(request, "new_customer.html")

def save_customer(request):
    if request.method == 'POST':
        customer_name=request.POST['cname']
        customer_phone=request.POST['cphone']
        customer_email=request.POST['cemail']
        customer_gstin=request.POST['cgstin']
        customer_tin=request.POST['ctin']
        customer_pan=request.POST['cpan']
        customer_vat=request.POST['cvat']
        customer_website=request.POST['cweb']
        customer_contact_person_name = request.POST['cperson']
        customer_contact_person_phone = request.POST['cpphone']
        customer_contact_person_email=request.POST['cemail']
        customer_contact_person_name_1 = request.POST['cperson1']
        customer_contact_person_phone_1 = request.POST['cpphone1']
        customer_contact_person_email_1 = request.POST['cemail1']
        customer_billing_address = request.POST['caddress']
        customer_billing_country = request.POST['ccountry']
        customer_billing_state = request.POST['cstate']
        customer_billing_city = request.POST['ccity']
        customer_billing_pincode = request.POST['cpincode']
        customer_shipping_address = request.POST['csaddress']
        customer_shipping_country = request.POST['cscountry']
        customer_shipping_state = request.POST['csstate']
        customer_shipping_city = request.POST['cscity']
        customer_shipping_pincode = request.POST['cspincode']
        customer_facebook = request.POST['cfacebook']
        customer_lst = request.POST['clst']
        customer_cst = request.POST['ccst']
        customer_service_tax_no = request.POST['cstn']
        customer_notes = request.POST['cnotes']
        cust = Customer()
        cust.cust_name = customer_name
        cust.cust_phone = customer_phone
        cust.cust_email = customer_email
        cust.cust_gstin = customer_gstin
        cust.cust_pan = customer_pan
        cust.cust_tin = customer_tin
        cust.cust_vat = customer_vat
        cust.cust_website = customer_website
        cust.cust_company_address = customer_billing_address
        cust.cust_country = customer_billing_country
        cust.cust_state = customer_billing_state
        cust.cust_city = customer_billing_city
        cust.cust_pincode = customer_billing_pincode
        if customer_shipping_address :
            cust.cust_shipping_address = customer_shipping_address
        else:
            cust.cust_shipping_address = customer_billing_address
        if customer_shipping_country :
            cust.cust_shiiping_country = customer_shipping_country
        else:
            cust.cust_shiiping_country = customer_billing_country
        if customer_shipping_state :
            cust.cust_shipping_state = customer_shipping_state
        else:
            cust.cust_shipping_state = customer_billing_state
        if customer_shipping_city :
            cust.cust_shipping_city = customer_shipping_city
        else:
            cust.cust_shipping_city = customer_billing_city
        if customer_shipping_pincode :
            cust.cust_shipping_pincode = customer_shipping_pincode
        else:
            cust.cust_shipping_pincode = customer_billing_pincode
        cust.cust_facebook = customer_facebook
        cust.cust_lst = customer_lst
        cust.cust_cst = customer_cst
        cust.cust_service_tax_no = customer_service_tax_no
        cust.cust_notes = customer_notes
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        print m
        cust.master_company = m
        cust.save()
        customer_contact = Contact.objects.create(name=customer_contact_person_name,phone=customer_contact_person_phone,email=customer_contact_person_email)
        c = Customer.objects.get(cust_name=customer_name)
        c.cust_contact.add(customer_contact)
        c.save()
        if customer_contact_person_email_1 and customer_contact_person_phone_1 and customer_contact_person_name_1 :
            customer_contact_1 = Contact.objects.create(name=customer_contact_person_name_1,phone=customer_contact_person_phone_1,email=customer_contact_person_email_1)
            cu = Customer.objects.get(cust_name=customer_name)
            cu.cust_contact.add(customer_contact_1)
            cu.save()
        return HttpResponse("Added Successfully")

def view_credit_notes(request):
    return render(request, "view_credit_notes.html")


def view_delivery_notes(request):
    return render(request, "view_delivery_notes.html")


def view_invoices(request):
    return render(request, "view_invoices.html")


def view_preference(request):
    return render(request, "view_preferences.html")


def view_product(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    ps = Product_Service.objects.filter(master_company=m)
    return render(request, "view_product.html", {'ps':ps})


def view_purchase_order(request):
    return render(request, "view_purchase_order.html")


def view_quotes(request):
    return render(request, "view_quotes.html")


def view_report(request):
    return render(request, "view_report.html")


def new_invoice(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    unit = Unit.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_invoice.html", {"prod": prod, "client": client , 'tax' : tax, 'unit': unit ,'usertax' : usertax, userunit : 'userunit'})


def new_product(request):
    return render(request, "new_product.html")

def save_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('pname','')
        product_description = request.POST.get('pdesc','')
        product_sales_price = request.POST.get('psprice','')
        product_sales_cess_percent = request.POST.get('pscesspercent',False)
        product_sales_currency = request.POST.get('pscurrency',False)
        product_sales_cess = request.POST.get('pscess',False)
        product_quantity = request.POST.get('pquant',False)
        product_unit = request.POST.get('punit',False)
        product_tax = request.POST.get('ptax',False)
        product_hsn = request.POST.get('phsn',False)
        product_purchase_price = request.POST.get('ppprice',False)
        product_purchase_cess_percent = request.POST.get('ppcesspercent',False)
        product_purchase_currency = request.POST.get('ppcurrency',False)
        product_purchase_cess = request.POST.get('ppcess',False)
        prod = Product_Service()
        if product_name != 'False':
            prod.name = product_name
            if product_description != 'False':
                prod.description = product_description
            else :
                prod.description = ''
            if product_sales_price != 'False':
                prod.sales_unit_price = product_sales_price
            else:
                prod.sales_unit_price = ''
            if product_quantity != 'False':
                prod.quantity = product_quantity
            else :
                prod.quantity = ''
            if product_unit != 'False' :
                prod.unit = product_unit
            else:
                prod.unit = ''
            if product_tax != 'False':
                prod.tax = product_tax
            else:
                prod.tax = ''
            if product_hsn != 'False':
                prod.hsn = product_hsn
            else:
                prod_hsn = ''
            if product_sales_price !='False':
                prod.sales_unit_price = product_sales_price
            else:
                prod.sales_unit_price = ''
            if product_sales_cess_percent != 'False':
                prod.sales_cess_percent = product_sales_cess_percent
            else:
                prod.sales_cess_percent = ''
            if product_sales_cess !='False':
                prod.sales_cess = product_sales_cess
            else:
                prod.sales_cess = ''
            if product_sales_currency != 'False':
                prod.sales_currency = product_sales_currency
            else:
                prod.sales_currency = ''
            if product_purchase_price != 'False':
                prod.purchase_unit_price = product_purchase_price
            else:
                prod.purchase_unit_price = ''
            if product_purchase_cess_percent != 'False':
                prod.purchase_cess_percent = product_purchase_cess_percent
            else:
                prod.purchase_cess_percent = ''
            if product_purchase_cess != 'False':
                prod.purchase_cess = product_purchase_cess
            else:
                prod.purchase_cess = ''
            if product_purchase_currency != 'False':
                prod.purchase_currency = product_purchase_currency
            else:
                prod.purchase_currency = ''
            prod.type = 'Product'
            prod.sac= ''

        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        prod.master_company = m
        prod.save()
        return HttpResponse("Added Successfully")

def save_service(request):
    if request.method == 'POST':
        service_name = request.POST.get('sname', False)
        service_description = request.POST.get('sdesc', False)
        service_sales_price = request.POST.get('ssprice', False)
        service_sales_cess_percent = request.POST.get('sscesspercent', False)
        service_sales_currency = request.POST.get('sscurrency', False)
        service_sales_cess = request.POST.get('sscess', False)
        service_unit = request.POST.get('sunit', False)
        service_tax = request.POST.get('stax', False)
        service_sac = request.POST.get('ssac', False)
        service_purchase_price = request.POST.get('spprice', False)
        service_purchase_cess_percent = request.POST.get('spcesspercent', False)
        service_purchase_currency = request.POST.get('spcurrency', False)
        service_purchase_cess = request.POST.get('spcess', False)
        service = Product_Service()
        service.name = service_name
        if service_description != 'False':
            service.description = service_description
        else:
            service.description = ''
        if service_sales_price != 'False':
            service.sales_unit_price = service_sales_price
        else:
            service.sales_unit_price = ''
        if service_sac != 'False':
            service.sac = service_sac
        else:
            service.sac = ''
        if service_unit != 'False':
            service.unit = service_unit
        else:
            service.unit = ''
        if service_tax != 'False':
            service.tax = service_tax
        else:
            service.tax = ''
        service.quantity = ''
        service.hsn = ''
        if service_sales_price != 'False':
            service.sales_unit_price = service_sales_price
        else:
            service.sales_unit_price = ''
        if service_sales_cess_percent != 'False':
            service.sales_cess_percent = service_sales_cess_percent
        else:
            service.sales_cess_percent = ''
        if service_sales_cess != 'False':
            service.sales_cess = service_sales_cess
        else:
            service.sales_cess = ''
        if service_sales_currency != 'False':
            service.sales_currency = service_sales_currency
        else:
            service.sales_currency = ''
        if service_purchase_price != 'False':
            service.purchase_unit_price = service_purchase_price
        else:
            service.purchase_unit_price = ''
        if service_purchase_cess_percent != 'False':
            service.purchase_cess_percent = service_purchase_cess_percent
        else:
            service.purchase_cess_percent = ''
        if service_purchase_cess != 'False':
            service.purchase_cess = service_purchase_cess
        else:
            service.purchase_cess = ''
        if service_purchase_currency != 'False':
            service.purchase_currency = service_purchase_currency
        else:
            service.purchase_currency = ''
        service.type = 'Service'
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        service.master_company = m
        service.save()
        return HttpResponse("Added Successfully")







