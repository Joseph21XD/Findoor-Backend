from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('admin/', admin.site.urls),
	
	url(r'^$', hello.views.index, name='index'),
	url(r'^persona.json/KEY=(?P<tok>[-\w]+)/$', hello.views.personJson, name='personJson'),
	url(r'^persona/(?P<id_personaje>\d+).json/KEY=(?P<tok>[-\w]+)/$', hello.views.person_id_Json, name='person_id_Json'),
	url(r'^persona/add/(?P<name>[-\w]+)/(?P<lastName>[-\w]+)/(?P<isFace>\d+)/(?P<mail>[-\w]+)/(?P<pwd>[-\w]+)/(?P<img>[-\w]+)/$',hello.views.person_add, name='person_add'),
	url(r'^persona/update/(?P<id_persona>\d+)/(?P<name>[-\w]+)/(?P<lastName>[-\w]+)/(?P<isFace>\d+)/(?P<mail>[-\w]+)/(?P<pwd>[-\w]+)/(?P<img>[-\w]+)/KEY=(?P<tok>[-\w]+)/$',hello.views.person_update, name='person_update'),
	url(r'^persona/login/(?P<mail>[-\w]+)/(?P<pwd>[-\w]+)/$',hello.views.loginByCredentials, name='person_login'),
	url(r'^persona/token/(?P<tok>[-\w]+)/$',hello.views.loginByToken, name='person_token'),	
	url(r'^sitio.json/KEY=(?P<tok>[-\w]+)/$', hello.views.sitioJson, name='sitioJson'),
	url(r'^sitio/TYPE=(?P<type>[-\w]+)/(?P<id_persona>\d+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_type_Json, name='sitio_type_Json'),
	url(r'^sitio/comment/(?P<id_site>[-\w]+)/(?P<comment>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_comment, name='sitio_comment'),
	url(r'^sitio/comment/(?P<id_site>[-\w]+).json/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_comment_Json, name='sitio_comment_Json'),
	url(r'^sitio/suggest/(?P<nom>[-\w]+)/(?P<lat>[-\w]+)/(?P<lon>[-\w]+)/(?P<dir>[-\w]+)/(?P<desc>[-\w]+)/(?P<img>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_suggest, name='sitio_suggest'),
	url(r'^sitio/ranking.json/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_ranking_Json, name='sitio_ranking_Json'),	
	url(r'^sitio/close/(?P<lat>[-\w]+)/(?P<lon>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_close, name='sitio_close'),
		
	url(r'^persona/seguir/(?P<id_persona>\d+)/KEY=(?P<tok>[-\w]+)/$', hello.views.seguir, name='seguir'),
	url(r'^persona/seguidores/KEY=(?P<tok>[-\w]+)/$', hello.views.seguidores, name='seguidores'),
	url(r'^persona/seguidos/KEY=(?P<tok>[-\w]+)/$', hello.views.seguidos, name='seguidores'),
	url(r'^persona/seguido/(?P<id_persona>\d+)/KEY=(?P<tok>[-\w]+)/$', hello.views.get_seguido, name='get_seguido'),
	url(r'^sitio/add/TYPE=(?P<type>[-\w]+)/(?P<id_site>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_type_add, name='sitio_type_add'),
	url(r'^sitio/ranking/add/(?P<id_site>[-\w]+)/(?P<rank>\d+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_ranking_add, name='sitio_ranking_add'),
	url(r'^sitio/ranking/get/(?P<id_site>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_ranking_get, name='sitio_ranking_get'),
	
	url(r'^sitio/get/TYPE=(?P<type>[-\w]+)/(?P<id_site>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_type_get, name='sitio_type_get'),
	url(r'^sitio/delete/TYPE=(?P<type>[-\w]+)/(?P<id_site>[-\w]+)/KEY=(?P<tok>[-\w]+)/$', hello.views.sitio_type_delete, name='sitio_type_delete'),
	url(r'^persona/delete/(?P<id_persona>\d+)/KEY=(?P<tok>[-\w]+)/$', hello.views.seguido_delete, name='seguido_delete'),
	url(r'^persona/facebook/(?P<name>[-\w]+)/(?P<lastName>[-\w]+)/(?P<isFace>\d+)/(?P<mail>[-\w]+)/(?P<pwd>[-\w]+)/(?P<img>[-\w]+)/$',hello.views.login_facebook, name='login_facebook'),
]
