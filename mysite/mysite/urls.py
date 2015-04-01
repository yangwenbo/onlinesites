from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.view import hello,static,uploadapk,result,dynamic,static_res,uploadhash,uploadapk_d,uploadhash_d,dynamic_res,download_res


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^hello$',hello),
    url('^staticanalysis$', static),
    url('^uploadapk$', uploadapk),
    url('^result$', result),
    url('^dynamicanalysis$', dynamic),
    url('^static_res/(.*)', static_res),
    url('^uploadhash$', uploadhash),
    url('^uploadhash_d$', uploadhash_d),
    url('^uploadapk_d$', uploadapk_d),
    url('^dynamic_res/(.*)', dynamic_res),
    url('^download_res/(.*)', download_res),
)
