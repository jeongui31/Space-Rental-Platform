# Generated by Django 5.0.4 on 2024-11-27 18:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('home', '0002_space_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('booking_status', models.CharField(max_length=20)),
                ('booking_created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking_updated_at', models.DateTimeField(auto_now=True)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.space')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
            options={
                'db_table': 'booking',
            },
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(check=models.Q(('end_date__gt', models.F('start_date'))), name='check_end_date_gt_start_date'),
        ),
    ]