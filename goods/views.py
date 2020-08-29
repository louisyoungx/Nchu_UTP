import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from Nchu_UTP.settings import SITE_URL, DEBUG
from goods.models import Goods,GoodsImg
from utils.Mixin import LoginMixin

# Create your views here.


# 分类主页面
class ListView(View):
    """分类主页面"""
    def get(self, request, classify):
        context={
            'classify':classify
        }
        return render(request, 'goods-classify.html', context=context)

class AddListView(View):
    """返回商品列表"""
    def get(self, request):
        """处理GET请求业务逻辑"""
        # 通过django的view实现商品列表页
        classify = request.GET.get('classify')
        print(classify)
        json_list = []
        # 获取所有商品
        goods = Goods.objects.filter(classify=classify)[:50]
        if len(goods)==0:
            return JsonResponse({'status':0})
        for good in goods:
            i = 1
            json_dict = {}
            # 获取商品的每个字段，键值对形式

            json_dict['title'] = good.name
            json_dict['price'] = good.price
            json_dict['place'] = good.place

            # 合成地址页面
            href = SITE_URL + "goods-detail/" + str(good.id)
            json_dict['id'] = href

            #查询所有图片
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
    def get(self, request, good_id):
        context={
            'id':good_id,
        }
        return render(request, 'goods-detail.html', context=context)

class InfoView(View):
    '''商品详情页'''
    def get(self, request):
        good_id = request.GET.get('id')
        good = Goods.objects.get(id=good_id)
        seller = good.user
        goodNum = len(seller.Goods.all())
        queryset = seller.Info.all()
        for li in queryset:
            info = li
        nickname = info.nickname
        try:
            head = info.head_img
            avatar = SITE_URL + "media/" + str(head)
        except:
            avatar = "image/mine/head.png"

        i = 1
        json_dict = {}
        # 获取商品的每个字段，键值对形式
        json_dict['seller'] = nickname
        json_dict['avatar'] = avatar
        json_dict['num'] = goodNum
        json_dict['title'] = good.name
        json_dict['price'] = good.price
        json_dict['intro'] = good.intro
        json_dict['place'] = good.place
        json_dict['classify'] = good.classify
        json_dict['like_num'] = good.like_num
        json_dict['click_num'] = good.click_num

        # 查询所有图片
        ImgList = good.Img.all()
        for img in ImgList:
            index = 'pic' + str(i)
            url = SITE_URL + "media/" + str(img.image)
            json_dict[index] = str(url)
            i = i + 1
        # 将获取到的数据返回到 json中
        # 返回json，一定要指定类型content_type='application/json'
        return JsonResponse(json_dict, safe=False)

# 商品发布页面
class ReleaseView(LoginMixin, View):
    """商品发布页面"""
    def get(self, request):
        return render(request, 'goods-release.html')
    def post(self, request):
        user = request.user
        classify = request.POST.get("classify")
        name = request.POST.get("name")
        price = request.POST.get("price")
        intro = request.POST.get("intro")
        place = request.POST.get("place")
        sub = request.POST.get("sub-done")
        avatar = request.FILES.get('avatar')
        pic2 = request.FILES.get('pic2')
        pic3 = request.FILES.get('pic3')
        if intro == '':
            intro = '没有留下任何信息'
        if place == '':
            place = '图书馆大门口'
        if not all([classify, name, price]):
            return HttpResponse('error')
        else:
            if DEBUG == True:
                print(classify, name, price)
            good = Goods.objects.create(user=user, name=name, price=price, intro=intro, place=place,surface=avatar, classify=classify)
            image1 = GoodsImg(goods=good, hash='test', image=avatar, index=1)
            image1.save()
            print(pic3)
            if pic2 == None:
                pass
            else:
                image2 = GoodsImg(goods=good, hash='test', image=pic2, index=2)
                image2.save()
            if pic3 == None:
                pass
            else:
                image3 = GoodsImg(goods=good, hash='test', image=pic3, index=3)
                image3.save()
            good.save()
            if sub == '发布':
                return redirect(reverse('main:mine'))
            elif sub =='保存并继续编辑':
                return HttpResponse(request)
            else:
                return redirect(reverse('goods:release'))
        pass