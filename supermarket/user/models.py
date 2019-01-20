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
                                    MinLengthValidator(2, '用户名至少两位')
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

    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "users"




