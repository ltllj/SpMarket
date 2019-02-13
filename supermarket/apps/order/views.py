from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django_redis import get_redis_connection

from carts.helper import json_msg
from db.base_view import VerifyLoginView
from goods.models import Goods_sku
from order.models import Transport, Order, OrderGoods
from user.models import UserAddress, Users
from datetime import datetime
import random


class ConfirmOrderView(VerifyLoginView):
    """确认订单页面"""

    def get(self, request):
        # 1. 如果没有收货地址,就显示添加收货地址
        # 如果有收货地址就显示默认收货地址,如果没有默认就显示第一个

        # 获取session中的用户id
        user_id = request.session.get('ID')

        # >>>>>收货地址处理
        address = UserAddress.objects.filter(user_id=user_id).order_by("-isDefault").first()

        # 2. 展示商品信息,获取多个商品信息,并且根据商品sku_ids获取购物车redis中的数量
        sku_ids = request.GET.getlist('sku_ids')
        # 准备一个空列表,存放遍历出的商品
        goods_skus = []
        # 准备商品总价格
        goods_total_price = 0
        # 准备redis
        r = get_redis_connection()
        # 准备键
        cart_key = f'cart_{user_id}'

        # 得到一个id列表,所以进行遍历取出每一个sku_id
        for sku_id in sku_ids:
            # 得到商品信息
            try:
                goods_sku = Goods_sku.objects.get(pk=sku_id)
            except Goods_sku.DoesNotExist:
                # 商品不存在就回到购物车
                return redirect("carts:购物车列表页面")
            # 获取对应商品的数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                # 商品不存在就回到购物车
                return redirect("carts:购物车列表页面")
            # 将count保存到商品对象上
            goods_sku.count = count

            # 存放商品
            goods_skus.append(goods_sku)

            # 统计商品总价格
            goods_total_price += goods_sku.price * count

        # 获取运输方式
        transports = Transport.objects.filter(is_delete=False).order_by("price")

        # 渲染数据到模板
        context = {
            'address': address,
            'goods_skus': goods_skus,
            'goods_total_price': goods_total_price,
            'transports': transports,
        }

        return render(request, 'order/tureorder.html', context=context)

    def post(self, request):
        """
            保存订单数据
            1.订单基本信息表和订单商品表
        """
        # 1.接收参数
        transport_id = request.POST.get('transport')
        sku_ids = request.POST.getlist('sku_ids')
        address_id = request.POST.get('address')

        # 接收用户的id
        user_id = request.session.get("ID")
        user = Users.objects.get(pk=user_id)

        # 验证数据的合法性
        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(2, "参数错误"))

        # 验证收货地址和运输方式存在
        try:
            address = UserAddress.objects.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在!"))

        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在!"))

        # 2.操作数据

        # >>>>操作订单基本信息表
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{} {}".format(address.hcity, address.hproper, address.harea, address.brief)
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            transport_price=transport.price,
            transport=transport.name,
            username=address.username,
            phone=address.phone,
            address=address_info
        )

        # >>>>操作订单商品表
        # 操作redis
        r = get_redis_connection()
        cart_key = f'cart_{user_id}'

        # 准备个变量保存商品总金额
        goods_total_price = 0
        for sku_id in sku_ids:
            # 获取商品对象
            try:
                goods_sku = Goods_sku.objects.get(pk=sku_id, is_delete=False, is_shelf=True)
            except Goods_sku.DoesNotExist:
                return JsonResponse(json_msg(5, "商品不存在"))

            # 获取购物车中商品的数量
            # redis 基于内存的存储,有可能数据会丢失
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                return JsonResponse(json_msg(6, "购物车中数量不存在!"))

            # 判断库存是否足够
            if goods_sku.stock < count:
                return JsonResponse(json_msg(7, "库存不足!"))

            # 保存订单商品表
            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count,
            )

            # 添加商品总金额
            goods_total_price += goods_sku.price * count

            # 扣除库存, 同时销量增加
            goods_sku.stock -= count
            goods_sku.sales += count
            goods_sku.save()

        # >>>>再操作订单基本信息表(商品总金额和订单总金额)
        order_price = goods_total_price + transport.price
        order.goods_total_price = goods_total_price
        order.order_price = order_price
        order.save()

        # >>>> 清空redis中对应sku_id的购物车数据
        r.hdel(cart_key, *sku_ids)

        # 3.合成响应
        return JsonResponse(json_msg(0, "创建订单成功", data=order_sn))


class ConfirmPayView(VerifyLoginView):
    """确认支付页面"""

    def get(self, request):
        # 1.获取用户收货地址
        # 获取session中的用户id
        user_id = request.session.get('ID')
        # >>>>>收货地址处理
        order = Order.objects.filter(user_id=user_id)

        # 2. 获取数据库中的商品信息,获取多个商品信息,并且根据商品sku_ids获取购物车redis中的数量

        context = {
            'order': order,
        }

        return render(request, 'order/order.html', context=context)

    def post(self, request):
        pass
