# Generated by Django 4.2.3 on 2024-06-24 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketingSystemApp', '0019_farmerproduct_certifications_farmerproduct_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='certifications',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='minimum_order_quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='product_quality',
            field=models.CharField(default='Standard', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='production_method',
            field=models.CharField(default='Standard', max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='season_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='season_start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
