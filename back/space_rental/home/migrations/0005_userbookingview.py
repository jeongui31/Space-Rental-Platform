# Generated by Django 5.0.4 on 2024-11-28 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_review_review_check_review_rating_range'),
    ]

    operations = [
        # SQL 뷰 생성
        migrations.RunSQL(
            sql="""
                CREATE VIEW user_booking_view AS
                SELECT 
                    b.booking_id,
                    u.user_name,
                    u.email,
                    u.phone,
                    s.space_name,
                    s.image,
                    s.address,
                    b.start_date,
                    b.end_date,
                    b.booking_status
                FROM 
                    booking b
                JOIN 
                    space s ON b.space_id = s.space_id
                JOIN 
                    user u ON b.user_id = u.user_id
                ORDER BY 
                    b.booking_created_at DESC;
            """,
            reverse_sql="DROP VIEW IF EXISTS user_booking_view;"
        ),

        # Django 모델 정의
        migrations.CreateModel(
            name='UserBookingView',
            fields=[
                ('booking_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('space_name', models.CharField(max_length=200)),
                ('image', models.URLField(blank=True, null=True)),
                ('address', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('booking_status', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'user_booking_view',
                'managed': False,
            },
        ),
    ]
