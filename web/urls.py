from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from apps.pokemon_app import views
from django.contrib.auth import views as auth_views
admin.autodiscover()

urlpatterns = []

# Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    from django.contrib.staticfiles import views as staticviews
    from django.conf.urls.static import static
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^static/(?P<path>.*)$', staticviews.serve),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


normalpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login,{'template_name': 'login.html'}, name ='login'),
    url(r'^register/', views.register,name ='register' ),
    url(r'^$', views.app_entry, name='app_entry'),
    url(r'^egg_moves/$', views.egg_moves, name='egg_moves'),
    url(r'^results/', views.results, name='results'),
    url(r'^simple_upload/', views.simple_upload, name='simple_upload'),
    url(r'^upload/', views.parse, name='parse'),
    url(r'^favorites/', views.favorites, name='favorites'),
]

urlpatterns += normalpatterns


