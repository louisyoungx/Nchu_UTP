from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.

# 用户模型类
class UserInfo(BaseModel):
    '''用户模型类'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Info', on_delete=models.CASCADE, verbose_name='所属用户')
    trading_place = models.CharField(max_length=20, blank=True, verbose_name='交易地点')
    head_img = models.ImageField(upload_to='head', blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=6, blank=True, verbose_name='昵称')
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    QQ = models.CharField(max_length=20, blank=True, verbose_name='QQ号')
    WeChat = models.CharField(max_length=20, blank=True, verbose_name='微信号')
    signature = models.CharField(max_length=20, blank=True, verbose_name='个性签名')
    date_birth = models.CharField(max_length=10, blank=True, verbose_name='生日')
    college = models.CharField(max_length=20, blank=True, verbose_name='学院')
    apartment = models.CharField(max_length=5, blank=True, verbose_name='寝室楼')


    class Meta:
        db_table = 'utp_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname