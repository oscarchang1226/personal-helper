# Generated by Django 5.1.3 on 2024-11-13 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField()),
                ('account_id', models.IntegerField()),
                ('payment_flag', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceManager',
            fields=[
                ('manager_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=100)),
                ('account_status', models.CharField(max_length=100)),
                ('service_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.servicemanager')),
            ],
        ),
    ]