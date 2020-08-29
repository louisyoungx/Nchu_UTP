# Generated by Django 3.0.5 on 2020-08-29 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200822_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.SmallIntegerField(choices=[(3, '待评价'), (4, '已完成'), (2, '待交易'), (1, '待付款')], default=2, verbose_name='订单状态'),
        ),
    ]
