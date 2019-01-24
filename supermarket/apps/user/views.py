import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetModelForm, InforForm
from user.helper import set_password, login, check_login, send_sms
from user.models import Users
from django_redis import get_redis_connection


class LoginView(View):
    """登录视图"""

    def get(self, request):
        # 展示登录表单
        return render(request, 'user/login.html')

    def post(self, request):
        # 接受参数
        data = request.POST
        # 验证数据是否合法

        form = LoginModelForm(data)

        if form.is_valid():
            # 验证成功
            # 操作数据库
            # 保存登录标识到session中, 单独创建一个方法保存, 更新个人资料
            user = form.cleaned_data['user']

            # request.session['ID'] = user.pk
            # request.session['phone'] = user.phone
            # # request.session['head'] = user.head
            # request.session.set_expiry(0)  # 关闭浏览器就没有

            login(request, user)
            # 合成响应 跳转到个人中心
            return redirect('user:个人中心')


        else:
            # 合成响应
            return render(request, 'user/login.html', {'form': form})


class RegisterView(View):
    """注册视图"""

    def get(self, request):
        # 展示注册表单
        return render(request, 'user/reg.html')

    def post(self, request):
        # 接受参数
        data = request.POST
        # 验证参数的合法性 表单进行验证
        form = RegisterModelForm(data)
        if form.is_valid():
            # 操作数据库
            cleaned_data = form.cleaned_data
            # 通过模型类实例一个对象 完成用户的添加
            user = Users()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            return redirect('user:登录')

        else:
            # 错误
            return render(request, 'user/reg.html', context={'form': form})


class MemberView(VerifyLoginView):
    # 个人中心

    def get(self, request):
        return render(request, 'user/member.html')

    def post(self, request):
        pass

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ForgetView(View):
    """忘记密码"""

    def get(self, request):
        # 展示注册表单
        return render(request, 'user/forgetpassword.html')

    def post(self, request):
        # 接受参数
        data = request.POST
        # 通过表单验证参数是否合法
        forget_form = ForgetModelForm(data)
        if forget_form.is_valid():
            # 获取用户填写的手机号和密码
            phone = forget_form.cleaned_data['phone']
            password = forget_form.cleaned_data['password']
            # 哈希加密
            password = set_password(password)
            # 查找出对应的手机号并对数据进行更新
            Users.objects.filter(phone=phone).update(password=password)
            # 跳转到登陆页面
            return redirect('user:登录')

        else:
            # 错误
            return render(request, 'user/forgetpassword.html', context={'forget_form': forget_form})


class InforView(VerifyLoginView):

    def get(self, request):
        # 返回个人资料页面
        # 在sesion中获取用户的ID
        user_id = request.session.get('ID')
        user = Users.objects.get(pk=user_id)
        # 将用户信息渲染到页面
        context = {
            "user": user
        }
        return render(request, 'user/infor.html', context=context)

    def post(self, request):
        # 接受参数
        data = request.POST
        # 通过表单验证参数是否合法
        form = InforForm(data)
        if form.is_valid():
            head = request.FILES.get('head')
            # 从session中获取用户id
            user_id = request.session.get('ID')
            # 获取用户填写的信息
            user = Users.objects.get(pk=user_id)
            user.nickname = form.cleaned_data['nickname']
            gender = data.get('gender')
            birth_of_date = data.get('birth_of_date')
            school = data.get('school')
            position = data.get('position')
            Hometown = data.get('Hometown')

            # 更新对应用户的信息
            Users.objects.filter(pk=user_id).update(gender=gender,
                                                    birth_of_date=birth_of_date,
                                                    school=school,
                                                    position=position,
                                                    Hometown=Hometown, )

            if head is not None:
                user.head = head
            user.save()
            # 同时修改session
            login(request, user)
            return redirect('user:个人资料')
        else:
            # 错误
            return render(request, 'user/infor.html', context={'form': form})


class SendcallsView(View):
    """接收ajax请求,操作后端服务器,发送短信验证码"""

    def get(self, request):
        pass

    def post(self, request):
        # 一.接受参数
        phone = request.POST.get('phone', '')
        # 对接受的电话号码进行正则验证
        res = re.search('^1[3-9]\d{9}$', phone)
        # 判断参数合法性
        if res is None:
            return JsonResponse({'error': 1, 'error_message': '电话号码格式错误'})
        # 二.操作数据

        # 先模拟,最后接入运营商
        # 1.模拟时需要自己先生成随机的验证码
        # 2.保存验证码到redis中(好处:存储读取速度快,减轻服务器压力,并且可以设置过期时间)
        # 3.最后接入运营商

        # =====> 1.生成随机验证码(字符串)
        list = [str(random.randint(0, 9)) for _ in range(6)]  # 这里是列表,需要转化成字符串
        auth_code = "".join(list)
        print(">>>>>>随机验证码:{}<<<<<<".format(auth_code))

        # =====>2.保存验证码到redis中
        connect = get_redis_connection()
        # 保存手机号对应的验证码
        connect.set(phone, auth_code)
        # 设置60秒后过期
        connect.expire(phone, 60)
        # 获取当前手机号获取验证码的次数
        phone_times = "{}_times".format(phone)
        now_times = connect.get(phone_times)
        if now_times is None or int(now_times) < 5:
            # 保存手机发送验证码的次数,最多6次
            connect.incr(phone_times)
            # 设置一个过期时间,一个小时候再发送
            connect.expire(phone_times, 3600)
        else:
            # 返回用户发送次数过多
            return JsonResponse({"error": 1, "error_message": "发送验证码次数过多"})

        # >>>3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"猪罗大型商城超市\"}" % auth_code
        # print(params)
        rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 三.合成响应
        return JsonResponse({'error': 0})
