from django import forms

from user.helper import set_password
from user.models import Users
from django_redis import get_redis_connection

class RegisterModelForm(forms.ModelForm):
    """注册表单模型类"""

    # 单独定义一个字段
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '密码必须填写',
                                   'min_length': '密码最小长度至少8位',
                                   'max_length': '密码最大长度最多16位',
                               })

    repassword = forms.CharField(max_length=16,
                                 min_length=8,
                                 error_messages={
                                     'required': '密码必须填写',
                                     'min_length': '密码最小长度至少8位',
                                     'max_length': '密码最大长度最多16位',
                                 })
    # 验证码验证
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': '验证码必须填写',
                              })

    agree = forms.BooleanField(error_messages={
                                    'required': '必须同意用户协议'
                              })

    class Meta:
        model = Users
        fields = ['phone', ]

        error_messages = {
            "phone": {
                'required': '手机号码必须填写',
            }
        }

    # 验证手机号是否在数据库中存在
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        flag = Users.objects.filter(phone=phone).exists()
        if flag:
            # 存在  则错误  不能注册  抛出异常
            raise forms.ValidationError('该手机号已注册')
        else:  # 返回清洗后的数据
            return phone

    # 验证两次密码是否一致
    def clean(self):
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            # 抛出异常
            raise forms.ValidationError({'repassword': '两次密码不一致'})

        # 验证用户填写的验证码与redis中验证码是否一样
        try:
            captcha = self.cleaned_data.get('captcha')
            phone = self.cleaned_data.get('phone','')
            # 获取redis中的验证码
            res = get_redis_connection()
            auth_code = res.get(phone)
            auth_code = auth_code.decode('utf-8')

            # 比对
            if captcha and captcha != auth_code:
                raise forms.ValidationError({"captcha":"验证码输入错误"})
        except:
            raise forms.ValidationError({"captcha":"验证码输入错误"})



        # 返回所有清洗后的数据
        return self.cleaned_data











class LoginModelForm(forms.ModelForm):
    """注册表单模型类"""

    # 验证密码单独定义一个字段
    class Meta:
        model = Users
        fields = ['phone','password']


        error_messages = {
            "phone":{
                'required':'必须填写',
            },
            'password':{
                'required':'请填写密码',
            }
        }

    def clean(self):
        # 验证手机号是否在数据库中

        phone = self.cleaned_data.get('phone')
        # 查询数据库
        # 验证手机号
        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            raise forms.ValidationError({'phone':'手机号错误'})

        # 验证密码
        password = self.cleaned_data.get('password')
        # 查寻数据库
        if user.password != set_password(password):
            raise forms.ValidationError({'password':'密码错误'})

        # 返回所有清洗后的数据

        self.cleaned_data['user'] = user

        return self.cleaned_data


class ForgetModelForm(forms.ModelForm):
    """注册表单模型类"""

    # 单独定义一个字段
    password = forms.CharField(max_length=16,
                               min_length=8,
                               error_messages={
                                   'required': '密码必须填写',
                                   'min_length': '密码最小长度至少8位',
                                   'max_length': '密码最大长度最多16位',
                               })

    repassword = forms.CharField(max_length=16,
                                 min_length=8,
                                 error_messages={
                                     'required': '密码必须填写',
                                     'min_length': '密码最小长度至少8位',
                                     'max_length': '密码最大长度最多16位',
                                 })

    class Meta:
        model = Users
        fields = ['phone']

        error_messages = {
            "phone": {
                'required': '手机号码必须填写',
            }
        }

    # 验证手机号是否在数据库中存在
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        flag = Users.objects.filter(phone=phone)
        if not flag:
            raise forms.ValidationError('手机号不存在')

        else:
            return phone

    # 验证两次密码是否一致
    def clean(self):
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')
        if pwd and repwd and pwd != repwd:
            # 抛出异常
            raise forms.ValidationError({'repassword': '两次密码不一致'})
        else:
            return self.cleaned_data


class InforForm(forms.Form):


    nickname = forms.CharField(max_length=10,
                               min_length=2,
                               error_messages={
                                   'min_length': '昵称最小长度为2位',
                                   'max_length': '昵称最大长度为10位',

                               })

    def clean(self):
        return self.cleaned_data
