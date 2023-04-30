from django.db import models
from user.models import User
from product.models import Product
import uuid


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.user}: {'open' if self.open else 'closed'}"

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self) -> str:
        return f"{self.cart}: {self.product} ={self.count}"
    
    
class Track(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    track = models.UUIDField(default=uuid.uuid4().hex, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.cart.user} - {self.created_at}"