from django.conf.urls import url
from . import views


urlpatterns = [
    url(r"^user_login/$", views.user_login, name="user_login"),
    url(r"^user_logout/$", views.user_logout, name="user_logout"),
    url(r"^reg/$", views.reg, name="reg"),
    url(r"^code/$", views.code, name="code"),
    url(r"^user_info/$", views.user_info, name="user_info"),
    url(r"^index/$", views.index, name="index"),
    url(r"^user_update/(?P<u_id>\d+)/$", views.user_update, name="user_update"),

    url(r"^article_add/$", views.article_add, name="article_add"),
    url(r"^article_detail/(?P<a_id>\d+)/$", views.article_detail, name="article_detail"),
    url(r"^article_show/(?P<a_id>\d+)/$", views.article_show, name="article_show"),
    url(r"^article_update/(?P<a_id>\d+)/$", views.article_update, name="article_update"),
    url(r"^article_self/$", views.article_self, name="article_self"),
    url(r"^article_delete/(?P<a_id>\d+)/$", views.article_delete, name="article_delete"),
    # url(r"^article_list/$", views.article_list, name="article_list"),
    url(r"^show/(?P<u_id>\d+)/$", views.show, name="show"),
    url(r"^article_update/(?P<a_id>\d+)/$", views.article_update, name="article_update"),
]
