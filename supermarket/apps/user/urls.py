from django.conf.urls import url

from user.views import LoginView, RegisterView, MemberView, ForgetView, InforView, SendcallsView

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),name='登录'),
    url(r'^register/$',RegisterView.as_view(),name='注册'),
    url(r'^member/$',MemberView.as_view(), name='个人中心'),
    url(r'^forget/$',ForgetView.as_view(), name='修改密码'),
    url(r'^infor/$',InforView.as_view(), name='个人资料'),
    url(r'^sendcalls/$',SendcallsView.as_view(), name='发送短信验证码'),
]