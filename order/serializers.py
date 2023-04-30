from rest_framework import serializers
from .models import Cart, CartProduct, Track


class AddToCartSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
        ),
        write_only=True
    )

    class Meta:
        model = CartProduct
        fields = ['id', 'products']


class DeleteFromCartSerializer(serializers.ModelSerializer):
    products = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = CartProduct
        fields = ['id', 'products']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["track", "created_at"]


class TrackListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', format='%Y-%m-%d')
    time = serializers.DateTimeField(source='created_at', format='%H:%M:%S')

    class Meta:
        model = Track
        fields = ["track", "date", "time"]


class TrackGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['product', 'count']