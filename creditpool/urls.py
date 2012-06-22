from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('creditpool.views',
	url(r'^$', 'index'),
	url(r'^new_transaction', 'new_transaction'),
	url(r'^confirm_transaction', 'confirm_transaction'),
	url(r'^commit_transaction', 'commit_transaction'),
	url(r'^transfer/(?P<id>\d+)$', 'transfer', name='transfer'),
)
