# Generated by Django 5.0 on 2023-12-13 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_product_category_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
