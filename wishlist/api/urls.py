from rest_framework.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from api import views


urlpatterns = [
    url(r'^auth/', obtain_auth_token),
    url(r'^clients/$', views.ClientList.as_view(), name='client-list-create'),
    url(r'^clients/(?P<pk>[0-9]+)/$', views.ClientDetail.as_view(), name='client-detail-update-delete'),
    url(r'^clients/(?P<pk>[0-9]+)/wishlist/$', views.ClientWishlist.as_view(), name='client-wishlist'),
    url(r'^wishlist/$', views.WishlistList.as_view(), name='wishlist-create'),
    url(r'^wishlist/(?P<string>[\w\-]+)/(?P<pk>[0-9]+)/$', views.WishlistDetail.as_view(), name='wishlist-delete'),
]
