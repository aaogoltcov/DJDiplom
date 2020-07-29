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
