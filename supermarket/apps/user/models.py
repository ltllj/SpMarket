from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


# Create your models here.


class Users(models.Model):  # 创建用户表

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )

    phone = models.CharField(max_length=11,
                             validators=[
                                 RegexValidator(r'^1[3-9]\d{9}$',"手机号码格式错误")
                             ])
    password = models.CharField(max_length=32,
                                validators=[
                                    MinLengthValidator(8, '密码最小长度为8位')
                                ])

    nickname = models.CharField(max_length=20,
                                null=True,
                                blank=True,
                                validators=[
                                    MinLengthValidator(2, '昵称至少两位')
                                ])

    gender = models.SmallIntegerField(choices=gender_choices, default=1)

    school = models.CharField(max_length=100,
                              null=True,
                              blank=True,
                              )

    position = models.CharField(max_length=100,
                                null=True,
                                blank=True,
                                )

    Hometown = models.CharField(max_length=100,
                                null=True,
                                blank=True,
                                )

    birth_of_date = models.DateField(null=True,
                                     blank=True,
                                     )
    # 设置头像字段
    head = models.ImageField(upload_to='shop/%Y%m/%d', default='head/qqlogin.png')

    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "users"


class UserAddress(models.Model):
    """用户收货地址管理"""
    user = models.ForeignKey(to="Users", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话",
                             max_length=11,
                             validators=[
                                 RegexValidator('^1[3-9]\d{9}$', '电话号码格式错误')
                             ])
    hcity = models.CharField(verbose_name="省", max_length=100, blank=True, null=True)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, null=True)
    harea = models.CharField(verbose_name="区", max_length=100)
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}:{}".format(self.username,self.phone)

