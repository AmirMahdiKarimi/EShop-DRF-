from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    remaining_count = models.IntegerField()
    type = models.CharField(max_length=120)
    brand = models.CharField(max_length=120)

    score_avg = models.FloatField(default=0)
    vote = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Opinion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='opinions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')    

    def __str__(self):
        return f"{self.user.username} opinion on {self.product.name}"
    
class Score(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')    

    def __str__(self):
        return f"{self.user} score '{self.score}' to {self.product}"
    
    

    