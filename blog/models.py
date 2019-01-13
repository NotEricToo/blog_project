# -*- conding = utf-8 -*-
from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    chinese_name = models.CharField(max_length=100,blank=True,null=True,verbose_name="中文名字")
    img_path = models.CharField(max_length=500,blank=True,null=True,verbose_name="头像路径")
    desc = models.TextField(max_length=100,blank=True,null=True,verbose_name="描述")



class Article(models.Model):
    atc_topic = models.CharField(max_length=100,blank=True,verbose_name="标题")
    atc_desc = models.CharField(max_length=200,blank=True,null=True,verbose_name="描述")
    user = models.ForeignKey(User,blank=True,null=True,on_delete=False,verbose_name="用户")
    atc_content = models.TextField(max_length=2000,null=True,verbose_name="内容")
    click_count = models.IntegerField(null=True,default=0,verbose_name="点击次数")
    like_count = models.IntegerField(blank=True,null=True,default=0,verbose_name="点赞次数")
    create_time = models.DateTimeField(blank=True,null=True,default = datetime.datetime.now(),verbose_name="创建时间")
    update_time = models.DateTimeField(null=True,default = datetime.datetime.now(),verbose_name="更新时间")
    class Meta:
        db_table = 'tbl_article'
        verbose_name = '文章表'
        ordering = ["-id"]


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    atc_id = models.ForeignKey(Article,on_delete=False)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=False)
    cmt_content = models.CharField(max_length=200,null=True)
    create_time = models.DateTimeField(null=True,default = datetime.datetime.now())
    like_count = models.IntegerField(null=True,default=0)
    super_comment = models.IntegerField(null=True,blank=True,default=None)
    username = models.CharField(max_length=30,null=True,blank=True)
    email = models.CharField(max_length=50,null=True,blank=True)
    class Meta:
        db_table = 'tbl_comment'
        verbose_name = '评论表'

class UserTrack(models.Model):
    id = models.AutoField(primary_key=True)
    remote_addr = models.CharField(max_length=100,null=True)
    http_user_agent = models.CharField(max_length=200,null=True)
    http_referer = models.CharField(max_length=200,null=True)
    class Meta:
        db_table = 'tbl_user_track'
        verbose_name = '用户跟踪表'

    @classmethod
    def create(cls, remote_addr,http_user_agent,http_referer):
        track = cls(remote_addr = remote_addr,http_user_agent=http_user_agent,http_referer=http_referer )
        return track

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=50,null=False,verbose_name="分类名称")
    cg_desc = models.TextField(max_length=1000,null=True,blank=True,verbose_name="分类描述")
    imgpath = models.CharField(max_length=500,null=True,blank=True)
    articles = models.ManyToManyField(Article,blank=True)
    class Meta:
        db_table='tbl_category'
        verbose_name = '文章分类'

    def __str__(self):
        return 'Catetory id : ' + str(self.id) + ' Category Name : ' + self.cg_name

# class Mid_atc_cg(models.Model):
#     id = models.AutoField(primary_key=True)
#     atc_id = models.ForeignKey(Article,on_delete=models.CASCADE)
#     cg_id = models.ForeignKey(Category,on_delete=models.CASCADE)
#     class Meta:
#         db_table='tbl_mid_atc_cg'
#         verbose_name = '文章分类中间表'






