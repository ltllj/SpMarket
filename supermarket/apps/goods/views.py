from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import Goods_sku, Album, Commodity


class IndexView(View):

    """首页视图"""
    def get(self,request):
        return render(request, 'goods/index.html')

    def post(self,request):
        pass


class CategoryView(View):
    """商品目录视图"""
    def get(self,request):
        # 查询所有的分类
        commodities = Commodity.objects.filter(is_delete=False)
        # 查询所有的商品信息
        good_sku = Goods_sku.objects.filter(is_delete=False)
        # 渲染到模板
        context = {
            'commodities':commodities,
            'good_sku':good_sku,
        }
        return render(request, 'goods/category.html',context=context)

    def post(self,request):
        pass


class DetailView(View):
    """商品详情视图"""

    def get(self, request, id):
        # 获取商品sku的信息
        goods_sku = Goods_sku.objects.get(pk=id)
        # urls = Album.objects.filter(goods_sku_id=id)
        # 渲染给页面
        context = {
            'goods_sku':goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)

    def post(self, request):
        pass
