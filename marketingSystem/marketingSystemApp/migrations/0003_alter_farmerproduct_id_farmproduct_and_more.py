# Generated by Django 4.2.11 on 2024-04-26 01:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('marketingSystemApp', '0002_remove_customuser_name_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerproduct',
            name='id_farmproduct',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='farmerproduct',
            name='id_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.product'),
        ),
        migrations.AlterField(
            model_name='farmerproduct',
            name='rating',
            field=models.CharField(default='N/A', max_length=255),
        ),
    ]
