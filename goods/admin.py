from django.contrib import admin
from goods.models import Goods, GoodsImg


# Goods模型的管理器
@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'click_num', 'like_num', 'surface')

@admin.register(GoodsImg)
class GoodsImgAdmin(admin.ModelAdmin):
    list_display = ('goods', 'index', 'hash', 'image')

#admin.site.register(User, UserAdmin)