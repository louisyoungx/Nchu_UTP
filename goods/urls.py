from django.urls import path, re_path
from goods import views
from goods.views import ListView, AddListView

app_name = 'goods'

urlpatterns = [
    path('/classify/<classify>/', ListView.as_view(), name='classify'),
    path('-add/', AddListView.as_view(), name='addgoods'),
]
