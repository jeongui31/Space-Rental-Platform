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
        managed = True
        db_table = 'User'
        
class Host(models.Model):
    user = models.OneToOneField(
        'User',  # 'User' 모델과 연결
        on_delete=models.CASCADE,  # 연결된 'User' 삭제 시 Host도 삭제
        primary_key=True 
    )
    company_name = models.CharField(
        max_length=100,
        null=True,
        default='개인'
    )
    business_license = models.CharField(
        max_length=30,
        unique=True 
    )

    class Meta:
        managed = True
        db_table = 'host'
        
    def save(self, *args, **kwargs):
        if not self.company_name:  # company_name이 비어 있으면 default 값 설정
            self.company_name = '개인'
        super().save(*args, **kwargs)