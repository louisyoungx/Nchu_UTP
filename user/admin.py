from django.contrib import admin
from user.models import UserInfo


# User模型的管理器
@admin.register(UserInfo)

class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'college', 'nickname', 'apartment', 'head_img')

#admin.site.register(User, UserAdmin)