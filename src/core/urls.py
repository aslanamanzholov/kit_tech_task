from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from .users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet,
                basename='user_list')

urlpatterns = i18n_patterns(
    path(route='admin/', view=admin.site.urls),
    path(route='api/', view=include(router.urls)),
)

urlpatterns += [
    path(route='api-auth/', view=include('rest_framework.urls')),
]


if DEBUG:
    from debug_toolbar import urls
    from django.conf.urls.static import static

    urlpatterns += (
        path(route='__debug__/', view=include(urls)),
        # path(route='silk/', view=include('silk.urls')),
    )
    urlpatterns += tuple(
        static(MEDIA_URL, document_root=MEDIA_ROOT)
    )
