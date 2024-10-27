from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('groups/manager/users', views.manager_list),
    path('groups/manager/users/<int:pk>', views.manager_list_remove),
    path('groups/delivery-crew/users', views.deliverycrew_list),
    path('groups/delivery-crew/users/<int:pk>', views.deliverycrew_list_remove),
    path('menu-items/',views.MenuItem.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItem.as_view()),
    path('catagories',views.Catagory.as_view()),
    path('cart/menu-items',views.cart),
    path('orders',views.Orders),
    path('orders/<int:pk>',views.SingleOrder),
    
]