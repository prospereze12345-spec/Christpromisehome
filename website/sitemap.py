"""
sitemaps.py
-----------
Sitemap classes for Christ Promise Children's Home (christpromisehome.com).

Drop this file into your `website` app (same folder as views.py / urls.py).

Django's sitemap framework needs `django.contrib.sitemaps` in INSTALLED_APPS
and the "sites" framework enabled. See the bottom of this file / the
accompanying urls.py notes for the settings.py changes required.

Why a dict-based config instead of one class per page:
    Every page here is a flat, static template driven by a named URL
    (no model instances), so a single class that iterates over a list of
    (url_name, changefreq, priority) tuples is far easier to maintain than
    one Sitemap subclass per page. When you add a new page, you add one
    line here — nothing else.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap for the public static pages of
    Christ Promise Children's Home.
    """

    protocol = "https"

    pages = [
        ("home", "weekly", 1.0),
        ("about", "monthly", 0.9),
        ("programmes", "monthly", 0.9),
        ("donate", "weekly", 0.9),
        ("gallery", "monthly", 0.6),
        ("contact", "monthly", 0.7),
        ("safeguarding", "yearly", 0.5),
        ("privacy_policy", "yearly", 0.3),
        ("terms_and_conditions", "yearly", 0.3),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        url_name, _, _ = item
        return reverse(url_name)

    def changefreq(self, item):
        _, changefreq, _ = item
        return changefreq

    def priority(self, item):
        _, _, priority = item
        return priority

    # No lastmod is set on purpose: these are hand-edited templates with no
    # "date last changed" tracked anywhere. If you later move page copy into
    # the database (e.g. a FlatPage or a CMS model with `updated_at`), add:
    #
    #   def lastmod(self, item):
    #       return item.updated_at
    #
    # Google is fine with sitemaps that omit lastmod; it just won't use
    # freshness as a crawl-priority signal for these URLs.


# Registered in urls.py as:
#   sitemaps = {"static": StaticViewSitemap}