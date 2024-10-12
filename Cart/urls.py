from django.urls import path
from .views import CartView,CartItemView,CartUpdateDeleteView

urlpatterns=[
    path('cart/', CartView.as_view(), name='cart'),
    path('cartitem/', CartItemView.as_view(), name='cartitem'),
    path('cart/<int:pk>/', CartUpdateDeleteView.as_view(), name='cartdelete'),
]