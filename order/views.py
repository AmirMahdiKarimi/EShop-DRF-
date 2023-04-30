from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse

from .serializers import AddToCartSerializer, DeleteFromCartSerializer, ShopSerializer, TrackListSerializer, TrackGetSerializer
from .models import Cart, CartProduct, Track, Product


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return JsonResponse({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'results': data
        })
    

class AddToCartAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user, open=True)
        products = self.request.data.get('products')
        message = []
        for add_product in products:
            try:
                product = Product.objects.get(id=add_product['id'])
                if product.remaining_count == 0:
                    message.append({"id": add_product['id'], "success": False, "message": "product unavailable!"})
                elif product.remaining_count < add_product['count']:
                    message.append({"id": add_product['id'], "success": False, "message": "product remaining is not enough!"})
                else: 
                    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
                    cart_product.count += add_product['count']
                    product.remaining_count -= add_product['count']
                    cart_product.save()
                    product.save()
                    message.append({"id": add_product['id'], "success": True, "message": "product added."})
            except:
                message.append({"id": add_product['id'], "success": False, "message": "product not founded!"})
        return message
            
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": message}, status=201)

    
class DeleteFromCartAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteFromCartSerializer
    
    def destroy(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, open=True)
        products = request.data.get('products')
        if products[0] == "all":
            cart_products = CartProduct.objects.filter(cart=cart)
            cart_products.delete()
            return Response({"message": "All products removed."}, status=202)
        removed = []
        for remove_product in products:
            try:
                product = Product.objects.get(id=remove_product)
                try:
                    cart_product = CartProduct.objects.get(cart=cart, product=product)
                    product.remaining_count += cart_product.count
                    self.perform_destroy(cart_product)
                    product.save()
                    removed.append({"id": remove_product, "success": True, "message": "product removed."})
                except:
                    removed.append({"id": remove_product, "success": False, "message": "product was not in cart."})
            except:
                removed.append({"id": remove_product, "success": False, "message": "product not founded!"})
        return Response({"message": removed}, status=202)
    

class ShopAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSerializer
    
    def get_object(self):
        try:
            cart = Cart.objects.get(user=self.request.user, open=True)
            track, created = Track.objects.get_or_create(cart=cart)
            cart.open = False
            cart.save()
            return track
        except:
            return False

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            data = serializer.data
            return Response(data)
        return Response({"message": "You don't have open cart or already bought this cart."})
        

class TrackListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackListSerializer

    def get_queryset(self):
        return Track.objects.filter(cart__user=self.request.user)
    

class TrackGetAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TrackGetSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        track_id = self.kwargs.get('track_id')
        track = get_object_or_404(Track, track=track_id, cart__user=self.request.user)
        response = CartProduct.objects.filter(cart=track.cart)
        return response
    