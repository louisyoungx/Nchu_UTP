from django.contrib import admin
from user.models import User


# User模型的管理器
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'college', 'nickname', 'apartment', 'head_img')

#admin.site.register(User, UserAdmin)