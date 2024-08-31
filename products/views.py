from django.core.cache import cache
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
# class ProductListAPIView(APIView):
#     def get(self, request):
#         cache_key = "product_list"

#         if not cache.get(cache_key):
#             print("cache miss")
#             products = Product.objects.all()
#             serializer = ProductSerializer(products, many=True)
#             json_response = serializer.data
#             cache.set("cache_key", json_response, 5)
        
#         response_data = cache.get(cache_key)
#         return Response(response_data)
    
@api_view(["GET"])
def product_list(request):
    cache_key = "product_list"

    if not cache.get(cache_key):
        print("cache miss")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_data = serializer.data
        cache.set(cache_key, json_data, 180)

    response_data = cache.get(cache_key)
    return Response(response_data)