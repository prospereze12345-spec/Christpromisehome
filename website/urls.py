from django.urls import path
from . import views
from website.views import smtp_test
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("programmes/", views.programmes, name="programmes"),
    path("gallery/", views.gallery, name="gallery"),
    path("donate/", views.donate, name="donate"),
   path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
path("safeguarding/", views.safeguarding, name="safeguarding"),
path(
    "terms-and-conditions/",
    views.terms_and_condition,
    name="terms_and_conditions",
),
path(
    "contact/send/",
    views.send_contact_message,
    name="send_contact_message"
),
path(
    "donate/send/",
    views.send_donation_enquiry,
    name="send_donation_enquiry",
),
path("smtp-test/", smtp_test, name="smtp_test"),
]

