# Generated by Django 4.0.4 on 2022-05-22 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_customer_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
    ]