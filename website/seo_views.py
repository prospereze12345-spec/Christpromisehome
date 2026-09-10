"""
seo_views.py
------------
A dynamic robots.txt view.

Why a view instead of a static /static/robots.txt file:
    A static file is simpler, but a view lets you automatically block
    crawling on any non-production environment (staging, a Heroku review
    app, DEBUG=True locally) without remembering to swap files. Getting a
    staging copy of this site indexed under the real domain is a classic,
    embarrassing SEO mistake (duplicate content, or a "Coming soon" page
    outranking the real one) — this view makes that impossible by
    construction.

Drop this file into your `website` app next to sitemaps.py, then wire it
up in urls.py (see the accompanying urls.py notes).
"""

from django.conf import settings
from django.http import HttpResponse
from django.templatetags.static import static
from django.urls import reverse


def robots_txt(request):
    """
    Serves /robots.txt.

    - In production (DEBUG=False) it allows everything except admin/media
      management paths and points crawlers at the sitemap.
    - In any non-production environment it disallows everything, so a
      staging deploy can never accidentally get indexed under the live
      domain.
    """

    sitemap_url = request.build_absolute_uri(reverse("sitemap"))

    if settings.DEBUG or getattr(settings, "SEO_ENVIRONMENT", "production") != "production":
        lines = [
            "User-agent: *",
            "Disallow: /",
        ]
    else:
        lines = [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /accounts/",
            "Disallow: /media/private/",
            "",
            f"Sitemap: {sitemap_url}",
        ]

    return HttpResponse("\n".join(lines), content_type="text/plain")