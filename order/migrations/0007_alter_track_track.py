# Generated by Django 4.1.7 on 2023-04-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_track_track'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='track',
            field=models.UUIDField(default='bf716d7c136b4772b9e740fbe927d0d6', editable=False, unique=True),
        ),
    ]
