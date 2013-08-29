from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from django.utils.functional import lazy
from django.core.urlresolvers import reverse

lazy_reverse = lazy(reverse, str)

urlpatterns = patterns('',

	url(r'^tcs/', include('tcs.urls')),
	url(r'^$', RedirectView.as_view(url = lazy_reverse('main'))),

    # Examples:
    # url(r'^$', 'tcsweb.views.home', name='home'),
    # url(r'^tcsweb/', include('tcsweb.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
