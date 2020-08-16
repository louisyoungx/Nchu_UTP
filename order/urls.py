from django.urls import path, re_path
from order import views
from order.views import ListView, InfoView, ComfrimView

app_name = 'order'

urlpatterns = [
    path('-list/', ListView.as_view(),name='list'),
    path('-info/', InfoView.as_view(),name='info'),
    path('-comfirm/', ComfrimView.as_view(),name='info'),
]
