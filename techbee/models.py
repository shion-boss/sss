from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import cloudinary
from cloudinary.models import CloudinaryField

# Create your models here.

class user_meta(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=20)
    photo=CloudinaryField('image',null=True, blank=True)
    name=models.CharField(max_length=20)
    plofile=models.TextField(max_length=220,default='')
    point=models.IntegerField(default=0)
    like_point=models.IntegerField(default=0)
    give_like=models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(10)])
    qrcode=models.CharField(max_length=30)
    position=models.CharField(max_length=10,default='',blank=True,null=True)
    last_login=models.DateTimeField(default=timezone.datetime.now)

class categories_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    categories=models.CharField(max_length=30)
    img=CloudinaryField('image',null=True, blank=True)
    post_time=models.DateTimeField(default=timezone.datetime.now)


class parts_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    categories=models.ForeignKey(categories_model,on_delete=models.SET_NULL,blank=True,null=True)
    file_name=models.CharField(max_length=30)
    video=CloudinaryField("video",default='')
    image =CloudinaryField('image', null=True, blank=True)
    html_code=models.TextField(max_length=2000)
    css_code=models.TextField(max_length=2000)
    like_count=models.IntegerField(default=0)
    post_time=models.DateTimeField(default=timezone.datetime.now)

class channel_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.ForeignKey(User,on_delete=models.CASCADE,related_name='channel_user',blank=True,null=True)
    channel_time=models.DateTimeField(default=timezone.datetime.now)

class like_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    part_id=models.ForeignKey(parts_model,on_delete=models.CASCADE,blank=True,null=True)
    like_time=models.DateTimeField(default=timezone.datetime.now)

class favorite_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    part_id=models.ForeignKey(parts_model,on_delete=models.CASCADE,blank=True,null=True)
    favorite_time=models.DateTimeField(default=timezone.datetime.now)

class afirieito_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    introducer=models.CharField(max_length=20)

class event_model(models.Model):
    img=CloudinaryField('image',null=True, blank=True)
    event_name=models.CharField(max_length=15)
    event_date=models.CharField(max_length=15)
    event_time=models.CharField(max_length=15)
    event_venue=models.CharField(max_length=30)
    event_dis=models.TextField(max_length=140,blank=True,null=True)
    set_event=models.DateTimeField(default=timezone.datetime.now)

class event_img_model(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(event_model,on_delete=models.CASCADE)
    img=CloudinaryField('image', blank=True,null=True)

class footer_cat_model(models.Model):
    footer_cat=models.CharField(max_length=20)

    def __str__(self):
        return self.footer_cat

class footer_model(models.Model):
    footer_cat=models.ForeignKey(footer_cat_model,on_delete=models.SET_NULL,blank=True,null=True)
    header=models.CharField(max_length=30)
    img=CloudinaryField('image', null=True, blank=True)
    text=models.TextField(max_length=1000)

    def __str__(self):
        return self.header

class tech_tube_model(models.Model):
    category=models.CharField(max_length=30)
    image =CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.category

class tube_movie_model(models.Model):
    category=models.ForeignKey(tech_tube_model,on_delete=models.SET_NULL,blank=True,null=True)
    title=models.CharField(max_length=30)
    video=CloudinaryField("video",default='')
    image =CloudinaryField('image', null=True, blank=True)
    text=models.TextField(max_length=2000)
    post_time=models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.title

class tech_teaching_model(models.Model):
    category=models.CharField(max_length=30)
    image =CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.category

class teaching_movie_model(models.Model):
    category=models.ForeignKey(tech_teaching_model,on_delete=models.SET_NULL,blank=True,null=True)
    title=models.CharField(max_length=30)
    video=CloudinaryField("video",default='')
    image =CloudinaryField('image', null=True, blank=True)
    text=models.TextField(max_length=2000)
    post_time=models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.title

class tech_bee_model(models.Model):
    category=models.CharField(max_length=30)
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.category

class bee_model(models.Model):
    category=models.ForeignKey(tech_bee_model,on_delete=models.SET_NULL,blank=True,null=True)
    title=models.CharField(max_length=30)
    image =CloudinaryField('image', null=True, blank=True)
    text=models.TextField(max_length=2000)
    post_time=models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.title
