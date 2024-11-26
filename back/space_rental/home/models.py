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

class SpaceCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=30, unique=True, null=False)

    class Meta:
        db_table = 'space_category'

    def __str__(self):
        return self.category_name


class SpaceCategoryMapping(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    category = models.ForeignKey(SpaceCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'space_category_mapping'

class SpaceWithCategories(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    price_per_date = models.PositiveIntegerField()
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    space_created_at = models.DateTimeField()
    space_updated_at = models.DateTimeField()
    categories = models.TextField()  # 카테고리 목록은 콤마로 구분된 문자열

    class Meta:
        managed = False  # Django가 데이터베이스를 관리하지 않음
        db_table = 'space_with_categories'  # VIEW 이름