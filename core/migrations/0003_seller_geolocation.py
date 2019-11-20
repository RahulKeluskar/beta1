# Generated by Django 2.2.7 on 2019-11-14 18:01

from django.db import migrations
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_seller_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(blank=True, max_length=100, null=True),
        ),
    ]