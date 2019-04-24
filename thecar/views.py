from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import HttpResponse
from io import BytesIO
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import models
from . import utils
from .utils import require_login
from django.core.paginator import Paginator
from django.conf import settings
from . import cache_util


# 验证码
def code(request):
    # 验证码的视图函数
    img, msg = utils.create_code()
    file = BytesIO()
    img.save(file, "PNG")
    request.session["code"] = msg
    return HttpResponse(file.getvalue(), 'image/png')


# 登录
def user_login(request):
    if request.method == "GET":
        return render(request, "thecar/user_login.html", {})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        # code = request.POST["code"].strip()

        # 数据校验
        # 第一步验证码验证
        # msg = request.session["code"]
        # if msg.lower() != code.lower():
        #     return render(request, "TheCar/login.html", {"msg": "验证码有误！！"})
        if username == "":
            return render(request, "thecar/user_login.html", {"msg": "用户名不能为空"})
        if password == "":
            return render(request, "thecar/user_login.html", {"msg": "用户名不能为空"})

        # user = models.User.objects.filter(username=username, password=password)
        # if len(user) == 1:
        #     request.session["login_user"] = user[0]
        #     return redirect(reverse("TheCar:user_info"))
        # else:
        #     return render(request, "TheCar/login.html", {"msg": "登录失败，用户名或密码错误"})
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # request.session["login_user"] = user
                # return render(request, "thecar/index.html", {"user": user})
                return redirect(reverse("thecar:index"))
            else:
                return render(request, "thecar/user_login.html", {"msg": "登录失败"})
        else:
            return render(request, "thecar/user_login.html", {"msg": "用户名或密码错误，请重新登陆"})


# 退出
def user_logout(request):
    request.session.flush()
    logout(request)
    return redirect(reverse("thecar:index"))


# 注册
def reg(request):
    if request.method == "GET":
        return render(request, "thecar/reg.html", {})
    else:
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        nickname = request.POST["nickname"].strip()
        confirm_pwd = request.POST["confirm_pwd"].strip()
        code = request.POST["code"].strip()
        msg = request.session["code"]
        avatar = request.FILES.get("avatar", "static/img/avatar/default.jpg")

        if msg.lower() != code.lower():
            return render(request, "thecar/reg.html", {"msg": "验证码有误！！"})
        if username == "":
            return render(request, "thecar/reg.html", {"msg": "用户名不能为空"})
        if len(password) < 3:
            return render(request, "thecar/reg.html", {"msg": "密码不能小于六位"})
        if password != confirm_pwd:
            return render(request, "thecar/reg.html", {"msg": "两次密码不一致"})
        try:
            models.User.objects.get(username=username)
            return render(request, "thecar/reg.html", {"msg": "用户名已存在"})
        except:
            try:
                models.UserInfo.objects.get(nickname=nickname, avatar=avatar)
                return render(request, "thecar/reg.html", {"msg": "该昵称已存在"})
            except:
                user = User.objects.create_user(username=username, password=password)
                userinfo = models.UserInfo(nickname=nickname, avatar=avatar, user=user)
                user.save()
                userinfo.save()
                return render(request, "thecar/user_login.html", {"msg": "用户注册成功，请登录！"})


@login_required
# 个人信息
def user_info(request):

    return render(request, "thecar/user_info.html")


@login_required
# 修改用户信息
def user_update(request, u_id):
    if request.method == "POST":
        nickname = request.POST["nickname"].strip()
        gender = request.POST["gender"].strip()
        age = request.POST["age"].strip()
        avatar = request.FILES.get("avatar",)

        if nickname == "":
            return render(request, "thecar/user_info.html", {"msg": "用户昵称不能为空"})
        if avatar == "":
            return render(request, "thecar/user_info.html", {"msg": "用户头像不能为空"})
        user = models.UserInfo.objects.get(pk=u_id)

        user.avatar = avatar
        user.nickname = nickname
        user.age = age
        user.gender = gender
        # request.session["login_user"] = user
        user.save()

        return render(request, "thecar/user_info.html", {"msg": "修改成功"})


# 主页
def index(request):
    pageNow = request.GET.get("pageNow", 1)
    articles = models.Article.objects.all()
    paginator = Paginator(articles, settings.PAGE_SIZE)
    page = paginator.page((pageNow))
    return render(request, "thecar/index.html", {"page": page})


def show(request, u_id):
    user = models.UserInfo.objects.get(pk=u_id)
    return render(request, "thecar/show.html", {"user": user})


@login_required
# 添加文章
def article_add(request):
    if request.method == "GET":
        return render(request, "thecar/article_add.html", {})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        author = request.user

        if title == "":
            return render(request, "thacar/article_add.html", {"msg": "文章标题不能为空"})
        if len(title) > 200:
            return render(request, "thacar/article_add.html", {"msg": "标题不能超200字"})
        if content == "":
            return render(request, "thacar/article_add.html", {"msg": "内容不能为空"})

        at = models.Article(title=title, content=content, author=author)
        try:
            at.save()
            return redirect(reverse("thecar:article_detail", kwargs={"a_id": at.id}))
        except:
            return render(request, "thecar/article_add.html", {"msg": "添加失败，请重新添加"})


@login_required
# 文章详情
def article_detail(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.count += 1
    at.save()

    return render(request, "thecar/article_detail.html", {"article": at})


def article_show(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.count += 1
    at.save()

    return render(request, "thecar/article_show.html", {"article": at})


@login_required
#
def article_self(request):
    login_user = request.user
    articles = models.Article.objects.filter(author=login_user)
    return render(request, "thecar/article_self.html", {"articles": articles})


@login_required
# 修改文章
def article_update(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "thecar/article_update.html", {"article": at})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()

        if title == "":
            return render(request, "thecar/article_update.html", {"msg": "标题不能为空"})
        if content == "":
            return render(request, "thecar/article_update.html", {"msg": "内容不能为空"})
        if len(title) > 200:
            return render(request, "thacar/article_update.html", {"msg": "标题不能超200字"})

        at.title = title
        at.content = content
        at.save()
        return redirect(reverse("thecar:article_detail", kwargs={"a_id": at.id}))


@login_required
# 删除文章
def article_delete(request, a_id):
    try:
        at = models.Article.objects.get(pk=a_id)
        at.delete()
    except:
        pass
    finally:
        return redirect(reverse("thecar:article_self"))


# 文章列表
def article_list(request, ):
    articles = models.Article.objects.all()
    return render(request, "thecar/article_list.html", {"articles": articles})












