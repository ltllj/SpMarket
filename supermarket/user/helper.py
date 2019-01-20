import hashlib

from supermarket.settings import SECRET_KEY


def set_password(password):
    # 循环  + 加盐
    for _ in range(1000):
        password_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.md5(password_str.encode('utf-8'))
        password = h.hexdigest()

    # 返回密码
    return password


def login(request,user):

    request.session['ID'] = user.pk
    request.session['phone'] = user.phone
    request.session.set_expiry(0)  # 关闭浏览器就没有