from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
# Create your views here.
from shop.models import Category, Products


def allProdCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)

        products_list = Products.objects.all().filter(category=c_page, available=True)

    else:
        products_list = Products.objects.all().filter(available=True)
    paginator = Paginator(products_list, 6)
    try:
        page = int(request.GET.get('page', 1))
        # page = request.GET.get('page') same as above
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'products': products})


def ProDetail(request, c_slug, product_slug):
    try:
        product = Products.objects.get(category__slug=c_slug, slug=product_slug)
        print(type(product))
    except Exception as e:
        raise e

    return render(request, 'product.html', {'product': product})
