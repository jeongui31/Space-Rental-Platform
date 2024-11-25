from django.db import models
from django.utils.timezone import now

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    user_name=models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10)
    user_created_at = models.DateTimeField(default=now)
    user_updated_at = models.DateTimeField(default=now)
    
    class Meta:
        managed = False
        db_table = 'User'
        
class Host(models.Model):
    user = models.OneToOneField(
        'User',  # 'User' 모델과 연결
        on_delete=models.CASCADE,  # 연결된 'User' 삭제 시 Host도 삭제
        primary_key=True 
    )
    company_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    business_license = models.CharField(
        max_length=30,
        unique=True 
    )
    host_rating = models.DecimalField(
        max_digits=3,  # 최대 자릿수 (소수점 포함)
        decimal_places=2,  # 소수점 아래 두 자리
        default=0.00  # 기본값 0.00
    )

    class Meta:
        managed = False
        db_table = 'host'