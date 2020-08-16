from django.contrib import admin
from order.models import Order


# Order模型的管理器
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'goods', 'order_status', 'price', 'index', 'pay_method')

#admin.site.register(User, UserAdmin)