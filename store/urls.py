from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
path('aboutus',views.aboutus, name='aboutus'),   
path('storehome',views.storehome, name='storehome'),   
path('reviews',views.reviews, name='reviews'),  
path('sitehome',views.sitehome, name='sitehome'),   
path('shop',views.shop, name='shop'),
path('shop/<str:category>/', views.shop, name='shop'),
path('product/<int:product_id>/',views.product, name='product'),
path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('view_cart/', views.view_cart, name='view_cart'),
path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
path('create_order/', views.create_order, name='create_order'),
path('order_details/<int:order_id>', views.order_details, name='order_details'),
path('view_cart/update-purchase/', views.update_purchase, name='update_purchase'),













  



]
urlpatterns += staticfiles_urlpatterns()


