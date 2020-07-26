"""djdiplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin, auth
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path

from djdiplom import settings
from shop.views import index_view, goods_view, good_view, cart_view, signup, accessories_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logged_out'),
    path('goods/<int:catalog_id>', goods_view, name='goods'),
    path('good/<int:good_id>', good_view, name='good'),
    path('cart/', cart_view, name='cart'),
    path('accesories/', accessories_view, name='accessories')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
