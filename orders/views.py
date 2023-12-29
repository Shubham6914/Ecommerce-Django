from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from carts.models import CartItem
from .forms import OrderForm
from.models import Payment,Order,OrderProduct
import datetime
from django.http import HttpResponse,JsonResponse
import json
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.
def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get( user=request.user, order_number=body['orderID'])
        
        # store transaction details inside payment model
    payment = Payment(
            user=request.user,
            payment_id=body['transID'],
            payment_method=body['payment_method'],
            ammount_paid=body['amount'],
            status=body['status'],
        )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    # Move the cart item to order product table 
    cart_items = CartItem.objects.filter(user = request.user)
    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment_id = payment.id
        orderproduct.user_id  = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        
        # reduce the quantity of sold products 
        
        product = Product.objects.get(id = item.product_id)
        product.stock -= item.quantity
        product.save()
        
    # clear the cart after successfull order
    CartItem.objects.filter(user=request.user).delete()
        
    # Send order received email to customer 
    mail_subject = 'Thankyou for your Order'
    message = render_to_string('orders/order_received_email.html',{
            'user': request.user,
            'order' : order,
            'product':product,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()
    
    # send order number and transaction ID to sendData method by JSonResponse
    data = {
        'order_number':order.order_number,
        'transID' : payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    current_user = request.user
    # If the cart count is less than or equal to 0, redirect back to the store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Store all the billing information inside the billing table
            data = form.save(commit=False)
            data.user = current_user
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr, mt, dt = map(int, datetime.date.today().strftime('%Y %m %d').split())
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%y%m%d")

            # Concatenate current date and user id to generate order number
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payment.html', context)
        else:
            print(form.errors)
            return HttpResponse("Form is not valid. Handle the error as needed.")
    else:
        return redirect('checkout')

def order_complete(request):
    
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        subtotal =0 
        for i in ordered_products:
            subtotal += (i.product_price * i.quantity)
        
        payment = Payment.objects.get(payment_id=transID)
        
        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'subtotal':subtotal,
            
        }
        return render(request, 'orders/order_complete.html',context)
    
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
        