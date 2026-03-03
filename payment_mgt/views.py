import logging
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from store.models import Order
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


# Exempt CSRF for this view only since it's dealing with Stripe Checkout
from django.shortcuts import redirect


@csrf_exempt
def create_checkout_session(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id, customer=request.user)


            total_price = sum(
                item.product.sale_price * item.quantity
                for item in order.orderproduct_set.all()
            )


            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your Order',
                            },
                            'unit_amount': int(total_price * 100),  # Stripe accepts amounts in cents
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'user_id': request.user.id,
                    'order_id': order_id,
                },
                mode='payment',
                 success_url='https://gaiterless-nataly-subapparent.ngrok-free.dev/payment_mgt/payment_success/',
                 cancel_url='https://gaiterless-nataly-subapparent.ngrok-free.dev/payment_mgt/payment_cancel/',
            )


            # Redirect to Stripe Checkout session URL
            return redirect(session.url)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating checkout session: {e}")
            return JsonResponse({'error': str(e)}, status=500)



# Payment success view without csrf exemption
def payment_success(request):
    return render(request, 'payment_mgt/pay_success.html', {'message': 'Payment Success!'})




# Payment decline view without csrf exemption
def payment_decline(request):
    return render(request, 'payment_mgt/pay_decline.html', {'Title': 'Payment Decline!'})

