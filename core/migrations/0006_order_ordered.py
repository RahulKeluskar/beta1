# Generated by Django 2.2.7 on 2019-11-21 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]