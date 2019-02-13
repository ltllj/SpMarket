from django.conf.urls import url

from goods.views import IndexView, DetailView, CategoryView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='商城首页'),
    url(r'^category/(?P<com_id>\d*)_{1}(?P<order>\d?)\.html$', CategoryView.as_view(), name='商品目录'),
    url(r'^detail/(?P<id>\d+)/$', DetailView.as_view(), name='商品详情'),
]

# * 匹配零到多个
# . 匹配所有
