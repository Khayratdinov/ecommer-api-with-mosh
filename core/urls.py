from django.contrib import admin
from django.urls import path, include



urlpatterns = [

    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('playground/', include('apps.playground.urls')),
    path('store/', include('apps.store.urls')),
    path('users/', include('apps.users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

]
