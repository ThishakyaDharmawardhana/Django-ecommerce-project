from django.urls import path
from . import views


urlpatterns = [
    path('create-checkout-session/<int:order_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_decline/', views.payment_decline, name='payment_decline'),


    
]
