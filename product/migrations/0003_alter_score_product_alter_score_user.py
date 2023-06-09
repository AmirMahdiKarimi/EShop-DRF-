# Generated by Django 4.1.7 on 2023-04-25 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_score_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='product.product'),
        ),
        migrations.AlterField(
            model_name='score',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score', to=settings.AUTH_USER_MODEL),
        ),
    ]
