"""
seo_views.py
------------
Dynamic robots.txt view for Christ Promise Children's Home.
"""

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse


def robots_txt(request):
    """
    Serves /robots.txt.

    Production:
        Allows search engines to crawl the public website.

    Non-production:
        Blocks crawling completely.
    """

    sitemap_url = request.build_absolute_uri(
        reverse("sitemap")
    )

    environment = getattr(
        settings,
        "SEO_ENVIRONMENT",
        "production"
    )

    if environment != "production":
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

    response = HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )

    # Prevent an old robots.txt response from being cached.
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response