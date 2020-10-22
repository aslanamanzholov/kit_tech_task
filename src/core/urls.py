from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from .task.views import TaskViews
from .users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet,
                basename='user_list')
router.register(r'task', TaskViews,
                basename='task_list')

urlpatterns = i18n_patterns(
    path(route='admin/', view=admin.site.urls),
    path(route='api/v1/', view=include(router.urls)),
    path(route='api-token-auth', view=TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(route='api/token/refresh/', view=TokenRefreshView.as_view(), name='token_refresh'),
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
