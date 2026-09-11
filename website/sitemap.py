from types import SimpleNamespace

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap for the public static pages of
    Christ Promise Children's Home.

    The sitemap domain is taken from SEO_SITE_DOMAIN rather than
    django.contrib.sites, so an incorrect django_site database record
    cannot produce example.com URLs.
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

    def get_urls(self, page=1, site=None, protocol=None):
        """
        Ignore django_site completely.

        Always use our explicitly configured production domain.
        """

        domain = getattr(
            settings,
            "SEO_SITE_DOMAIN",
            "christpromisehome.com",
        )

        fixed_site = SimpleNamespace(
            domain=domain
        )

        return super().get_urls(
            page=page,
            site=fixed_site,
            protocol="https",
        )