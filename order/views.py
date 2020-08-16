from django.shortcuts import render
from django.views import View
from utils.Mixin import LoginMixin

# Create your views here.

# 用户订单
class ListView(LoginMixin, View):
    def get(self, request):
        user = request.user
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
        }
        return render(request, 'order-list.html', context=userLogin)

class InfoView(LoginMixin, View):
    def get(self, request):
        user = request.user
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
        }
        return render(request, 'order-info.html', context=userLogin)

class ComfrimView(LoginMixin, View):
    def get(self, request):
        user = request.user
        username = user.username
        userLogin = {
            "status": 1,
            "username": username,
        }
        return render(request, 'order-comfrim.html', context=userLogin)
