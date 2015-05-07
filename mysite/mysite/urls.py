from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.view import hello,static,uploadapk,result,dynamic,static_res,uploadhash,uploadapk_d,uploadhash_d,dynamic_res,download_res,manual_res


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url("",static),
    url(r'^admin/', include(admin.site.urls)),
    url('^hello$',hello),
    url('^s_analysis$', static),
    url('^uploadapk$', uploadapk),
    url('^result$', result),
    url('^dynamicanalysis$', dynamic),
    url('^s_res/(.*)', static_res),
    url('^uploadhash$', uploadhash),
    url('^uploadhash_d$', uploadhash_d),
    url('^uploadapk_d$', uploadapk_d),
    url('^dynamic_res/(.*)', dynamic_res),
    url('^manual_res/(.*)', manual_res),
    url('^download_res/(.*)', download_res),
)
