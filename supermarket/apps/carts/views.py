from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from carts.helper import json_msg, get_cart_count
from db.base_view import VerifyLoginView
from goods.models import Goods_sku
from django_redis import get_redis_connection


class AddCartView(VerifyLoginView):
    """操作购物车,实现购物车的添加"""
    """
        1.需要接受的参数.
            sku_id  count
            从session中获取用户的user_id
        2.验证参数合法性
            a.判断参数为整数
            b.验证数据库总存在商品
            c.验证库存是否充足
        3.操作数据
            将购物车保存到redis
            存储的时候才用数据类型为hash
             key       field     value field value
             cart_user_id sku_id count
    """

    def post(self, request):
        # 1.接收参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get("count")

        # a.判断参数为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误"))
        # b.验证数据库总存在商品
        try:
            goods_sku = Goods_sku.objects.get(pk=sku_id)
        except Goods_sku.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在"))
        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足"))

        # 2.操作数据
        # 创建连接
        connect = get_redis_connection()
        # 处理购物车的key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取购物车中已经存在的数量,加上需要添加的库存进行比较
        old_count = connect.hget(cart_key, sku_id)  # 获取出来是二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足"))
        # 将商品添加到购物车
        # connect.hset(cart_key,sku_id,old_count + count)
        res = connect.hincrby(cart_key, sku_id, count)
        if res <= 0:
            connect.hdel(cart_key, sku_id)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3.合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))


class ListCartView(VerifyLoginView):

    def get(self, request):
        # 获取用户ID
        user_id = request.session.get('ID')
        # 得到redis连接
        r = get_redis_connection()
        # 准备键
        cart_key = f'cart_{user_id}'
        # 得到字典形式的商品ID和商品数量
        datas = r.hgetall(cart_key)
        # 准备一个列表
        goods_skus = []
        # 遍历字典
        for sku_id,count in datas.items():
            # 将二进制数据转换成成整数
            sku_id = int(sku_id)
            count = int(count)
            # 根据sku_id获取商品信息
            try:
                goods_sku = Goods_sku.objects.get(pk=sku_id,is_delete=False)
            except Goods_sku.DoesNotExist:
                # 删除redis中过期的数据
                r.hdel(cart_key,sku_id)
                continue
            # 将购物车的数量与商品信息合成在一起(给对象添加属性)
            setattr(goods_sku,'count',count)
            # 保存商品到商品列表
            goods_skus.append(goods_sku)

        # 渲染数据到模板
        context = {
            'goods_skus':goods_skus
        }
        return render(request, 'carts/shopcart.html',context=context)

    def post(self, request):
        # 1.接收参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get("count")

        # a.判断参数为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误"))
        # b.验证数据库总存在商品
        try:
            goods_sku = Goods_sku.objects.get(pk=sku_id)
        except Goods_sku.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在"))
        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足"))

        # 2.操作数据
        # 创建连接
        connect = get_redis_connection()
        # 处理购物车的key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取购物车中已经存在的数量,加上需要添加的库存进行比较
        old_count = connect.hget(cart_key, sku_id)  # 获取出来是二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足"))
        # 将商品添加到购物车
        # connect.hset(cart_key,sku_id,old_count + count)
        connect.hincrby(cart_key, sku_id, count)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3.合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))


class DetailCartView(VerifyLoginView):
    def post(self, request):
        # 1.接收参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get("count")

        # a.判断参数为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, "参数错误"))
        # b.验证数据库总存在商品
        try:
            goods_sku = Goods_sku.objects.get(pk=sku_id)
        except Goods_sku.DoesNotExist:
            return JsonResponse(json_msg(2, "商品不存在"))
        # 判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, "库存不足"))

        # 2.操作数据
        # 创建连接
        connect = get_redis_connection()
        # 处理购物车的key
        cart_key = f"cart_{user_id}"

        # 添加
        # 获取购物车中已经存在的数量,加上需要添加的库存进行比较
        old_count = connect.hget(cart_key, sku_id)  # 获取出来是二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)
        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, "库存不足"))
        # 将商品添加到购物车
        # connect.hset(cart_key,sku_id,old_count + count)
        connect.hincrby(cart_key, sku_id, count)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)

        # 3.合成响应
        return JsonResponse(json_msg(0, "添加购物车成功", data=cart_count))
