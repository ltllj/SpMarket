from django.conf.urls import url

from carts.views import AddCartView, ListCartView

urlpatterns= [
    url(r'^add/$',AddCartView.as_view(),name='添加购物车'),
    url(r'^shopcart/$',ListCartView.as_view(),name='购物车列表页面'),

]