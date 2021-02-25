from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "foodgram.views.page_not_found"
handler500 = "foodgram.views.server_error"

urlpatterns = [
    path("", include("api.urls")),
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("about-author/", views.flatpage, {"url": "/about-author/"},
         name="about-author"),
    path("about-spec/", views.flatpage, {"url": "/about-spec/"},
         name="about-spec"),
    path("", include("users.urls")),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
