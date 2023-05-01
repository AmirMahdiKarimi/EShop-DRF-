from django.contrib import admin
from .models import Cart, CartProduct, Track

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ('open',) 


class TrackFields(admin.ModelAdmin):
    readonly_fields = ('track', 'created_at') 
    fields = ('cart', 'track', 'created_at')

admin.site.register(CartProduct)
admin.site.register(Track, TrackFields)