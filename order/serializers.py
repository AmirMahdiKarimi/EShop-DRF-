from rest_framework import serializers
from .models import Cart, CartProduct, Track, Product
from rest_framework.utils import html
from collections.abc import Mapping
from collections import OrderedDict
from rest_framework.exceptions import ValidationError


# class AddToCartSerializer(serializers.ModelSerializer):
#     products = serializers.ListField(
#         child=serializers.DictField(
#             child=serializers.IntegerField(),
#         ),
#         write_only=True
#     )

#     class Meta:
#         model = CartProduct
#         fields = ['id', 'products']

class AddToCartProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
    
    def validate(self, attrs):
        try:
            product = Product.objects.get(id=attrs['id'])
            if product.remaining_count == 0:
                respons={"id": attrs['id'], "success": False, "message": "product unavailable!"}
            elif product.remaining_count < attrs['count']:
                respons={"id": attrs['id'], "success": False, "message": "product remaining is not enough!"}
            elif attrs['count'] < 1:
                respons={"id": attrs['id'], "success": False, "message": "product count should be positive!"}
            else:
                respons={'id': attrs['id'], 'count': attrs['count'], "success": True}
        except Product.DoesNotExist:
            respons={"id": attrs['id'], "success": False, "message": "product not founded!"}
        return respons

class AddToCartSerializer(serializers.Serializer):
    products = AddToCartProductSerializer(many=True)

    def create(self, validated_data):
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user, open=True)
        message = []
        for item in validated_data['products']:
            if item["success"] == False:
                message.append(item)
            else:
                product = Product.objects.get(id=item['id'])
                cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
                cart_product.count += item['count']
                product.remaining_count -= item['count']
                cart_product.save()
                product.save()
                message.append({"id": item['id'], "success": True, "message": "product added."})

        return message


# class DeleteFromCartSerializer(serializers.ModelSerializer):
#     products = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True
#     )

#     class Meta:
#         model = CartProduct
#         fields = ['id', 'products']


class IdListField(serializers.ListField):
    def to_internal_value(self, data):
        if html.is_html_input(data):
            data = html.parse_html_list(data, default=[])
        if (isinstance(data, (str, Mapping)) or not hasattr(data, '__iter__')) and data != "all":
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')
        return self.run_child_validation(data)
    
    def run_child_validation(self, data):
        result = []
        errors = OrderedDict()
        if data == "all":
            return data
        for idx, item in enumerate(data):
            try:
                result.append(self.child.run_validation(item))
            except ValidationError as e:
                errors[idx] = e.detail

        if not errors:
            return result
        raise ValidationError(errors)

    def to_representation(self, value):
        if value == 'all':
            return [value]
        else:
            return [self.child.to_representation(item) if item is not None else None for item in value]
        
class DeleteFromCartSerializer(serializers.ModelSerializer):
    products = IdListField(
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