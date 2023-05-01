from rest_framework import serializers
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Product, Opinion, Score


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'desc', 'price', 'remaining_count', 'type', 'brand')


    def validate(self, data):
        if data['price'] < 0: 
            raise serializers.ValidationError("Price should be greater than zero.")
        if data['remaining_count'] < 0:
            raise serializers.ValidationError("Remaining count should be positive.")
        return data


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'desc', 'price', 'remaining_count', 'type', 'brand', 'created_at', 'last_update')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'desc', 'price', 'remaining_count', 'type', 'brand', 'created_at', 'last_update')


class AddOpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ('text',)


class OpinionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ('user', 'text', 'created_at')


class AddScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('score',)

    def validate(self, data):
        user = self.context['request'].user
        product = self.context['product']
        if Score.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError('You have already scored this product.')
        
        return data
    

class ScoreSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('score',)

    def get_score(self, obj):
        return round(obj.score_avg)