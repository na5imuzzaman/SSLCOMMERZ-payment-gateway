from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from .tran_id import id_generator
from .models import Transaction_Data
from . import credential


def index_view(request):
    return render(request, "index.html", {})


def checkout_view(request):
    if request.method == "GET":
        amount = request.GET.get('amount')
        if amount != None:
            print(amount)

            settings = {'store_id': credential.store_id,
                        'store_pass': credential.store_pass, 'issandbox': True}
            sslcommez = SSLCOMMERZ(settings)
            post_body = {}
            post_body['total_amount'] = amount
            post_body['currency'] = "BDT"
            post_body['tran_id'] = id_generator()
            post_body['success_url'] = credential.GATEWAY + "success/"
            post_body['fail_url'] = credential.GATEWAY + "failed/"
            post_body['cancel_url'] = credential.GATEWAY + "cancle/"
            post_body['emi_option'] = 0
            post_body['cus_name'] = "Nasim"
            post_body['cus_email'] = "xyz.jgc@gmail.com"
            post_body['cus_phone'] = "017961533690"
            post_body['cus_add1'] = "Dhaka"
            post_body['cus_city'] = "Dhaka"
            post_body['cus_country'] = "Bangladesh"
            post_body['shipping_method'] = "NO"
            post_body['multi_card_name'] = ""
            post_body['num_of_item'] = 1
            post_body['product_name'] = "Test"
            post_body['product_category'] = "Test Category"
            post_body['product_profile'] = "general"

            response = sslcommez.createSession(post_body)
            return redirect('https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"])

        return render(request, "checkout.html", {})


@csrf_exempt
def success_view(request):
    if request.POST:
        data = request.POST
        obj = Transaction_Data.objects.create(
            tran_id=data['tran_id'],
            val_id=data['val_id'],
            amount=data['amount'],
            card_type=data['card_type'],
            card_no=data['card_no'],
            store_amount=data['store_amount'],
            bank_tran_id=data['bank_tran_id'],
            status=data['status'],
            tran_date=data['tran_date'],
            currency=data['currency'],
            card_issuer=data['card_issuer'],
            card_brand=data['card_brand'],
            card_issuer_country=data['card_issuer_country'],
            card_issuer_country_code=data['card_issuer_country_code'],
            verify_sign=data['verify_sign'],
            verify_sign_sha2=data['verify_sign_sha2'],
            currency_rate=data['currency_rate'],
            risk_title=data['risk_title'],
            risk_level=data['risk_level'],
        )
    return render(request, "success.html", {})


@csrf_exempt
def failed_view(request):
    if request.POST:
        print(request.POST)
    return render(request, "failed.html", {})


@csrf_exempt
def cancle_view(request):
    if request.POST:
        print(request.POST)
    return render(request, "cancle.html", {})
