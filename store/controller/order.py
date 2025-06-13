from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from store.models import Cart, Product, Order, OrderItem
from django.contrib.auth.decorators import login_required


def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, "store/orders/index.html", context)


def vieworder(request, t_no):
    order = Order.objects.get(tracking_no=t_no, user=request.user)
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order': order, 'orderitems': orderitems}
    return render(request, "store/orders/view.html", context)
