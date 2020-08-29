from django.urls import path, re_path
from main import views
from main.views import HomeView, ClassView, MineView, CartView, IndexView, ActiveView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('classification', ClassView.as_view(), name='class'),
    path('mine/', MineView.as_view(), name='mine'),
    path('cart/', CartView.as_view(), name='cart'),
    path('index/', IndexView.as_view(), name='index'),
    path('active/<token>/', ActiveView.as_view(), name='active'),
    path('active', ActiveView.as_view(), name='activity'),
    path('404', views.notFound404, name='404'),
    path('set_cookie', views.set_cookie, name='cookie'),
    path('test/', views.test, name='test'),

]
