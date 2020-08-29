from django.urls import path, re_path
from goods import views
from goods.views import ListView, AddListView, ReleaseView, DetailView, InfoView

app_name = 'goods'

urlpatterns = [
    path('/classify/<classify>/', ListView.as_view(), name='classify'),
    path('-add/', AddListView.as_view(), name='addgoods'),
    path('-release/', ReleaseView.as_view(), name='release'),
    path('-info/', InfoView.as_view(), name='info'),
    path('-detail/<good_id>', DetailView.as_view(), name='detail'),
]
