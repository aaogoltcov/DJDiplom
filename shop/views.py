from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import connection, IntegrityError
from django.db.models import Count, Sum
from django.shortcuts import render, redirect

from cart.models import Cart
from orders.models import Order
from shop.forms import ReviewForm, SignUpForm
from shop.models import Feedback

from shop.sql_scripts.sql_scripts import dict_fetchall, SELECT_MENU, SELECT_SUB_MENU, SELECT_PAPERS, \
    SELECT_GOODS_IN_PAPERS, SELECT_CATALOG, SELECT_GOODS_IN_CATALOG, get_good_info_and_feedback


def check_feedback(request, good_id):
    try:
        user_id = request.session['_auth_user_id']
    except KeyError:
        user_id = 0
    try:
        csrftoken = request.COOKIES['csrftoken']
    except KeyError:
        csrftoken = None
    csrftoken_check = Feedback.objects.filter(good_id=int(good_id), csrftoken=csrftoken).values('csrftoken').distinct()
    author_id_check = Feedback.objects.filter(good_id=int(good_id), author_id=int(user_id)).values(
        'author_id').distinct()
    if csrftoken_check or author_id_check:
        return False
    else:
        return True


def get_menu():
    with connection.cursor() as cursor:
        menus = dict_fetchall(cursor.execute(SELECT_MENU))
        sub_menus = dict_fetchall(cursor.execute(SELECT_SUB_MENU))
        for menu in menus:
            menu['sub_menus'] = []
            for sub_menu in sub_menus:
                if sub_menu['catalog_id'] == menu['catalog_id']:
                    menu['sub_menus'].append(sub_menu)
        return menus


def add_good_to_cart(request):
    try:
        user_id = request.session['_auth_user_id']
    except KeyError:
        user_id = 0

    try:
        get_good_id_for_cart = int(request.POST.get('cart'))
    except TypeError:
        get_good_id_for_cart = None
    if get_good_id_for_cart and user_id != 0:
        Cart(user_id=user_id, good_id=get_good_id_for_cart).save()


def index_view(request):
    with connection.cursor() as cursor:
        papers = dict_fetchall(cursor.execute(SELECT_PAPERS))
        goods = dict_fetchall(cursor.execute(SELECT_GOODS_IN_PAPERS))
        for paper in papers:
            paper['goods'] = []
            for good in goods:
                if paper['paper_id'] == good['paper_id']:
                    paper['goods'].append(good)
        context = {
            'papers': papers,
            'menus': get_menu(),
        }
    add_good_to_cart(request)
    return render(request, 'index.html', context)


def goods_view(request, catalog_id):
    with connection.cursor() as cursor:
        catalogs = dict_fetchall(cursor.execute(SELECT_CATALOG))
        goods = dict_fetchall(cursor.execute(SELECT_GOODS_IN_CATALOG))
        for catalog in catalogs:
            catalog['goods'] = []
            for good in goods:
                if catalog['catalog_id'] == good['catalog_id']:
                    catalog['goods'].append(good)
        context = {
            'catalogs': [catalog for catalog in catalogs if (catalog['catalog_id'] == int(catalog_id))][0],
            'menus': get_menu(),
        }
    add_good_to_cart(request)
    return render(request, 'goods.html', context)


def good_view(request, good_id):
    form = ReviewForm()
    is_feedback = check_feedback(request, good_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if is_feedback:
                try:
                    user_id = request.session['_auth_user_id']
                except KeyError:
                    user_id = 0
                if user_id:
                    Feedback(person_name=str(form.cleaned_data['person_name']),
                             description=str(form.cleaned_data['description']),
                             score=str(form.cleaned_data['score']),
                             good_id=good_id,
                             author_id=request.session['_auth_user_id'],
                             csrftoken=request.COOKIES['csrftoken'],
                             ).save()
                else:
                    Feedback(person_name=str(form.cleaned_data['person_name']),
                             description=str(form.cleaned_data['description']),
                             score=str(form.cleaned_data['score']),
                             good_id=good_id,
                             csrftoken=request.COOKIES['csrftoken'],
                             ).save()
                return redirect('good', good_id=good_id)
    else:
        form = form
    context = {
        'form': form,
        'good_id': good_id,
        'good': get_good_info_and_feedback(good_id)[0],
        'menus': get_menu(),
        'is_feedback': is_feedback,
    }
    add_good_to_cart(request)
    return render(request, 'good.html', context)


def cart_view(request):
    try:
        user_id = request.session['_auth_user_id']
    except KeyError:
        user_id = 0

    try:
        get_cart_for_order = request.POST.get('order').replace('[', '').replace(']', '').split(',')
    except AttributeError:
        get_cart_for_order = None

    is_ordered = False

    goods = Cart.objects.filter(user__id=user_id, is_ordered=False).values('good__name',
                                                                           'good__description',
                                                                           'good__price',
                                                                           ).annotate(total=Count('good__id')
                                                                           ).annotate(total_price=Sum('good__price')
                                                                           ).order_by('-total')
    total_goods = sum([good['total'] for good in goods if good])
    total_price = sum([good['total_price'] for good in goods if good])
    cart = (Cart.objects.filter(user__id=user_id).values('id', ))
    list_of_cart = [[value for key, value in item.items() if value][0] for item in cart if item]

    if get_cart_for_order and user_id != 0:
        order = Order(user_id=user_id, goods_count=total_goods, goods_price=total_price)
        order.save()
        for cart in list_of_cart:
            order.cart.add(cart)
            order.save()
            cart_is_ordered = Cart.objects.get(id=cart)
            cart_is_ordered.is_ordered = True
            cart_is_ordered.save()
        is_ordered = True

    context = {
        'goods': goods,
        'total': total_goods,
        'total_price': total_price,
        'cart': list_of_cart,
        'is_ordered': is_ordered,
        'menus': get_menu(),
    }

    return render(request, 'cart.html', context)


def signup(request):
    is_user = False
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                User.objects.create(username=email.split('@')[0], email=email,
                                    password=make_password(raw_password)).save()

                user = authenticate(email=email, password=raw_password)
                print(user)
                login(request, user)
                return redirect('login')
            except IntegrityError:
                is_user = True
    else:
        form = SignUpForm()
    return render(
        request,
        'signup.html',
        {'form': form,
         'menus': get_menu(),
         'is_user': is_user, },
    )


def accessories_view(request):
    return render(request, 'accessories.html', {'menus': get_menu(), })
