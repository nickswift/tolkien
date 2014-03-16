from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^csrf'  , 'auth.views.reset_csrf'),
    url(r'^create', 'auth.views.user_create'),
    url(r'^login' , 'auth.views.user_login'),
    url(r^'logout', 'auth.views.user_logout'),
)
