from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

is_on_sale_choices = (
    (False, "下架"),
    (True, "上架"),
)


# Create your models here.

class Commodity(models.Model):
    """商品分类模型"""

    classification_name = models.CharField(max_length=50,
                                           verbose_name="分类名", )

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.classification_name

    class Meta:
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name


class Goods_spu(models.Model):
    """商品spu表"""
    spu_name = models.CharField(max_length=50,
                                verbose_name="商品spu名")

    content = RichTextUploadingField(verbose_name="商品详情")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = "商品spu名"
        verbose_name_plural = verbose_name


class Unit(models.Model):
    """商品单位表"""
    unit_name = models.CharField(max_length=20,
                                 verbose_name="商品单位")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.unit_name

    class Meta:
        verbose_name = "商品单位"
        verbose_name_plural = verbose_name


class Activity(models.Model):
    """首页活动专区"""
    title = models.CharField(max_length=100,
                             verbose_name="首页活动名称")
    picture_address = models.ImageField(upload_to="activity/%Y%m/%d",
                                        verbose_name="图片地址")

    url_site = models.URLField(verbose_name='活动的url地址',
                               max_length=200)

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name


class Goods_sku(models.Model):
    """商品sku表"""
    trade_name = models.CharField(max_length=100,
                                  verbose_name="商品sku名")
    breif = models.CharField(max_length=200,
                             null=True,
                             blank=True,
                             verbose_name="商品简介")
    price = models.DecimalField(max_digits=9,
                                decimal_places=2,
                                verbose_name="商品价格",
                                default=0)

    stock = models.IntegerField(verbose_name="商品库存",
                                default=0)

    sales = models.IntegerField(default=0,
                                verbose_name="商品销量")

    logo = models.ImageField(upload_to='goods/%Y%m/%d',
                             verbose_name="封面图片")

    is_shelf = models.BooleanField(verbose_name="是否上架",
                                   choices=is_on_sale_choices,
                                   default=False)

    unit = models.ForeignKey(to="Unit",
                             verbose_name="单位")
    commodity = models.ForeignKey(to="Commodity",
                                  verbose_name="商品分类")
    goods_spu = models.ForeignKey(to="Goods_spu",
                                  verbose_name="商品spu")
    activity = models.ForeignKey(to="Activity",
                                 verbose_name="活动分类")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.trade_name

    class Meta:
        verbose_name = "商品sku管理"
        verbose_name_plural = verbose_name


class Album(models.Model):
    """商品相册管理"""
    picture_address = models.ImageField(upload_to="goods_pictures/%Y%m/%d",
                                        verbose_name="商品图片地址")
    goods_sku = models.ForeignKey(to="Goods_sku",
                                  verbose_name="商品sku")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return "商品相册:{}".format(self.picture_address.name)

    class Meta:
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name


class Wheel_planting(models.Model):
    """轮播图片管理"""
    name = models.CharField(max_length=50,
                            verbose_name="轮播活动名称")

    picture_address = models.ImageField(verbose_name='轮播图片地址',
                                        upload_to='banner/%Y%m/%d')

    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0, )

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "轮播图片管理"
        verbose_name_plural = verbose_name


class ActivityZone(models.Model):
    """
        首页特色专区
    """
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    brief = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )
    is_on_sale = models.BooleanField(verbose_name="是否上线",
                                     choices=is_on_sale_choices,
                                     default=0,
                                     )
    goods_sku = models.ManyToManyField(to="Goods_sku", verbose_name="商品")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "特色专区管理"
        verbose_name_plural = verbose_name
