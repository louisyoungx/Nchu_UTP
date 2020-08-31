from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from Nchu_UTP.settings import SITE_URL, FDFS_URL
from utils.Mixin import LoginMixin
from user.models import UserInfo

# Create your views here.

# 个人主页
class PageView(View):
    """个人页面"""
    def get(self, request, username):
        """处理GET请求业务逻辑"""
        if request.user.is_authenticated:
            userPage = {
                "status":1,
                "username":username,
            }
            return render(request, 'user-personal-page.html', context=userPage)
        return render(request, 'user-personal-page.html')

# 个人信息页面
class InfoView(LoginMixin, View):
    def get(self, request):
        user = request.user
        info = user.Info.all()[0]
        nickname = info.nickname
        try:
            head = info.head_img
            avatar = FDFS_URL + str(head)
        except:
            avatar = "image/mine/head.png"
        userLogin = {
            "status": 1,
            "username": nickname,
            "avatar":avatar,
        }
        return render(request, 'user-info.html', context=userLogin)

# 用户收藏
class FavorView(LoginMixin, View):
    def get(self, request):
        user = request.user
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
        }
        return render(request, 'user-favorite.html', context=userLogin)

# 用户设置页面
class SettingView(LoginMixin, View):
    def get(self, request):
        user = request.user
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
        }
        return render(request, 'user-setting.html', context=userLogin)
    def post(self,request):
        setting = request.POST.get('setting')
        if setting == 'exit':
            logout(request)
            return JsonResponse({'status':1})


def avatar(request):
    # 获取上传头像的处理对象
    if request.user.is_authenticated:
        user = request.user
        info = user.Info.all()[0]
        if request.method == 'POST':
            avatar = request.FILES.get('avatar')

            # 1. 删除原头像
            try:
                head = info.head_img
                info.head_img.delete()
            except:
                pass
            # 2. 将传来的头像数据，保存到数据库
            info.head_img = avatar
            info.save()
            return redirect(reverse('user:info'))

        return redirect(reverse('user:info'))