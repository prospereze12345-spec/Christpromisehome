from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include

from website.sitemap import StaticViewSitemap
from website.seo_views import robots_txt


def google_verification(request):
    return HttpResponse(
        "google-site-verification: google19468042a663e340.html",
        content_type="text/plain",
    )


sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("website.urls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    path("robots.txt", robots_txt, name="robots_txt"),

    path(
        "google19468042a663e340.html",
        google_verification,
        name="google_verification",
    ),
]