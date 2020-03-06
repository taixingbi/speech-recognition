from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views

from django.views.generic import TemplateView


urlpatterns = [

    path('', views.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),

    #test
    path('test/', views.Demo.test, name='test'),
    path('s3/', views.Demo.s3, name='s3'),
    path('db/', views.Demo.db, name='db'),
    path('ses/', views.Demo.ses, name='ses'),

    
    path('<key>/', views.Demo.demo, name='demo'),

    path('aws/<key>/', views.Demo.aws, name='aws'),

    #api
    path('api/', include([
        #path('<key>', views.Demo.demo, name='demo'),
        path('demo/', views.Demo.demo, name='demo'),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
