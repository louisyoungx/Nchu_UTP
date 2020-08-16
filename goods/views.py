from django.shortcuts import render
from django.views import View

# Create your views here.

# 分类主页面
class ListView(View):
    """分类主页面"""
    def get(self, request, classify):
        """处理GET请求业务逻辑"""
        if classify == 'sjsm':
            return render(request, 'goods-classify.html')
        return render(request, 'goods-classify.html')

# 商品详情页
class DetailView(View):
    '''商品详情页'''
    def get(self, request):
        pass