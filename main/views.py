import re
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, request
from django.template import loader
from django.urls import reverse
from django.views import View
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as tjss, SignatureExpired
from Nchu_UTP.settings import SITE_URL
from celeryT.tasks import send_register_active_email
from user.models import UserInfo

# Create your views here.



# 主页



class HomeView(View):
    '''主页'''
    def get(self, request):
        return render(request, 'homePage.html')

# 分类页面
class ClassView(View):
    '''分类页面'''
    def get(self, request):
        return render(request, 'classPage.html')

# 个人页面
class MineView(View):
    """个人页面"""
    def get(self, request):
        """处理GET请求业务逻辑"""
        if request.user.is_authenticated:
            user = request.user
            queryset = user.Info.all()
            for li in queryset:
                info = li
            nickname = info.nickname
            try:
                head = info.head_img
                avatar = SITE_URL+"media/"+str(head)
            except:
                avatar = "image/mine/head.png"
            nickname = info.nickname
            userLogin = {
                "status":1,
                "username":nickname,
                "avatar":avatar,
            }
            return render(request, 'minePage.html', context=userLogin)
        return render(request, 'minePage.html')

# 购物车页面
class CartView(View):
    '''购物车页面'''

    def get(self, request):
        return render(request, 'cartPage.html')

# 索引页面
class IndexView(View):
    '''索引页面（登陆、注册）'''

    def get(self, request):
        '''索引页面'''
        if request.user.is_authenticated:
            # 判断用户是否登陆
            return redirect(reverse('main:home'))
        else:
            next_url = request.GET.get('next', reverse('main:home'))
            print(next_url)
            # 获取所有cookie
            cookies = request.COOKIES
            # 假如cookie存在
            if 'username' in cookies:
                # 获取记住的用户名
                username = cookies['username']
            else:
                username = ''
            # 返回response
            return render(request, 'index.html',{'username': username, 'next':next_url })

    def post(self, request):
        '''登陆/注册？'''
        reType = request.POST.get('type')

        if reType == 'login':
            '''ajax登陆检查'''

            # 获取数据
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if settings.DEBUG == True:
                print('{username}--登陆'.format(username=username))
                try:
                    print('{username}--认证'.format(username=user.username))
                except:pass

            # 校验数据
            if not all([username, password]):
                return JsonResponse({'check': '2'})

            # 业务处理
            # elif username == 'Louis' and password == '201314abc':
            elif user is not None:
                if user.is_active:
                    # 用户已激活
                    next_url = request.POST.get('next', reverse('main:home'))
                    print(next_url)
                    # 设置session,标记为登陆
                    login(request, user)
                    return JsonResponse({'check': '1', 'next':next_url}) # 登陆成功
                else:
                    #用户未激活
                    send_email(user.id, user.email, username)
                    errmsg = '用户{user}未激活，已重新发送邮件'.format(user=username)
                    return JsonResponse({'check':'3','errmsg':errmsg})
            else:
                # 用户名或密码错误
                return JsonResponse({'check': '0'})

        elif reType == 'register':
            '''ajax注册处理'''

            # 接收数据
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            # 进行校验
            if not all([username, password, email]):
                # 数据不完整
                return JsonResponse({'statusCode': 2})
            if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
                # 邮箱形式不对
                return JsonResponse({'statusCode': 3})

            # 进行业务处理：注册
            # 查找用户名是否重复
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = ""

            try:
                emails = User.objects.get(email=email)
            except User.DoesNotExist:
                emails = ""
            if user:
                return JsonResponse({'statusCode': 0})
            elif emails:
                return JsonResponse({'statusCode': 4})
            elif user == "" and emails == "":
                user = User.objects.create_user(username, email, password)
                user.is_active = 0
                info = UserInfo()
                info.user = user
                info.nickname = username
                user.save()
                info.save()

                #发送激活邮件，包含激活链接：http://nchu-UTP/active/[加盐id]

                #if send_register_active_email(user.id, email, username):   #celery异步处理
                if send_email(user.id, email, username):
                    # 返回应答
                    return JsonResponse({'statusCode': 1})
                else:
                    return JsonResponse({'statusCode': 5})

# 激活页面
class ActiveView(View):
    '''用户激活'''
    def get(self, request, token):
        '''进行用户激活'''
        #进行解密，获取要激活的用户信息
        key = tjss(settings.SECRET_KEY, 600)
        try:
            info = key.loads(token)
            #获取用户ID
            user_id = info['confirm']

            #根据用户ID获取用户信息
            user = User.objects.get(id = user_id)
            user.is_active = 1
            user.save()

            #跳转到登陆页面
            return redirect(reverse('main:index'))

        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse("激活链接已过期")


# 发送邮件
def send_email(ID,Email,User):
    # 发送激活邮件，包含激活链接：http://nchu-UTP/mine/active/[加盐id]
    # 用itsdangerous加密，导入为tjss
    key = tjss(settings.SECRET_KEY, 600)
    # 需要加密的信息
    info = {'confirm': ID}
    # 已经加密的信息
    tokenBytes = key.dumps(info)
    token = tokenBytes.decode()
    #url地址
    site = settings.SITE_HOST
    path = reverse('main:activity')
    # 发邮件
    #主题
    subject = '遇见，昌航有物'
    #正文
    message = ''
    #发件人
    sender = settings.EMAIL_HOST_USER
    #收件人列表
    receiver = [Email]

    url = 'http://{site}{path}/{token}/'.format(site=site, path=path, token=token)
    print(url)
    #team_blog = reverse('team:blog')
    team_blog = 'www.baidu.com'

    context = {
        'user': User,
        'url': url,
        'team':team_blog ,
    }
    email_template_name = 'email.html'
    t = loader.get_template(email_template_name)
    html_content = t.render(context)
    msg = EmailMultiAlternatives(subject, html_content, sender, receiver)
    msg.attach_alternative(html_content, "text/html")

    if msg.send():
        return 1
    else:
        return 0



def set_cookie(request):
    '''设置cookie'''
    userCookie = HttpResponse('SetCookie')
    #设置一个cookie信息,30天过期
    userCookie.set_cookie('username', '', max_age=30*24*60*60)
    return userCookie

def get_cookie(request):
    '''获得cookie信息'''
    #取出cookie num的值
    username = request.COOKIES['username']

def notFound404(request):
    return render(request, '404.html')

def test(request):
    return render(request,'')




'''
def page_not_found_view(request, exception, template_name='blog/error_page.html'):
    if exception:
        logger.error(exception)
    url = request.get_full_path()
    return render(request,
                  template_name,
                  {'message': '哎呀，您访问的地址 ' + url + ' 是一个未知的地方。请点击首页看看别的？',
                   'statuscode': '404'},
                  status=404)

def server_error_view(request, template_name='blog/error_page.html'):
    return render(request,
                  template_name,
                  {'message': '哎呀，出错了，我已经收集到了错误信息，之后会抓紧抢修，请点击首页看看别的？',
                   'statuscode': '500'},
                  status=500)

def permission_denied_view(request, exception, template_name='blog/error_page.html'):
    if exception:
        logger.error(exception)
    return render(
        request, template_name, {
            'message': '哎呀，您没有权限访问此页面，请点击首页看看别的？', 'statuscode': '403'}, status=403)
'''  # 备用

'''

def login(request):
    #ajax登陆检查

    username = request.POST.get('username')
    password = request.POST.get('password')
    # 获取数据
    print(username)

    # 判断是否正确
    # 用户名或密码为空
    if username == '' or password == '':
        return JsonResponse({'check': '2'})
    #用户名和密码正确
    elif username == 'Louis' and password == '201314abc':
        #设置cookie
        request.session['isLogin'] = True
        return JsonResponse({'check': '1'})
    #用户名或密码错误
    else:
        return JsonResponse({'check': '0'})

def register(request):
    #注册处理

    username = request.POST.get('username')
    password = request.POST.get('password')
    # 接收数据
    email = request.POST.get('email')

    #进行校验
    if not all([username, password, email]):
        #数据不完整
        return JsonResponse({'statusCode':2})
    if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        #邮箱形式不对
        return JsonResponse({'statusCode':3})

    #进行业务处理：注册
    #查找用户名是否重复
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        user = ""

    if user:
        return JsonResponse({'statusCode': 0})
    elif user == "":
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
    #返回应答
    return JsonResponse({'statusCode': 1})

'''  # 替换