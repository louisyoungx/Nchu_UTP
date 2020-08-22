from django.conf import settings
from django.db import models
from db.base_model import BaseModel

# Create your models here.

class Order(BaseModel):
    '''订单模型类'''
    PAY_METHOD_CHOICES = {
        (1, '当面付款'),
        (2, '微信支付'),
        (3, '支付宝')
    }

    ORDER_STATUS_CHOICES= {
        (1, '待付款'),
        (2, '待交易'),
        (3, '待评价'),
        (4, '已完成')
    }

    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Order', on_delete=models.CASCADE, verbose_name='所属账号')
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE,related_name='Order', verbose_name='所属商品')
    hash = models.CharField(max_length=128, verbose_name='订单编号')
    price = models.IntegerField(verbose_name='成交价格')
    index = models.IntegerField(verbose_name='序号')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=2, verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, verbose_name='支付编号')



    class Meta:
        db_table = 'utp_order'
        verbose_name = '订单列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hash