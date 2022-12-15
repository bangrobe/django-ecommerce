from django.urls import path
from . import views
urlpatterns = [
    path('', views.shop, name='shoppage'),
    path('<str:category_slug>/', views.shop, name='shop-by-category'),
    path('<str:category_slug>/<str:product_slug>/', views.product_detail, name='product-detail'),
]