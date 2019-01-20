from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from db.base_view import VerifyLoginView
from user.forms import RegisterModelForm, LoginModelForm
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
    # @method_decorator(check_login)
    def get(self, request):
        return render(request, 'user/member.html')

    # @method_decorator(check_login)
    def post(self, request):
        pass

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
