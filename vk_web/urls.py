"""
URL configuration for vk_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from vk_web import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]


# Используйте include() чтобы добавлять URL из каталога приложения
from django.urls import include
from django.urls import path

urlpatterns += [
     path('', include('AskMe.urls')),

]

handler404 = "AskMe.views.page_not_found_view"

# Добавьте URL соотношения, чтобы перенаправить запросы с корневого URL, на URL приложения


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DIR)
