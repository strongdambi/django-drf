from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    # path("", views.ProductListAPIView.as_view(), name="product_list"),
    path("", views.product_list),
]