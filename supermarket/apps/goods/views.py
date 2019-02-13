from django.shortcuts import render

# Create your views here.
from django.views import View

from carts.helper import get_cart_count
from goods.models import Goods_sku, Album, Commodity, Wheel_planting, ActivityZone


class IndexView(View):
    """首页视图"""

    def get(self, request):
        wheel_planting = Wheel_planting.objects.all()
        activityzone = ActivityZone.objects.all()
        context = {
            'wheel_planting': wheel_planting,
            'activityzone': activityzone,
        }
        return render(request, 'goods/index.html', context=context)

    def post(self, request):
        pass


class CategoryView(View):
    """商品目录视图"""

    # 1.页面刚加载的时候  加载默认的排第一分类下的商品
    # 2.点击哪个分类,就显示对应分类下的商品
    # 3.可以按照综合(pk),销量(降序),价格(降序和升序),发布时间进行排序(并且是对应分类下的商品排序)
    #     添加一个参数order
    #         0:综合排序
    #         1:销量降序
    #         2:价格升序
    #         3:价格降序
    #         4.添加时间降序
    # order_rule = ['pk', '-sales', 'price', '-price', '-add_time']

    def get(self, request, com_id, order):
        # 查询所有的分类
        commodities = Commodity.objects.filter(is_delete=False)

        # 如果没有传就取出第一个分类
        if com_id == "":
            commodity = commodities.first()  # 或者commodity = commodities.[0]
            com_id = commodity.pk
        # 如果传了,就取出对应com_id的分类
        else:
            com_id = int(com_id)
            commodity = Commodity.objects.get(pk=com_id)

        # 再查询对应类下的所有商品信息
        goods_sku = Goods_sku.objects.filter(is_delete=False, commodity=commodity)

        if order == "":
            order = 0
        order = int(order)

        # 排序规则列表
        order_rule = ['pk', '-sales', 'price', '-price', '-add_time']
        goods_sku = goods_sku.order_by(order_rule[order])
        # if order == 0:
        #     goods_sku = goods_sku.order_by("pk")
        # elif order == 1:
        #     goods_sku = goods_sku.order_by("-sale_num")
        # elif order == 2:
        #     goods_sku = goods_sku.order_by("price")
        # elif order == 3:
        #     goods_sku = goods_sku.order_by("-price")
        # elif order == 4:
        #     goods_sku = goods_sku.order_by("-create_time")

        # 获取当前用户购物车中商品的总数量
        cart_count = get_cart_count(request)


        # 渲染到模板
        context = {
            'commodities': commodities,
            'goods_sku': goods_sku,
            'com_id': com_id,
            'order': order,
            'cart_count':cart_count,
        }
        return render(request, 'goods/category.html', context=context)


class DetailView(View):
    """商品详情视图"""

    def get(self, request, id):
        # 获取商品sku的信息
        goods_sku = Goods_sku.objects.get(pk=id)
        # urls = Album.objects.filter(goods_sku_id=id)
        # 渲染给页面
        context = {
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)

    def post(self, request):
        pass
