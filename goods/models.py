from django.conf import settings
from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField

# Create your models here.

class Goods(BaseModel):
    '''商品模型类'''
    status_choices = (
        (0, '下架'),
        (1, '在售'),
        (2, '售出')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='所属用户')
    name = models.CharField(max_length=15, verbose_name='商品标题')
    price = models.IntegerField(verbose_name='商品价格')
    intro = HTMLField(verbose_name='简介')
    place = models.CharField(max_length=20, verbose_name='希望交易地点')
    surface = models.ImageField(upload_to='goods', verbose_name='商品封面')
    classify = models.CharField(max_length=5, verbose_name='所属类别')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    like_num = models.IntegerField(default=0, verbose_name='收藏数')
    display_type = models.SmallIntegerField(default=1,choices=status_choices , verbose_name='商品状态')


    class Meta:
        db_table = 'utp_goods'
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class GoodsImg(BaseModel):
    '''商品图片模型类'''
    goods = models.ForeignKey('goods', on_delete=models.CASCADE, verbose_name='所属商品')
    hash = models.CharField(max_length=128, verbose_name='图片编号')
    image = models.ImageField(upload_to='goods', verbose_name='图片')
    index = models.IntegerField(verbose_name='序号')


    class Meta:
        db_table = 'utp_goods_img'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image