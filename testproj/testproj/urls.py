from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from testapp import views

router = DefaultRouter()

router.register(r'countries', views.CountryViewSet)
router.register(r'countries_h', views.CountryHyperlinkedViewSet, base_name='countryh')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls))
)
