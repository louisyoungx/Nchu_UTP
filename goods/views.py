import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from Nchu_UTP.settings import SITE_URL
from goods.models import Goods,GoodsImg

# Create your views here.

# 分类主页面



class ListView(View):
    """分类主页面"""
    def get(self, request, classify):
        return render(request, 'goods-classify.html')

class AddListView(View):
    """返回商品列表"""
    def get(self, request):
        """处理GET请求业务逻辑"""
        # 通过django的view实现商品列表页
        json_list = []
        # 获取所有商品
        goods = Goods.objects.all()[:3]
        for good in goods:
            i = 1
            json_dict = {}
            # 获取商品的每个字段，键值对形式
            json_dict['title'] = good.name
            json_dict['price'] = good.price
            json_dict['place'] = good.place
            ImgList = good.Img.all()
            for img in ImgList:
                index = 'pic'+str(i)
                url = SITE_URL + "media/" + str(img.image)
                json_dict[index] = str(url)
                i=i+1
            json_list.append(json_dict)
        # 将获取到的数据返回到 json中
        # 返回json，一定要指定类型content_type='application/json'
        return JsonResponse(json_list, safe=False)
        # return render(request, 'goods-classify.html', context=json_list)

# 商品详情页
class DetailView(View):
    '''商品详情页'''
    def get(self, request):
        pass