from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm, ForgetModelForm, InforModelForm
from user.helper import set_password, login, check_login
from user.models import Users


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


class InforView(View):

    def get(self, request):
        # 返回个人资料页面
        return render(request, 'user/infor.html')

    def post(self, request):
        # 接受参数
        data = request.POST
        # 通过表单验证参数是否合法
        form = InforModelForm(data)
        if form.is_valid():
            # 从数据库中获取用户手机号
            phone = Users.objects.get('phone')
            # 获取用户填写的信息
            nickname = form.cleaned_data['nickname']
            gender = form.cleaned_data['gender']
            birth_of_date = form.cleaned_data['birth_of_date']
            school = form.cleaned_data['school']
            possion = form.cleaned_data['possion']
            Hometown = form.cleaned_data['Hometown']
            # 更新对应用户的信息
            Users.objects.filter(phone=phone).update(nickname=nickname,
                                                     gender=gender,
                                                     birth_of_date=birth_of_date,
                                                     school=school,
                                                     possion=possion,
                                                     Hometown=Hometown,)
            return redirect('user:个人资料')
        else:
            # 错误
            return render(request,'user/infor.html',context={'form':form})