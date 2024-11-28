from django.db import models
from django.utils.timezone import now
from accounts.models import User

class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    space_name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
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
        
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    booking_status = models.CharField(max_length=20, null=False)
    booking_created_at = models.DateTimeField(default=now, null=False)
    booking_updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'booking'  # 테이블 이름
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F('start_date')),
                name='check_end_date_gt_start_date'
            ),
        ]
        
from django.db import models
from django.utils.timezone import now
from accounts.models import User


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey('Space', on_delete=models.CASCADE)
    review_rating = models.PositiveIntegerField(null=False)
    comment = models.TextField(null=True, blank=True)
    review_created_at = models.DateTimeField(default=now, null=False)

    class Meta:
        db_table = 'review'  # Specify the table name
        constraints = [
            models.CheckConstraint(
                check=models.Q(review_rating__gte=1) & models.Q(review_rating__lte=5),
                name='check_review_rating_range'
            ),
        ]

class UserBookingView(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    space_name = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_status = models.CharField(max_length=20)

    class Meta:
        managed = False  # Django가 데이터베이스를 관리하지 않음
        db_table = 'user_booking_view'  # 뷰 이름
