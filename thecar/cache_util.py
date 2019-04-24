from django.core.cache import cache
from . import models


def get_all_article(is_change=False):
    print("从缓存中获取数据")
    article = cache.get("all_article")
    if article is None or is_change:
        print("redis中没有数据，从数据库中获取数据")
        articles = models.Article.objects.all()
        print("将数据放到缓存中")
        cache.set("all_article", articles)
    return articles
