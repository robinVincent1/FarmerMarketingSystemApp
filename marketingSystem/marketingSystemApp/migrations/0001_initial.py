# Generated by Django 4.2.11 on 2024-04-23 07:22

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_approved', models.CharField(max_length=255)),
                ('date_approved', models.DateField(null=True)),
                ('volume_approved', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_user', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('role', models.CharField(choices=[('farmer', 'Farmer'), ('customer', 'Customer'), ('funder', 'Funder')], max_length=8)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='custom_users_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='custom_users_permissions', related_query_name='custom_user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FarmerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_farmproduct', models.CharField(max_length=255)),
                ('product_date', models.DateField(null=True)),
                ('product_quality', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_volume', models.CharField(max_length=255)),
                ('remaining_volume', models.CharField(max_length=255)),
                ('date_available', models.DateField(null=True)),
                ('rating', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FinancingOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_offer', models.CharField(max_length=255)),
                ('offer_date', models.DateField(null=True)),
                ('content', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_product', models.CharField(max_length=255)),
                ('product_name', models.CharField(max_length=255)),
                ('measurement', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_transaction', models.CharField(max_length=255)),
                ('volume', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateField(null=True)),
                ('id_approved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.approved')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_request', models.CharField(max_length=255)),
                ('request_status', models.CharField(max_length=255)),
                ('date_request', models.DateField(null=True)),
                ('rating', models.CharField(max_length=255)),
                ('need_date', models.DateField(null=True)),
                ('product_quality', models.CharField(max_length=255)),
                ('product_volume', models.CharField(max_length=255)),
                ('id_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Recommandation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_recommendation', models.CharField(max_length=255)),
                ('id_request', models.CharField(max_length=255)),
                ('recommendation_score', models.CharField(max_length=255)),
                ('farm_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.farmerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='FinancingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_financingrequest', models.CharField(max_length=255)),
                ('rating', models.CharField(max_length=255)),
                ('date_request', models.DateField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.financingoffer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='FinancingApproved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_financingapproved', models.CharField(max_length=255)),
                ('date_approved', models.DateField(null=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.financingrequest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='farmerproduct',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.product'),
        ),
        migrations.AddField(
            model_name='farmerproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.customuser'),
        ),
        migrations.CreateModel(
            name='Chatting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_chat', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('channel_date', models.DateField(null=True)),
                ('id_user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1_chats', to='marketingSystemApp.customuser')),
                ('id_user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_chats', to='marketingSystemApp.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='approved',
            name='farm_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.farmerproduct'),
        ),
        migrations.AddField(
            model_name='approved',
            name='id_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketingSystemApp.request'),
        ),
    ]
