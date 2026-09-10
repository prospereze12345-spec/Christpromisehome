

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "website"

    def ready(self):
        from django.conf import settings

        if getattr(settings, "SEO_ENVIRONMENT", "") != "production":
            return

        try:
            from django.contrib.sites.models import Site

            site = Site.objects.get(pk=settings.SITE_ID)

            if site.domain != "christpromisehome.com":
                site.domain = "christpromisehome.com"
                site.name = "Christ Promise Children's Home"
                site.save(update_fields=["domain", "name"])

        except Exception:
            # Do not prevent Django from starting if the database
            # or django_site table is not ready yet.
            pass