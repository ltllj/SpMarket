from django.utils.decorators import method_decorator
from django.views import View

from user.helper import check_login


class VerifyLoginView(View):
    """基础验证是否登录的视图,哪些视图登陆后才能看到就需要继承这个类"""

    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)