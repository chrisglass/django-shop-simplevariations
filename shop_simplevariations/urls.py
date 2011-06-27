from django.conf.urls.defaults import patterns, url

from .views import SimplevariationCartDetails


urlpatterns = patterns('',
    url(r'^delete/$',
        SimplevariationCartDetails.as_view(action='delete'),
        name='cart_delete'),
    url('^item/$',
        SimplevariationCartDetails.as_view(action='post'),
        name='cart_item_add' ),
    url(r'^$',
        SimplevariationCartDetails.as_view(), name='cart'),
    url(r'^cart/update/$',
        SimplevariationCartDetails.as_view(action='put'),
        name='cart_update'),
    url('^item/(?P<id>[0-9A-Za-z-_.//]+)$',
        SimplevariationCartDetails.as_view(),
        name='cart_item' ),
)
