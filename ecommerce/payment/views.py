from django.shortcuts import render

# Create your views here.


def payment_succes(request):

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')