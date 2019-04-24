from django.db import models
# from tinymce.models import HTMLField
from DjangoUeditor.models import UEditorField
from django.contrib.auth.models import User


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="用户主键")
    # username = models.CharField(max_length=100, unique=True, verbose_name="用户名称")
    # password = models.CharField(max_length=100, verbose_name="用户密码")
    # email = models.CharField(max_length=100, verbose_name="用户邮箱")
    nickname = models.CharField(max_length=100, verbose_name="用户昵称")
    avatar = models.ImageField(upload_to="static/img/avatar", default="static/img/avatar/default.jpg",
                               verbose_name="用户头像")
    gender = models.CharField(max_length=10, default="男", verbose_name="用户性别")
    age = models.IntegerField(max_length=20, default="18", verbose_name="用户年龄")
    # 和系统内置的用户管理，一对一的关联
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # lost_login = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="最后登录时间")


class Article(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="用户文章")
    title = models.CharField(max_length=200, verbose_name="用户文章")
    content = UEditorField(verbose_name="文章内容")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name="写文章时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="修改文章时间")
    count = models.IntegerField(default=0, verbose_name="点击量")
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    # 车名
    Car_name = models.CharField(max_length=200, verbose_name="汽车品牌")
    # 车型号
    Car_model = models.CharField(max_length=200, verbose_name="汽车型号")
    # 车动力
    Car_power = models.CharField(max_length=200, verbose_name="汽车动力")
    # 车描述
    Car_description = UEditorField(verbose_name="汽车描述")
    Car_user = models.ForeignKey(User, on_delete=models.CASCADE)
