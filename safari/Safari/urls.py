from django.contrib import admin
from django.urls import path, include
from Websitert import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin', admin.site.urls),
    path('event/', views.event, name='event'),
    #path('about/', views.about, name='tentang-kami'),
    path('fasilitas/', views.fasiltias, name='fasilitas'),
    path('contact/', views.contact, name='contact'),
    path('', include('Websitert.urls')),
    # path('accounts', include('django.contrib.auth.urls')),#new
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# url project/urls.py
