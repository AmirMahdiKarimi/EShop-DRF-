# Generated by Django 4.1.7 on 2023-04-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_track_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='track',
            field=models.UUIDField(default='1a9f10f5744a4cf181f9e4d1f453d3bd', editable=False, unique=True),
        ),
    ]
