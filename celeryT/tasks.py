#使用celery异步任务处理
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from itsdangerous import TimedJSONWebSignatureSerializer as tjss

#创建一个Celery类实例对象
app = Celery('celeryT.tasks', broker='127.0.0.1:6379/1', )

#定义任务函数
@app.task
def send_register_active_email(ID, Email, User):
    # 发送激活邮件，包含激活链接：http://nchu-UTP/mine/active/[加盐id]
    # 用itsdangerous加密，导入为tjss
    key = tjss(settings.SECRET_KEY, 3600)
    # 需要加密的信息
    info = {'confirm': ID}
    # 已经加密的信息
    tokenBytes = key.dumps(info)
    token = tokenBytes.decode()
    # url地址
    site = settings.SITE_HOST
    path = reverse('main:activity')
    # 发邮件
    # 主题
    subject = '遇见，昌航有物'
    # 正文
    message = ''
    # 发件人
    sender = settings.EMAIL_HOST_USER
    # 收件人列表
    receiver = [Email]

    url = '{site}{path}/{token}/'.format(site=site, path=path, token=token)

    html = '''<h3>昌航有物</h3><br> 
              <h3>尊敬的的{user}：</h3><br>
              <h1>请点击如下链接进行激活-->>></h1><br>
              <a href="{url}" >
              ----------点我进行邮箱验证----------》</a>
              再次感谢您！<br />
              <h3>如果上面链接无法打开，请将此链接复制至浏览器。</h3>
              {url}
              <br><br><br>
              '''.format(user=User, url=url)

    if send_mail(subject, message, sender, receiver, html_message=html, fail_silently=False):
        return 1
    else:
        return 0