from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'csrf$', 'auth.views.get_csrf'),
    url(r'user/list$', 'auth.views.list_users'),
    url(r'user/create$', 'auth.views.create_user'),
    url(r'user/auth$', 'auth.views.auth_user')
)
