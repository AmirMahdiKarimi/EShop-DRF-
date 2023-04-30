from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import AddProductSerializer, ProductListSerializer, ProductSerializer, AddOpinionSerializer, \
    OpinionListSerializer, AddScoreSerializer, ScoreSerializer
from .models import Product, Opinion, Score

class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    
    def get_queryset(self):
        type = self.request.query_params.get('type')
        name = self.request.query_params.get('name')
        brand = self.request.query_params.get('brand')        
        queryset = Product.objects.all()
        if type:
            queryset = queryset.filter(type=type)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        return queryset        

class AddProductAPIView(CreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class = AddProductSerializer


class ProductAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_object(self):
        product_id = self.kwargs.get('product_id')
        obj = get_object_or_404(self.get_queryset(), id=product_id)
        return obj


class AddOpinionAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddOpinionSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        opinion = serializer.save(user=self.request.user, product=product)
        return opinion
    
    def create(self, request, *args, **kwargs):
        try:
            super().create(request)
        except:
            message = 'You had an opinion for this product.'
            return Response({'message': message}, status=400)
        return Response({"message": "Opinion added."}, status=201)


class OpinionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OpinionListSerializer
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Opinion.objects.filter(product_id=product_id)


class AddScoreAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddScoreSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product'] = Product.objects.get(id=self.kwargs['product_id'])
        return context
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        score = serializer.save(user=self.request.user, product=product)
        score_avg = product.score_avg 
        vote = product.vote
        product.vote += 1
        product.score_avg = (score_avg * vote + score.score) / product.vote
        product.save()
        return score

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"message": "Score added."}, status=201)


class ScoreAPIView(RetrieveAPIView):
    serializer_class = ScoreSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def get_object(self):
        product_id = self.kwargs.get('product_id')
        obj = get_object_or_404(self.get_queryset(), id=product_id)
        return obj

