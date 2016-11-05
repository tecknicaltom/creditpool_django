from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('creditpool.views',
    url(r'^$', 'index'),
    url(r'^new_transaction$', 'new_transaction'),
    url(r'^confirm_new_transaction$', 'confirm_new_transaction'),
    url(r'^commit_transaction$', 'commit_transaction'),
    url(r'^transaction/(?P<id>\d+)$', 'transaction', name='transaction'),
    url(r'^change_history$', 'change_history'),
)
