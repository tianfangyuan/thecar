import hmac
import string
import random
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from django.shortcuts import render


# def require_login(fn):
#     """
#     一个判断用户是否登录的装饰器
#     :param fn: 视图函数
#     :return: 如果已登录，则进入视图函数，如果没登录则返回登录页面
#     """
#     def inner(request, *args, **kwargs):
#         # 判断session用户是否存在登录用户
#         username = request.user.username
#         if username is not None:
#             return fn(request, *args, **kwargs)
#         else:
#             # 将页面打到登录页面
#             return render(request, "thecar/user_login.html", {"msg": "该页面必须登录才能访问"})
#     return inner


def pwd_by_hmac(password):
    """
    使用hmac模块完成对用户密码的加密
    :param password: 用户密码
    :return: 一个加密后密文
    """
    return hmac.new(settings.SALT.encode("utf-8"), password.encode("utf-8"), "MD5").hexdigest()


def get_random_char(count=4):
    # 生成随机字符串
    ran = string.ascii_lowercase + string.digits
    char = ""
    for i in range(count):
        char += random.choice(ran)
    return char


def get_random_color():
    # 返回一个随机的rgb颜色
    return random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new("RGB", (120, 30), (26, 160, 52))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype("arial.ttf", 25)

    code = get_random_char()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5, 0), code[t], get_random_color(), font)

    # 生成干扰点
    for _ in range(random.randint(100, 300)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=get_random_color())
        # 使用模糊滤镜使图片模糊
        # img = img.filter(ImageFilter.BLUR)
        # img.save(".join(code)"+'.jpg', 'jpeg')
        return img, code


def require_login(fn):
    """
    一个判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已登录，则进入视图函数，如果没登录则返回登录页面
    """
    def inner(request, *args, **kwargs):
        # 判断session用户是否存在登录用户
        usernsme = request.user.get["username", None]
        if usernsme is not None:
            return fn(request, *args, **kwargs)
        else:
            # 将页面打到登录页面
            return render(request, "thecar/user_login.html", {"msg": "该页面必须登录才能访问"})
    return inner


