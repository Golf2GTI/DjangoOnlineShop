# Generated by Django 5.0 on 2023-12-15 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_productimage_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='order',
        ),
    ]
