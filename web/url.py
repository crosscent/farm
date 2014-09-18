from django.conf.urls.defaults import patterns, include, url
from vendors.views import registration

urlpatterns = patterns('',
	url(r'^$', 'web.views.index'),
    url(r'^registration/$', 'vendors.views.registration', name='registration'),
    url(r'^login/$', 'vendors.views.user_login', name='login'),
    url(r'^logout/$', 'vendors.views.user_logout', name='logout'),
    url(r'^profile/$', 'vendors.views.profile', name='profile'),
    )
