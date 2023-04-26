from django.urls import path
from . import views

urlpatterns = [
    path('product/list/', views.ProductListAPIView.as_view()),
    path('product/add/', views.AddProductAPIView.as_view()),
    path('product/get/<int:product_id>/', views.ProductAPIView.as_view()),
    path('opinion/add/<int:product_id>/', views.AddOpinionAPIView.as_view()),
    path('opinion/list/<int:product_id>/', views.OpinionListAPIView.as_view()),
    path('score/add/<int:product_id>/', views.AddScoreAPIView.as_view()),
    path('score/get/<int:product_id>/', views.ScoreAPIView.as_view()),    
]