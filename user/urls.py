from django.urls import path, re_path
from user import views
from user.views import PageView, InfoView, SettingView, FavorView

app_name = 'user'

urlpatterns = [
    path('/<username>/', PageView.as_view(),    name='page'),
    path('',             PageView.as_view(),    name='page'),
    path('-info/',       InfoView.as_view(),    name='info'),
    path('-favorite/',    FavorView.as_view(),   name='favor'),
    path('-setting/',    SettingView.as_view(), name='setting'),
    path('-avatar/',    views.avatar, name='avatar'),


]
