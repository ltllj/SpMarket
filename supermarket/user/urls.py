from django.conf.urls import url

from user.views import LoginView, RegisterView

urlpatterns = [
    url(r'^login/$',LoginView.as_view(),name='登录'),
    url(r'^register/$',RegisterView.as_view(),name='注册'),
]