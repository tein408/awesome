from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import uuid

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')    
    profile_img = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=11)
    activated = models.BooleanField()
    rating_score = models.DecimalField(max_digits=3, decimal_places=1)

    region = models.CharField(max_length=100, null=True)
    region_certification = models.CharField(max_length=1, default='N')
    created_at = models.DateTimeField(auto_now_add=True)

class follow_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

class block_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking_users')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by_user')
    created_at = models.DateTimeField(auto_now_add=True)

class evaluation_items(models.Model):
    score = models.DecimalField(max_digits=3, decimal_places=1)
    text = models.CharField(max_length=20)

class categories(models.Model):
    name = models.CharField(max_length=20)
    
class files(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class address_areas(models.Model):
    sido = models.CharField(max_length=50)
    sigg = models.CharField(max_length=50)
    emd = models.CharField(max_length=50)
    load_code = models.CharField(max_length=50)
    load_name = models.CharField(max_length=50)
    building_bonbeon = models.CharField(max_length=50)
    building_bubeon = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    building_num = models.CharField(max_length=50)
    building_x = models.DecimalField(max_digits=20, decimal_places=6)
    building_y = models.DecimalField(max_digits=20, decimal_places=6)
    entrance_x = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    entrance_y = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    emd_gubun = models.CharField(max_length=50)
    
class sido_areas(models.Model):
    adm_code = models.CharField(max_length=2)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)
    
class sigg_areas(models.Model):
    sido_area = models.ForeignKey(sido_areas,on_delete=models.CASCADE)
    adm_code = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=20)

# class emd_areas(models.Model):
#     sigg_area =models.ForeignKey(sigg_areas, on_delete=models.CASCADE)
#     adm_code = models.CharField(max_length=10)
#     name = models.CharField(max_length=50)
#     geom = models.MultiPolygonField(srid=4326)
#     location = models.PointField(srid=4326)
#     version = models.CharField(max_length=20)

# class activity_areas(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reference_area_id = models.IntegerField()
#     distance_meters = models.SmallIntegerField()
#     emd_area = ArrayField(models.ForeignKey(emd_areas, on_delete=models.CASCADE))
#     authenticated_at = models.DateTimeField(null=True)

class goods(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    # location = models.ForeignKey(address_areas, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='post_images/', null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    product_reserved = models.CharField(max_length=1, default='N')  # 예약 여부
    product_sold = models.CharField(max_length=1, default='N')  # 판매 여부

    view_num = models.PositiveIntegerField(default=0)  # 조회 수
    chat_num = models.PositiveIntegerField(default=0)  # 채팅 수

    # 매물 카테고리
    # category = models.ForeignKey(categories, on_delete=models.CASCADE)
    # 공개 / 비공개 저장
    # status = models.CharField(max_length=10)
    # 끌어올린 날짜 저장
    # refreshed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class transaction_reviews(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(goods, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    # evaluation_items = ArrayField(models.ForeignKey(evaluation_items, on_delete=models.CASCADE))
    evaluation_items_ids = models.ManyToManyField(evaluation_items)
    created_at = models.DateTimeField(auto_now_add=True)

class price_offers(models.Model):
    offerer = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(goods, on_delete=models.CASCADE)
    offered_price = models.IntegerField()
    accept_or_not = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class notifications(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(goods, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class notification_keywords(models.Model):
    register = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class wish_lists(models.Model):
    register = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(goods, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class chat_room(models.Model):
    goods = models.ForeignKey(goods, on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    created_at = models.DateTimeField(auto_now_add=True)

class chat_messages(models.Model):  
    chat_room = models.ForeignKey(chat_room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='receiver')
    message = models.CharField(max_length=500)
    read_or_not = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat_uuid = models.UUIDField(editable=False, unique=True, null=True)

