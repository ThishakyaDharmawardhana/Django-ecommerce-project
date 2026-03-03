import datetime
from django.shortcuts import render,redirect
from .models import Product, Category, CartItem, Order,OrderProduct
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404






# Create your views here.

def aboutus(request):
    return render(request, 'store/aboutus.html', {'title':'About Us'})

def storehome(request):
    return render(request, 'store/storehome.html', {'title':'Welcome to Phone Company'})

def reviews(request):
    return render(request, 'store/reviews.html', {'title':'reviews'})

#def shop(request):
    #products = Product.objects.all()
    #return render(request, 'store/shop.html', {'title':'shop','products':products})

def sitehome(request):
    return render(request, 'store/sitehome.html', {})

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product.html', {'product' : product, 'title': product.name })

def shop(request, category = None):
    if category:
        category = Category.objects.get(name=category)
        products = Product.objects.filter(category=category)
        return render(request, 'store/shop.html', {'products': products, 'title': category})
    else:
        products = Product.objects.all()
        return render(request, 'store/shop.html', {'products': products, 'title': 'All Phones' })


@login_required(login_url='login_user') 
def add_to_cart(request, product_id):
    if request.user :
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('shop')


@login_required(login_url='login_user')
def view_cart(request):
    if request.user.is_anonymous:
        pass
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.sale_price * item.quantity for item in cart_items)
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'title': 'Shopping Cart'})


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


@transaction.atomic
def create_order(request, orderid=None):
    if request.user.is_authenticated:
        try:        
            # If no orderid, create a new order
            new_order = Order.objects.create(customer=request.user, date=datetime.now().date())
            new_order.save()
           
            print("order craeted")


            cart_items_purchase = CartItem.objects.filter(user=request.user, purchase=True)
            if cart_items_purchase:
                for item in cart_items_purchase:
                    product = Product.objects.get(id=item.product_id)
                    soldprice = product.sale_price
                    orderproduct = OrderProduct.objects.create(product=item.product, order=new_order)
                    orderproduct.quantity = item.quantity
                    orderproduct.soldprice = soldprice
                    orderproduct.save()
                    item.delete()


            print ("order products created")


            order_items = OrderProduct.objects.filter(order_id=new_order.id)
            total_price = sum(item.soldprice * item.quantity for item in order_items)
            new_order.total = total_price
            new_order.status = "Unpaid"
            new_order.save()




            return redirect('order_details', order_id=new_order.id)




        except Exception as e:
            print("Error creating order occurred:", e)
            return redirect('view_cart')





@login_required(login_url='login_user')
def order_details(request, order_id):#Call this view after creating an order
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        order_products = order.orderproduct_set.select_related('product')
        total_price = sum(op.soldprice * op.quantity for op in order.orderproduct_set.all())


        return render(request, 'store/order_details.html', {
            'order': order,
            'order_products': order_products,
            'title': "Order Details",
            'total_price': total_price,
        })
    else:
        messages.error(request, "The order not found.")
        return redirect('welcome')




@login_required
def update_purchase(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        item_id = request.POST.get('id')
        purchase_value = request.POST.get('purchase') == 'true'  # Convert to boolean

        try:
            item = CartItem.objects.get(id=item_id)
            item.purchase = purchase_value  # Update the purchase field
            item.save()

            # Recalculate the total price for selected items only
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.sale_price * item.quantity for item in cart_items if item.purchase)

            # Make sure total_price is a number
            total_price = round(total_price, 2)

            # Return calculated total price
            return JsonResponse({'total_price': total_price})
        
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

