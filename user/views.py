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

        try:
            head = info.head_img
            avatar = FDFS_URL + str(head)
        except:
            avatar = "image/mine/head.png"

        sign = "欢迎，来到昌航有物！"
        if info.signature:
            signature = info.signature
            if len(str(signature)) > 9:
                signature = signature[0:8]+"······"
        else:
            signature = sign
        if info.nickname:  nickname= info.nickname
        else: nickname = sign
        if info.date_birth:  birthday= info.date_birth
        else: birthday = sign
        if info.phone:     phone= info.phone
        else: phone = sign
        if info.QQ:        QQ= info.QQ
        else: QQ = sign
        if info.grade:     grade= info.grade
        else: grade = sign
        if info.college:   college= info.college
        else: college = sign
        if info.apartment: apartment= info.apartment
        else: apartment = sign

        userLogin = {
            "status":    1,
            "avatar":    avatar,
            "username":  nickname,
            "nickname":  nickname,
            "signature": signature,
            "birthday":  birthday,
            "phone":     phone,
            "QQ":        QQ,
            "grade":     grade,
            "college":   college,
            "apartment": apartment,
        }
        return render(request, 'user-info.html', context=userLogin)
    def post(self, request):
        '''
        'signature': signature,
        'nickname': nickname,
        'birthday': birthday,
        'phone': phone,
        'QQ': QQ,
        'grade': grade,
        'college': college,
        'apartment': apartment
        '''
        try:
            user = request.user
            info = user.Info.all()[0]

            signature = request.POST.get('signature')
            nickname = request.POST.get('nickname')
            birthday = request.POST.get('birthday')
            phone = request.POST.get('phone')
            QQ = request.POST.get('QQ')
            grade = request.POST.get('grade')
            college = request.POST.get('college')
            apartment = request.POST.get('apartment')

            if signature: info.signature = signature
            if nickname:  info.nickname  = nickname
            if birthday:  info.date_birth  = birthday
            if phone:     info.phone     = phone
            if QQ:        info.QQ        = QQ
            if grade:     info.grade     = grade
            if college:   info.college   = college
            if apartment: info.apartment = apartment

            info.save()
            return JsonResponse({'status':'1'})
        except:
            return JsonResponse({'status':'0'})

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
        info = user.Info.all()[0]
        username = info.nickname

        try:
            head = info.head_img
            avatar = FDFS_URL + str(head)
        except:
            avatar = "image/mine/head.png"
        print(username, avatar)
        userLogin = {
            "status": 1,
            "username": username,
            'avatar': avatar,
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