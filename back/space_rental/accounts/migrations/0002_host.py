# Generated by Django 5.0.4 on 2024-11-26 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('business_license', models.CharField(max_length=30, unique=True)),
                ('host_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
            ],
            options={
                'db_table': 'host',
                'managed': False,
            },
        ),
    ]
