"""donsai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from . import views
# from dajaxice.core import dajaxice_autodiscover, dajaxice_config
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf import settings


app_name = 'donsai'


urlpatterns = [
    path('', views.index, name='index'),
    path('web/', views.web, name='web'),
    path('api/', views.api, name='api'),
    path('donsai/', views.index, name='index'),
    path('donsai/web/', views.web, name='web'),
    path('donsai/api/', views.api, name='api'),
    path('omnichat/', views.web, name='web'),
    path('omnichat/api', views.api, name='api'),
    path('donsai/omnichat/', include('omnichat_web.urls')),
    path('donsai/omnichat/api/', include('omnichat_api.urls')),
    path('donsai/admin/', admin.site.urls),
]

# urlpatterns += patterns('',
#                         url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),)
# urlpatterns += staticfiles_urlpatterns()
