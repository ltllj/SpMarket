from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm, LoginModelForm
from user.helper import set_password
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
            user = form.cleaned_data['user']

            request.session['ID'] = user.pk
            request.session['phone'] = user.phone
            request.session.set_expiry(0)  # 关闭浏览器就没有

            # 操作数据库
            return redirect('item:首页')

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
