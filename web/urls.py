from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from apps import views

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
    url(r'^$', views.app_entry, name='app_entry'),
]
urlpatterns += normalpatterns
