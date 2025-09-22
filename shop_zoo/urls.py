from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_zoo, name='shop_zoo'),
    path('<int:product_id>/', views.single_product, name='single_product'),
    path('register/', views.register, name='register'),
    path('shop_zoo/', views.shop_zoo, name='shop_zoo'),
]
