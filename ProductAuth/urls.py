from django.urls import path
from .views import ProductListCreateView,ProductPostRetrieveUpdateDeleteView,CategoriesListCreateView, CategoryPostRetrieveUpdateDeleteView,BrandListCreateView,BrandPostRetrieveUpdateDeleteView

urlpatterns = [
    path('product/', ProductListCreateView.as_view()),
    path('product/<int:pk>/', ProductPostRetrieveUpdateDeleteView.as_view()),
    path('category/', CategoriesListCreateView.as_view()),
    path('category/<int:pk>/', CategoryPostRetrieveUpdateDeleteView.as_view()),
    path('brand/', BrandListCreateView.as_view()),
    path('brand/<int:pk>/', BrandPostRetrieveUpdateDeleteView.as_view()),
]