from django.db import models
from django.utils.timezone import now
from accounts.models import User

class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    capacity = models.PositiveIntegerField(null=False)
    price_per_date = models.PositiveIntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space_created_at = models.DateTimeField(default=now)
    space_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'space'  # 테이블 이름 지정

    def __str__(self):
        return self.space_name
