from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from utils.Mixin import LoginMixin

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
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
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
