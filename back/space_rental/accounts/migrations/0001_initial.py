# Generated by Django 5.0.4 on 2024-11-27 05:27

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('role', models.CharField(max_length=10)),
                ('user_created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'User',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('company_name', models.CharField(default='개인', max_length=100, null=True)),
                ('business_license', models.CharField(max_length=30, unique=True)),
                ('host_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
            ],
            options={
                'db_table': 'host',
                'managed': True,
            },
        ),
    ]
