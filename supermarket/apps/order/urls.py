from django.conf.urls import url

from order.views import ConfirmOrderView, ConfirmPayView

urlpatterns = [
    url(r'^confirm/$',ConfirmOrderView.as_view(),name="确认订单"),
    url(r'^order/$',ConfirmPayView.as_view(),name="确认支付"),
]