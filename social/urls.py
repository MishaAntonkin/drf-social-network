from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from rest_framework.schemas import get_schema_view

from user.urls import router


schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('user-api/', include((router.urls, 'user-api'))),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('schema/', schema_view),

]
