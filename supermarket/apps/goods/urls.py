from django.conf.urls import url

from goods.views import IndexView, DetailView, CategoryView

urlpatterns = [
    url(r'^index/$',IndexView.as_view(),name='商城首页'),
    url(r'^category/$',CategoryView.as_view(),name='商品目录'),
    url(r'^detail/(?P<id>\d+)/$',DetailView.as_view(),name='商品详情'),
]