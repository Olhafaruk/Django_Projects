from ipaddress import ip_address

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render #для использования в представлениях
from .models import Article, Favorite, Category, Like, Tag
from django.db.models import Count


"""
Информация в шаблоны будет браться из базы данных
Но пока, мы сделаем переменные, куда будем записывать информацию, которая пойдет в контекст шаблона
"""
# Пример данных для новостей
info = {
    "users_count": 5,
    "news_count": len(Article.objects.all()),
    "categories": Category.objects.all(),
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/news/catalog/",
         "url_name": "news:catalog"},
        {"title": "Избранное",
         "url": "/news/favorites/",
         "url_name": "news:favorites"},
    ],
}
def favorites(request):
    ip_address = request.META.get('REMOTE_ADDR')
    favorite_articles = Article.objects.filter(favorites__ip_address=ip_address)
    print(f'Favorite articles for IP {ip_address}: {favorite_articles}')
    context = {**info,
               'news': favorite_articles,
               'news_count': len(favorite_articles),
               'page_obj': favorite_articles,
               'user_ip': request.META.get('REMOTE_ADDR'), }
    return render(request, 'news/catalog.html', context=context)

def toggle_favorite(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    ip_address = request.META.get('REMOTE_ADDR')
    favorite, created = Favorite.objects.get_or_create(article=article, ip_address=ip_address)
    if not created:
        favorite.delete()
    return redirect('news:detail_article_by_id', article_id=article_id)


def toggle_like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    ip_address = request.META.get("REMOTE_ADDR")
    like, created = Like.objects.get_or_create(article=article, ip_address=ip_address)
    if not created:
        like.delete()
    return redirect('news:detail_article_by_id', article_id=article_id)


def get_categories_with_news_count():
    categories = Category.objects.all().annotate(news_count=Count('article'))
    return categories

def main(request):
    """
    Представление рендерит шаблон main.html
    """
    categories = get_categories_with_news_count()
    context = {**info, 'categories': categories}
    return render(request, 'main.html', context=context)


def about(request):
    """Представление рендерит шаблон about.html"""
    categories = get_categories_with_news_count()
    context = {**info, 'categories': categories}
    return render(request, 'about.html', context=context)

def catalog(request):
    categories = get_categories_with_news_count()
    context = {**info, 'categories': categories}
    return render(request, 'news/catalog.html', context=context)

def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    return HttpResponse('All categories')

def get_news_by_category(request, category_id):
    """
    Возвращает новости по категории для представления в каталоге
    """
    category = get_object_or_404(Category, pk=category_id)
    articles = Article.objects.filter(category=category)
    #context = {**info, 'news': articles, 'news_count': len(articles), "categories": get_categories_with_news_count()}
    paginator = Paginator(articles, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj, }
    #добавлен параметр `user_ip`, который содержит IP-адрес пользователя. Это изменение сделано для передачи IP-адреса
    # пользователя в шаблоны, что позволяет корректно отображать состояние лайка.
    context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj,
               'user_ip': request.META.get('REMOTE_ADDR'), }
    return render(request, 'news/catalog.html', context=context)

def get_news_by_tag(request, tag_id):
    """
    Возвращает новости по тегу для представления в каталоге
    """
    tag = get_object_or_404(Tag, pk=tag_id)
    articles = Article.objects.filter(tags=tag)
    #context = {**info, 'news': articles, 'news_count': len(articles)}
    paginator = Paginator(articles, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj, }
    return render(request, 'news/catalog.html', context=context)

def get_category_by_name(request, slug):
    return HttpResponse(f"Категория {slug}")

def get_all_news(request):
    """Функция для отображения страницы "Каталог"
    будет возвращать рендер шаблона /templates/news/catalog.html
    - **`sort`** - ключ для указания типа сортировки с возможными значениями: `publication_date`, `views`.
    - **`order`** - опциональный ключ для указания направления сортировки с возможными значениями: `asc`, `desc`. По умолчанию `desc`.
    1. Сортировка по дате добавления в убывающем порядке (по умолчанию): `/news/catalog/`
    2. Сортировка по количеству просмотров в убывающем порядке: `/news/catalog/?sort=views`
    3. Сортировка по количеству просмотров в возрастающем порядке: `/news/catalog/?sort=views&order=asc`
    4. Сортировка по дате добавления в возрастающем порядке: `/news/catalog/?sort=publication_date&order=asc`
    """
    # считаем параметры из GET-запроса
    sort = request.GET.get('sort', 'publication_date')  # по умолчанию сортируем по дате загрузки
    order = request.GET.get('order', 'desc')  # по умолчанию сортируем по убыванию

    # Проверяем дали ли мы разрешение на сортировку по этому полю
    valid_sort_fields = {'publication_date', 'views'}
    if sort not in valid_sort_fields:
        sort = 'publication_date'

    # Обрабатываем направление сортировки
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    articles = Article.objects.select_related('category').prefetch_related('tags').order_by(order_by)

    #context = {**info, 'news': articles, 'news_count': len(articles), }
    paginator = Paginator(articles, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj, }
    context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj,
               'user_ip': request.META.get('REMOTE_ADDR'), }
    return render(request, 'news/catalog.html', context=context)

def get_detail_article_by_id(request, article_id):
    """
    Возвращает детальную информацию по новости для представления
    """
    article = get_object_or_404(Article, id=article_id)
    Article.objects.filter(pk=article_id).update(views=F("views") + 1)
    article.refresh_from_db() # Обновить объект article из базы данных
    context = {**info, 'article': article}
    return render(request, 'news/article_detail.html', context=context)

def get_detail_article_by_title(request, title):
    """
    Возвращает детальную информацию по новости для представления
    """
    article = get_object_or_404(Article, slug=title)
    #context = {**info, 'article': article}
    context = {**info, 'article': article, 'user_ip': request.META.get('REMOTE_ADDR'), }
    return render(request, 'news/article_detail.html', context=context)

def filter_news_by_tag_id(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    articles = Article.objects.filter(tags=tag)
    context = {**info, "news": articles, "news_count": len(articles), }
    return render(request, 'news/catalog.html', context=context)

def filter_article_by_category_id(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = Article.objects.filter(category=category)
    context = {**info, "news": articles, "news_count": len(articles), }
    return render(request, 'news/catalog.html', context=context)


def search_news(request):
    query = request.GET.get('q')
    articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    paginator = Paginator(articles, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj, }
    #context = {**info, 'news': articles, 'news_count': len(articles), 'query': query}
    context = {**info, 'news': articles, 'news_count': len(articles), 'page_obj': page_obj,
               'user_ip': request.META.get('REMOTE_ADDR'), }
    return render(request, 'news/catalog.html', context=context)

