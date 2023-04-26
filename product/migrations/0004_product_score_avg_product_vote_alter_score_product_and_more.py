# Generated by Django 4.1.7 on 2023-04-25 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_alter_score_product_alter_score_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='score_avg',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='vote',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='score',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AlterField(
            model_name='score',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]