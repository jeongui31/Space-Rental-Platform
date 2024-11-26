# Generated by Django 5.0.4 on 2024-11-26 10:18

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('space_id', models.AutoField(primary_key=True, serialize=False)),
                ('space_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
                ('capacity', models.PositiveIntegerField()),
                ('price_per_date', models.PositiveIntegerField()),
                ('space_created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('space_updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'db_table': 'space',
            },
        ),
    ]