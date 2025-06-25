from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from store.models import Cart, Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
import weasyprint
import os
from django.conf import settings
from django.shortcuts import get_object_or_404



def index(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, "store/orders/index.html", context)


def vieworder(request, t_no):
    order = Order.objects.get(tracking_no=t_no, user=request.user)
    orderitems = OrderItem.objects.filter(order=order)
    context = {'order': order, 'orderitems': orderitems}
    return render(request, "store/orders/view.html", context)



def download_invoice(request, t_no):
    order = get_object_or_404(Order, tracking_no=t_no, user=request.user)
    html = render_to_string('store/invoice.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{order.tracking_no}.pdf"'

    weasyprint.HTML(string=html).write_pdf(response)
    return response
