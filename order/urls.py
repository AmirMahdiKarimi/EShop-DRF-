from django.urls import path
import uuid
from . import views


urlpatterns = [
    path('cart/add/', views.AddToCartAPIView.as_view()),
    path('cart/remove/', views.DeleteFromCartAPIView.as_view()),
    path('shop/', views.ShopAPIView.as_view()),
    path('track/list/', views.TrackListAPIView.as_view()),
    path('track/get/<uuid:track_id>', views.TrackGetAPIView.as_view()),
]