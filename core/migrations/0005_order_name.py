# Generated by Django 2.2.7 on 2019-11-21 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_orderitem_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
