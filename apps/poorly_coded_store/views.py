from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum
from .models import Order, Product

def index(request):
    if request.method == "GET":
        context = {
            "all_products": Product.objects.all()
        }
        return render(request, "store/index.html", context)
    else:
        quantity_from_form = int(request.POST["quantity"])
        product = Product.objects.values('price').get(id=request.POST['pid'])
        total_charge = quantity_from_form * product['price']

        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        request.session['total_charge'] = str(total_charge)

        print("Charging credit card...")    
        return redirect('/checkout')

def checkout(request):
    if request.method == "POST":
        return HttpResponse("You cannot post data to this route. Please try again.")

    context = {
        'sum_prices': Order.objects.all().aggregate(Sum('total_price')),
        'sum_quantities': Order.objects.all().aggregate(Sum('quantity_ordered'))
    }
    return render(request, 'store/checkout.html', context)