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
from models import DBUser,MasterCompany,Customer,Product_Service,Contact,Tax,Unit,UserUnit,UserTax,Invoice,Credit_Notes,Delivery_Notes,Dummy_Product,Purchase_Order,Quotes
from datetime import datetime, timedelta
import csv
from django.core.files.storage import FileSystemStorage
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
    customers = Customer.objects.filter(master_company=m)
    return render(request, "view_customer.html",{'customers':customers})


def export_customer(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    customers = Customer.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Company Name', 'Phone', 'Email', 'GSTIN','PAN','TIN','VAT','Website','Billing Address','Country','State','City','Pincode','Shipping Address','Country','State','City','Pincode','Facebook','LST','CST','Service Tax No.','Notes','Primary Contact Name','Primary Contact Phone','Primary Contact Email', 'Secondary Contact Name', 'Seconadary Contact Phone','Secondary Contact Email'])
    for cust in customers:
        writer.writerow([cust.cust_name,cust.cust_phone,cust.cust_email,cust.cust_gstin,cust.cust_pan,cust.cust_tin,cust.cust_vat,cust.cust_website,cust.cust_company_address,cust.cust_country,cust.cust_state,cust.cust_city,cust.cust_pincode,cust.cust_shipping_address,cust.cust_shiiping_country,cust.cust_shipping_state,cust.cust_shipping_city,cust.cust_shipping_pincode,cust.cust_facebook,cust.cust_lst,cust.cust_cst,cust.cust_service_tax_no,cust.cust_notes,cust.cust_contact.all()[0].name,cust.cust_contact.all()[0].phone,cust.cust_contact.all()[0].email,cust.cust_contact.all()[1].name,cust.cust_contact.all()[1].phone,cust.cust_contact.all()[1].email])
    return response


def import_customer(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)
        for fields in reader:
            customer_name = fields[0]
            customer_phone = fields[1]
            customer_email = fields[2]
            customer_gstin = fields[3]
            customer_pan = fields[4]
            customer_tin = fields[5]
            customer_vat = fields[6]
            customer_website = fields[7]
            customer_billing_address = fields[8]
            customer_billing_country = fields[9]
            customer_billing_state = fields[10]
            customer_billing_city = fields[11]
            customer_billing_pincode = fields[12]
            customer_shipping_address = fields[13]
            customer_shipping_country = fields[14]
            customer_shipping_state = fields[15]
            customer_shipping_city = fields[16]
            customer_shipping_pincode = fields[17]
            customer_facebook = fields[18]
            customer_lst = fields[19]
            customer_cst = fields[20]
            customer_service_tax_no = fields[21]
            customer_notes = fields[22]
            customer_contact_person_name = fields[23]
            customer_contact_person_phone = fields[24]
            customer_contact_person_email = fields[25]
            customer_contact_person_name_1 = fields[26]
            customer_contact_person_phone_1 = fields[27]
            customer_contact_person_email_1 = fields[28]
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
            if customer_shipping_address:
                cust.cust_shipping_address = customer_shipping_address
            else:
                cust.cust_shipping_address = customer_billing_address
            if customer_shipping_country:
                cust.cust_shiiping_country = customer_shipping_country
            else:
                cust.cust_shiiping_country = customer_billing_country
            if customer_shipping_state:
                cust.cust_shipping_state = customer_shipping_state
            else:
                cust.cust_shipping_state = customer_billing_state
            if customer_shipping_city:
                cust.cust_shipping_city = customer_shipping_city
            else:
                cust.cust_shipping_city = customer_billing_city
            if customer_shipping_pincode:
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
            cust.master_company = m
            cust.save()
            customer_contact = Contact.objects.create(name=customer_contact_person_name,
                                                          phone=customer_contact_person_phone,
                                                          email=customer_contact_person_email)
            c = Customer.objects.get(cust_name=customer_name)
            c.cust_contact.add(customer_contact)
            c.save()
            if customer_contact_person_email_1 and customer_contact_person_phone_1 and customer_contact_person_name_1:
                customer_contact_1 = Contact.objects.create(name=customer_contact_person_name_1,
                                                                phone=customer_contact_person_phone_1,
                                                            email=customer_contact_person_email_1)
            cu = Customer.objects.get(cust_name=customer_name)
            cu.cust_contact.add(customer_contact_1)
            cu.save()

    return redirect(view_customer)

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
        return redirect(view_customer)

def view_credit_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    credit = Credit_Notes.objects.filter(master_company=m)
    return render(request, "view_credit_notes.html",{'credit':credit})

def export_credit_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    inv = Credit_Notes.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Credit_Notes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'No.', 'Date','Invoice No.','Invoice Date','Reason','Shipping Charges','Terms & Conditions','Total Amount','Total Discount','Total Tax'])
    for prod in inv:
        writer.writerow([prod.client_name,prod.no,prod.date,prod.invoice_no,prod.invoice_date,prod.reason,prod.shipping_charges,prod.terms_conditions,prod.total_amount,prod.total_discount,prod.total_tax])
    return response


def view_delivery_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    delivery = Delivery_Notes.objects.filter(master_company=m)
    return render(request, "view_delivery_notes.html",{ 'delivery' : delivery})

def export_delivery_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    inv = Delivery_Notes.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Delivery_Notes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'No.', 'Date','PO No.','Shipping Date','Waybill No.','Lr No.','Challan No.','Vehicle No.','Ship By','Transporter Name','Transporter ID','Transporter GSTIN','Terms & Conditions','Total Amount','Total Discount','Total Tax'])
    for prod in inv:
        writer.writerow([prod.client_name,prod.no,prod.date,prod.po_no,prod.shipping_date,prod.waybill_no,prod.lr_no,prod.challan_no,prod.vehicle_no,prod.ship_by,prod.transporter_name,prod.tansporter_id,prod.transporter_gstin,prod.terms_conditions,prod.total_amount,prod.total_discount,prod.total_tax])
    return response


def view_invoices(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    invoice = Invoice.objects.filter(master_company=m)
    return render(request, "view_invoices.html",{'invoice':invoice})

def export_invoice(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    inv = Invoice.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="invoice.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'Invoice No.', 'Invoice Date', 'Payment Terms','PO No.','Due Date','Shipping Charges','Waybill No.','Lr No.','Challan No.','Vehicle No.','Ship By','Transporter Name','Transporter ID','Transporter GSTIN','Terms & Conditions','Total Amount','Total Discount','Total Tax'])
    for prod in inv:
        writer.writerow([prod.client_name,prod.invoice_no,prod.invoice_date,prod.payment_terms,prod.po_no,prod.due_date,prod.shipping_charges,prod.waybill_no,prod.lr_no,prod.challan_no,prod.vehicle_no,prod.ship_by,prod.transporter_name,prod.transporter_id,prod.transporter_gstin,prod.terms_conditions,prod.total_amount,prod.total_discount,prod.total_tax])
    return response


def view_preference(request):
    return render(request, "view_preferences.html")


def view_product(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    ps = Product_Service.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "view_product.html", {'ps':ps,'unit':unit,'userunit':userunit})

def export_product(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    products = Product_Service.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Description', 'Quantity', 'Unit','Tax','HSN','Sales Unit Price','Sales Currency','Sales Cess Percent','Sales Cess','Purchase Unit Price','Purchase Currency','Purchase Cess Percent','Purchase Cess','Type','SAC'])
    for prod in products:
        writer.writerow([prod.name,prod.description,prod.quantity,prod.unit,prod.tax,prod.hsn,prod.sales_unit_price,prod.sales_currency,prod.sales_cess_percent,prod.sales_cess,prod.purchase_unit_price,prod.puchase_currency,prod.purchase_cess_percent,prod.purchase_cess,prod.type,prod.sac])
    return response

def import_product(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader)
        for fields in reader:
            item_name = fields[0]
            item_description = fields[1]
            item_quantity = int(fields[2])
            item_unit = fields[3]
            item_tax = fields[4]
            item_hsn = fields[5]
            item_sales_unit_price = int(fields[6])
            item_sales_currency = fields[7]
            item_sales_cess_percent = fields[8]
            item_sales_cess = fields[9]
            item_purchase_unit_price = fields[10]
            item_purchase_currency = fields[11]
            item_purchase_cess_percent = fields[12]
            item_purchase_cess = fields[13]
            item_type = fields[14]
            item_sac = fields[15]
            prod = Product_Service()
            prod.name = item_name
            prod.description = item_description
            prod.quantity = item_quantity
            prod.unit = item_unit
            prod.tax = item_tax
            prod.hsn = item_hsn
            prod.sales_unit_price = item_sales_unit_price
            prod.sales_currency = item_sales_currency
            prod.sales_cess_percent = item_sales_currency
            prod.purchase_unit_price = item_purchase_unit_price
            prod.puchase_currency = item_purchase_currency
            prod.purchase_cess_percent = item_purchase_cess_percent
            prod.purchase_cess = item_purchase_cess
            prod.type = item_type
            prod.sac = item_sac
            current_user = request.user.email
            x = DBUser.objects.get(email=current_user)
            m = x.master_company
            prod.master_company = m
            prod.save()

    return redirect(view_product)

def view_purchase_order(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    po = Purchase_Order.objects.filter(master_company=m)
    return render(request, "view_purchase_order.html",{'po':po})

def export_purchase_order(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    inv = Purchase_Order.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Purchase_Orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'No.', 'PO Date','Ref No.','Due Date','Shipping Charges','Terms & Conditions','Total Amount','Total Discount','Total Tax'])
    for prod in inv:
        writer.writerow([prod.client_name,prod.no,prod.po_date,prod.ref_no,prod.due_date,prod.shipping_charges,prod.terms_conditions,prod.total_amount,prod.total_discount,prod.total_tax])
    return response

def view_quotes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    q = Quotes.objects.filter(master_company=m)
    return render(request, "view_quotes.html", {'q': q})

def export_quotes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    inv = Quotes.objects.filter(master_company=m)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Quotes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'Quotation No.', 'Quotation Date','PO No.','Due Date','Shipping Charges','Terms & Conditions','Total Amount','Total Discount','Total Tax'])
    for prod in inv:
        writer.writerow([prod.client_name,prod.quotation_no,prod.quotation_date,prod.po_no,prod.due_date,prod.shipping_charges,prod.terms_conditions,prod.total_amount,prod.total_discount,prod.total_tax])
    return response


def view_report(request):
    return render(request, "view_report.html")


def new_invoice(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_invoice.html", {"prod": prod, "client": client, 'tax' : tax, 'unit': unit ,'usertax' : usertax, userunit : 'userunit'})

def new_delivery_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_delivery_notes.html", {"prod": prod, "client": client, 'tax' : tax, 'unit': unit ,'usertax' : usertax, userunit : 'userunit' })

def new_credit_notes(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    invoice = Invoice.objects.filter(master_company=m)
    return render(request, 'new_credit_notes.html', {'prod': prod, 'client': client, 'tax' : tax, 'unit': unit ,'usertax' : usertax,'userunit': userunit  ,'invoice':invoice })

def new_purchase_order(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_purchase_order.html", {"prod": prod, "client": client, 'tax' : tax, 'unit': unit ,'usertax' : usertax, userunit : 'userunit'})

def new_quote(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_quote.html",
                  {"prod": prod, "client": client, 'tax': tax, 'unit': unit, 'usertax': usertax, userunit: 'userunit'})

def new_product(request):
    current_user = request.user.email
    x = DBUser.objects.get(email=current_user)
    m = x.master_company
    prod = Product_Service.objects.filter(master_company=m)
    client = Customer.objects.filter(master_company=m)
    tax = Tax.objects.all()
    usertax = UserTax.objects.filter(master_company=m)
    unit = Unit.objects.all()
    userunit = UserUnit.objects.filter(master_company=m)
    return render(request, "new_product.html", {'tax' : tax, 'unit': unit ,'usertax' : usertax, userunit : 'userunit'})

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
                prod.sales_unit_price = int(product_sales_price)
            else:
                prod.sales_unit_price = 0
            if product_quantity != 'False':
                prod.quantity = int(product_quantity)
            else :
                prod.quantity = 0
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
                prod.puchase_currency = product_purchase_currency
            else:
                prod.puchase_currency = ''
            prod.type = 'Product'
            prod.sac= ''

        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        prod.master_company = m
        prod.save()
        return redirect(view_product)



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
            service.sales_unit_price = int(service_sales_price)
        else:
            service.sales_unit_price = 0
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
            service.puchase_currency = service_purchase_currency
        else:
            service.puchase_currency = ''
        service.type = 'Service'
        service.quantity = 0
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        service.master_company = m
        service.save()
        return redirect(view_product)

def save_invoice(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        invoice_no1 = request.POST['invoiceno1']
        invoice_no2 = request.POST['invoiceno2']
        invoice_no = invoice_no1 + ' ' + invoice_no2
        invoice_date = request.POST['invoicedate']
        payment_terms = request.POST['paymentterms']
        po_no = request.POST['pono']
        due_date = request.POST['duedate']
        total_discount =  request.POST['d']
        total_tax = request.POST['t']
        total_price = request.POST['totalp']
        shipping_price = request.POST['cship']
        waybill_no = request.POST['waybillno']
        challan_no = request.POST['challan']
        vehicle_no = request.POST['vehicle']
        lr_no = request.POST['lr']
        ship_by = request.POST['ship']
        transporter_name = request.POST['t1']
        transporter_id = request.POST['t2']
        transporter_gstin = request.POST['t3']
        notes = request.POST['notes']
        terms = request.POST['terms']
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        invoice = Invoice()
        invoice.client_name = client_name
        invoice.invoice_no = invoice_no
        invoice.invoice_date = invoice_date
        invoice.payment_terms = payment_terms
        invoice.po_no = po_no
        invoice.due_date = due_date
        invoice.total_discount = total_discount
        invoice.total_tax = total_tax
        invoice.total_amount = total_price
        invoice.shipping_charges = shipping_price
        invoice.waybill_no = waybill_no
        invoice.challan_no = challan_no
        invoice.vehicle_no = vehicle_no
        invoice.lr_no = lr_no
        invoice.ship_by = ship_by
        invoice.transporter_name = transporter_name
        invoice.transporter_gstin =transporter_gstin
        invoice.transporter_id = transporter_id
        invoice.private_notes = notes
        invoice.terms_conditions = terms
        invoice.master_company = m
        invoice.save()
        counter = int(request.POST['counter'])
        for x in range(0,counter-1):
            item_name = request.POST['item'+str(x+1)]
            unit = request.POST['unit'+str(x+1)]
            quantity = request.POST['qty'+str(x+1)]
            price = request.POST['price'+str(x+1)]
            discount = request.POST['discount'+str(x+1)]
            tax = request.POST['taxu'+str(x+1)]
            description = request.POST['desc'+str(x+1)]
            print(request.POST['total'+str(x+1)])
            total = request.POST['total'+str(x+1)]
            print x, counter
            d = Dummy_Product.objects.create(name=item_name, unit=unit, quantity=quantity, price=price,
                                             discount=discount, tax=tax, description=description, source='Invoice',item_total=total)
            i = Invoice.objects.get(invoice_no=invoice_no)
            print i
            i.items.add(d)
            i.save()
        return redirect(view_invoices)

def save_delivery_note(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        no1 = request.POST['invoiceno1']
        no2 = request.POST['invoiceno2']
        no = no1 + ' ' + no2
        date = request.POST['invoicedate']
        po_no = request.POST['pono']
        shipping_date = request.POST['duedate']
        total_discount =  request.POST['d']
        total_tax = request.POST['t']
        total_price = request.POST['totalp']
        shipping_price = request.POST['cship']
        waybill_no = request.POST['waybillno']
        challan_no = request.POST['challan']
        vehicle_no = request.POST['vehicle']
        lr_no = request.POST['lr']
        ship_by = request.POST['ship']
        transporter_name = request.POST['t1']
        transporter_id = request.POST['t2']
        transporter_gstin = request.POST['t3']
        notes = request.POST['notes']
        terms = request.POST['terms']
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        delivery = Delivery_Notes()
        delivery.client_name = client_name
        delivery.no = no
        delivery.date = date
        delivery.po_no = po_no
        delivery.shipping_date = shipping_date
        delivery.total_discount = total_discount
        delivery.total_tax = total_tax
        delivery.total_amount = total_price
        delivery.shipping_charges = shipping_price
        delivery.waybill_no = waybill_no
        delivery.challan_no = challan_no
        delivery.vehicle_no = vehicle_no
        delivery.lr_no = lr_no
        delivery.ship_by = ship_by
        delivery.transporter_name = transporter_name
        delivery.transporter_gstin = transporter_gstin
        delivery.tansporter_id = transporter_id
        delivery.private_notes = notes
        delivery.terms_conditions = terms
        delivery.master_company = m
        delivery.save()
        counter = int(request.POST['counter'])
        for x in range(0,counter-1):
            item_name = request.POST['item'+str(x+1)]
            unit = request.POST['unit'+str(x+1)]
            quantity = request.POST['qty'+str(x+1)]
            price = request.POST['price'+str(x+1)]
            discount = request.POST['discount'+str(x+1)]
            tax = request.POST['taxu'+str(x+1)]
            description = request.POST['desc'+str(x+1)]
            print(request.POST['total'+str(x+1)])
            total = request.POST['total'+str(x+1)]
            print x, counter
            d = Dummy_Product.objects.create(name=item_name, unit=unit, quantity=quantity, price=price,
                                             discount=discount, tax=tax, description=description, source='Delivery Notes',item_total=total)
            i = Delivery_Notes.objects.get(no=no)
            i.items.add(d)
            i.save()
        return redirect(view_delivery_notes)

def save_credit_note(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        no1 = request.POST['invoiceno1']
        no2 = request.POST['invoiceno2']
        no = no1 + ' ' + no2
        date = request.POST['invoicedate']
        invoice_no = request.POST['pono']
        invoice_date = request.POST['duedate']
        reason = request.POST['reason']
        total_discount =  request.POST['d']
        total_tax = request.POST['t']
        total_price = request.POST['totalp']
        shipping_price = request.POST['cship']
        notes = request.POST['notes']
        terms = request.POST['terms']
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        credit = Credit_Notes()
        credit.client_name = client_name
        credit.no = no
        credit.date = date
        credit.invoice_no = invoice_no
        credit.invoice_date = invoice_date
        credit.total_discount = total_discount
        credit.total_tax = total_tax
        credit.total_amount = total_price
        credit.shipping_charges = shipping_price
        credit.private_notes = notes
        credit.terms_conditions = terms
        credit.master_company = m
        credit.reason = reason
        credit.save()
        counter = int(request.POST['counter'])
        for x in range(0,counter-1):
            item_name = request.POST['item'+str(x+1)]
            unit = request.POST['unit'+str(x+1)]
            quantity = request.POST['qty'+str(x+1)]
            price = request.POST['price'+str(x+1)]
            discount = request.POST['discount'+str(x+1)]
            tax = request.POST['taxu'+str(x+1)]
            description = request.POST['desc'+str(x+1)]
            print(request.POST['total'+str(x+1)])
            total = request.POST['total'+str(x+1)]
            print x, counter
            d = Dummy_Product.objects.create(name=item_name, unit=unit, quantity=quantity, price=price,
                                             discount=discount, tax=tax, description=description, source='Credit Notes',item_total=total)
            i = Credit_Notes.objects.get(no=no)
            i.items.add(d)
            i.save()
        return redirect(view_credit_notes)

def save_purchase_order(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        no1 = request.POST['invoiceno1']
        no2 = request.POST['invoiceno2']
        no = no1 + ' ' + no2
        po_date = request.POST['invoicedate']
        ref_no = request.POST['refnumber']
        due_date = request.POST['duedate']
        total_discount =  request.POST['d']
        total_tax = request.POST['t']
        total_price = request.POST['totalp']
        shipping_price = request.POST['cship']
        notes = request.POST['notes']
        terms = request.POST['terms']
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        purchase = Purchase_Order()
        purchase.client_name = client_name
        purchase.no = no
        purchase.po_date = po_date
        purchase.ref_no = ref_no
        purchase.due_date = due_date
        purchase.total_discount = total_discount
        purchase.total_tax = total_tax
        purchase.total_amount = total_price
        purchase.shipping_charges = shipping_price
        purchase.private_notes = notes
        purchase.terms_conditions = terms
        purchase.master_company = m
        purchase.save()
        counter = int(request.POST['counter'])
        for x in range(0,counter-1):
            item_name = request.POST['item'+str(x+1)]
            unit = request.POST['unit'+str(x+1)]
            quantity = request.POST['qty'+str(x+1)]
            price = request.POST['price'+str(x+1)]
            discount = request.POST['discount'+str(x+1)]
            tax = request.POST['taxu'+str(x+1)]
            description = request.POST['desc'+str(x+1)]
            print(request.POST['total'+str(x+1)])
            total = request.POST['total'+str(x+1)]
            print x, counter
            d = Dummy_Product.objects.create(name=item_name, unit=unit, quantity=quantity, price=price,
                                             discount=discount, tax=tax, description=description, source='Purchase Order',item_total=total)
            i = Purchase_Order.objects.get(no=no)
            i.items.add(d)
            i.save()
        return redirect(view_purchase_order)

def save_quote(request):
    if request.method == 'POST':
        client_name = request.POST['clientname']
        no1 = request.POST['invoiceno1']
        no2 = request.POST['invoiceno2']
        no = no1 + ' ' + no2
        quote_date = request.POST['invoicedate']
        po_no = request.POST['pono']
        due_date = request.POST['duedate']
        total_discount =  request.POST['d']
        total_tax = request.POST['t']
        total_price = request.POST['totalp']
        shipping_price = request.POST['cship']
        notes = request.POST['notes']
        terms = request.POST['terms']
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        quote = Quotes()
        quote.client_name = client_name
        quote.quotation_no = no
        quote.quotation_date = quote_date
        quote.po_no = po_no
        quote.due_date = due_date
        quote.total_discount = total_discount
        quote.total_tax = total_tax
        quote.total_amount = total_price
        quote.shipping_charges = shipping_price
        quote.private_notes = notes
        quote.terms_conditions = terms
        quote.master_company = m
        quote.save()
        counter = int(request.POST['counter'])
        for x in range(0,counter-1):
            item_name = request.POST['item'+str(x+1)]
            unit = request.POST['unit'+str(x+1)]
            quantity = request.POST['qty'+str(x+1)]
            price = request.POST['price'+str(x+1)]
            discount = request.POST['discount'+str(x+1)]
            tax = request.POST['taxu'+str(x+1)]
            description = request.POST['desc'+str(x+1)]
            print(request.POST['total'+str(x+1)])
            total = request.POST['total'+str(x+1)]
            print x, counter
            d = Dummy_Product.objects.create(name=item_name, unit=unit, quantity=quantity, price=price,
                                             discount=discount, tax=tax, description=description, source='Quotes',item_total=total)
            i = Quotes.objects.get(quotation_no=no)
            i.items.add(d)
            i.save()
        return redirect(view_quotes)

def filterclient(request):
    if request.method == 'POST':
        company = request.POST.get('cpname', "")
        email = request.POST.get('cemail', "")
        phone = request.POST.get('cphone', "")
        city = request.POST.get('ccity', "")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Customer.objects.filter(master_company=m"
        if company != "":
            temp = temp + ", cust_name=company"
        if email != "":
            temp = temp + ", cust_email=email"
        if phone != "":
            temp = temp + ", cust_phone=phone"
        if city != "":
            temp = temp + ", cust_city=city"
        temp = temp + ")"
        customers = eval(temp)
        return render(request, "view_customer.html", {'customers': customers})

def filteritem(request):
    if request.method == 'POST':
        name = request.POST.get('name', "")
        unit = request.POST.get('unit', "")
        price1 = request.POST.get('price1', "")
        if price1:
            price1 = int(price1)
        price2 = request.POST.get('price2', "")
        if price2:
            price2 = int(price2)
        quant1 = request.POST.get('quant1', "")
        if quant1:
            quant1 = int(quant1)
        quant2 = request.POST.get('quant2', "")
        if quant2:
            quant2 = int(quant2)
        type = request.POST.get('type',"")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Product_Service.objects.filter(master_company=m"
        if name != "":
            temp = temp + ", name = name"
        if unit != "":
            temp = temp + ", unit = unit"
        if price1 != "" and price2 != "":
            temp = temp + " , sales_unit_price__gte = price1 , sales_unit_price__lte = price2"
        else:
            if price1 != "":
                temp = temp + ", sales_unit_price__gte = price1"
            if price2 != "":
                temp = temp + ", sales_unit_price__lte = price2"
        if quant1 != "" and quant2 != "":
            temp = temp + " , quantity__gte = quant1 , quantity__lte = quant2"
        else:
            if quant1 != "":
                temp = temp + " , quantity__gte = quant1"
            if quant2 != "":
                temp = temp + " , quantity__lte = quant2"
        if type != "":
            temp = temp + " , type = type"
        temp = temp + ")"
        ps = eval(temp)
        return render(request,'view_product.html',{'ps':ps})


def filterinvoice(request):
    if request.method == 'POST':
        client_name = request.POST.get('name', "")
        invoice_no = request.POST.get('invoiceno', "")
        issue_date1 = request.POST.get('issue1', "")
        issue_date2 = request.POST.get('issue2', "")
        due_date1 = request.POST.get('due1', "")
        due_date2 = request.POST.get('due2', "")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Invoice.objects.filter(master_company=m"
        if client_name != "":
            temp = temp + ", client_name = client_name"
        if invoice_no != "":
            temp = temp + ", invoice_no = invoice_no"
        if issue_date1 != "" and issue_date2 != "":
            temp = temp + ", invoice_date__gte = issue_date1 , invoice_date__lte = issue_date2"
        else:
            if issue_date1 != "":
                temp = temp + ", invoice_date__gte = issue_date1"
            if issue_date2 != "":
                temp = temp + ", invoice_date__lte = issue_date2"
        if due_date1 != "" and due_date2 != "":
            temp = temp + ", due_date__gte = due_date1 , due_date__lte = due_date2"
        else:
            if due_date1 != "":
                temp = temp + ", due_date__gte = due_date1"
            if due_date2 != "":
                temp = temp + ", due_date__lte = due_date2"

        temp = temp + ")"
        invoice = eval(temp)
        return render(request, "view_invoices.html", {'invoice': invoice})

def filterquote(request):
    if request.method == 'POST':
        client_name = request.POST.get('name', "")
        invoice_no = request.POST.get('invoiceno', "")
        issue_date1 = request.POST.get('issue1', "")
        issue_date2 = request.POST.get('issue2', "")
        due_date1 = request.POST.get('due1', "")
        due_date2 = request.POST.get('due2', "")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Quotes.objects.filter(master_company=m"
        if client_name != "":
            temp = temp + ", client_name = client_name"
        if invoice_no != "":
            temp = temp + ", quotation_no = invoice_no"
        if issue_date1 != "" and issue_date2 != "":
            temp = temp + ", quotation_date__gte = issue_date1 , quotation_date__lte = issue_date2"
        else:
            if issue_date1 != "":
                temp = temp + ", quotation_date__gte = issue_date1"
            if issue_date2 != "":
                temp = temp + ", quotation_date__lte = issue_date2"
        if due_date1 != "" and due_date2 != "":
            temp = temp + ", due_date__gte = due_date1 , due_date__lte = due_date2"
        else:
            if due_date1 != "":
                temp = temp + ", due_date__gte = due_date1"
            if due_date2 != "":
                temp = temp + ", due_date__lte = due_date2"
        temp = temp + ")"
        q = eval(temp)
        return render(request, "view_quotes.html", {'q': q})

def filterdeliverynotes(request):
    if request.method == 'POST':
        client_name = request.POST.get('name', "")
        invoice_no = request.POST.get('invoiceno', "")
        issue_date1 = request.POST.get('issue1', "")
        issue_date2 = request.POST.get('issue2', "")
        due_date1 = request.POST.get('due1', "")
        due_date2 = request.POST.get('due2', "")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Delivery_Notes.objects.filter(master_company=m"
        if client_name != "":
            temp = temp + ", client_name = client_name"
        if invoice_no != "":
            temp = temp + ", no = invoice_no"
        if issue_date1 != "" and issue_date2 != "":
            temp = temp + ", date__gte = issue_date1 , date__lte = issue_date2"
        else:
            if issue_date1 != "":
                temp = temp + ", date__gte = issue_date1"
            if issue_date2 != "":
                temp = temp + ", date__lte = issue_date2"
        if due_date1 != "" and due_date2 != "":
            temp = temp + ", shipping_date__gte = due_date1 , shipping_date__lte = due_date2"
        else:
            if due_date1 != "":
                temp = temp + ", shipping_date__gte = due_date1"
            if due_date2 != "":
                temp = temp + ", shipping_date__lte = due_date2"
        temp = temp + ")"
        delivery = eval(temp)
        return render(request, "view_delivery_notes.html", {'delivery': delivery})

def filtercreditnotes(request):
    if request.method == 'POST':
        client_name = request.POST.get('name', "")
        invoice_no = request.POST.get('invoiceno', "")
        issue_date1 = request.POST.get('issue1', "")
        issue_date2 = request.POST.get('issue2', "")
        amount1 = request.POST.get('due1', "")
        if amount1:
            amount1 = int(amount1)
        amount2 = request.POST.get('due2', "")
        if amount2:
            amount2 = int(amount2)
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Credit_Notes.objects.filter(master_company=m"
        if client_name != "":
            temp = temp + ", client_name = client_name"
        if invoice_no != "":
            temp = temp + ", no = invoice_no"
        if issue_date1 != "" and issue_date2 != "":
            temp = temp + ", date__gte = issue_date1 , date__lte = issue_date2"
        else:
            if issue_date1 != "":
                temp = temp + ", date__gte = issue_date1"
            if issue_date2 != "":
                temp = temp + ", date__lte = issue_date2"
        if amount1 != "" and amount2 != "":
            temp = temp + ", total_amount__gte = amount1 , total_amount__lte = amount2"
        else:
            if amount1 != "":
                temp = temp + ", total_amount__gte = amount1"
            if amount2 != "":
                temp = temp + ", total_amount__lte = amount2"

        temp = temp + ")"
        print temp
        credit = eval(temp)
        return render(request, "view_credit_notes.html", {'credit': credit})

def filterpurchaseorder(request):
    if request.method == 'POST':
        client_name = request.POST.get('name', "")
        invoice_no = request.POST.get('invoiceno', "")
        issue_date1 = request.POST.get('issue1', "")
        issue_date2 = request.POST.get('issue2', "")
        due_date1 = request.POST.get('due1', "")
        due_date2 = request.POST.get('due2', "")
        current_user = request.user.email
        x = DBUser.objects.get(email=current_user)
        m = x.master_company
        temp = "Purchase_Order.objects.filter(master_company=m"
        if client_name != "":
            temp = temp + ", client_name = client_name"
        if invoice_no != "":
            temp = temp + ", no = invoice_no"
        if issue_date1 != "" and issue_date2 != "":
            temp = temp + ", po_date__gte = issue_date1 , po_date__lte = issue_date2"
        else:
            if issue_date1 != "":
                temp = temp + ", po_date__gte = issue_date1"
            if issue_date2 != "":
                temp = temp + ", po_date__lte = issue_date2"
        if due_date1 != "" and due_date2 != "":
            temp = temp + ", due_date__gte = due_date1 , due_date__lte = due_date2"
        else:
            if due_date1 != "":
                temp = temp + ", due_date__gte = due_date1"
            if due_date2 != "":
                temp = temp + ", due_date__lte = due_date2"
        temp = temp + ")"
        po = eval(temp)
        return render(request, "view_purchase_order.html", {'po': po})
