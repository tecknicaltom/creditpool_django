from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('creditpool.views',
	url(r'^$', 'index'),
)