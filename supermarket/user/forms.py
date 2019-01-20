from django import forms

from user.helper import set_password
from user.models import Users


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
        repwd = self.cleaned_data.get('repasswprd')
        if pwd and repwd and pwd != repwd:
            # 抛出异常
            raise forms.ValidationError({'repassword': '两次密码不一致'})
        else:
            return self.cleaned_data


class LoginModelForm(forms.Form):
    """注册表单模型类"""

    # 验证密码单独定义一个字段


    class Meta:
        model = Users
        fields = ['phone']


        error_messages = {
            "phone":{
                'required':'必须填写',
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

