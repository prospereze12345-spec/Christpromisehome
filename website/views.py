
from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")

def about(request):
    return render(request, "website/about.html")


def programmes(request):
    return render(request, "website/programmes.html")

def contact(request):
    return render(request, "website/contact.html")

def gallery(request):
    return render(request, "website/gallery.html")

def donate(request):
    return render(request, "website/donate.html")

def privacy_policy(request):
    return render(request, "website/privacy_policy.html")


def safeguarding(request):
    return render(request, "website/Safeguarding.html")

def terms_and_condition(request):
    return render(request, "website/terms_and_conditions.html")








from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)


@require_POST
def send_contact_message(request):

    # -----------------------------------------
    # Get submitted form data
    # -----------------------------------------

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    consent = request.POST.get("consent")


    # -----------------------------------------
    # Validate required fields
    # -----------------------------------------

    if not name:
        return JsonResponse({
            "success": False,
            "message": "Please enter your name."
        }, status=400)

    if not email:
        return JsonResponse({
            "success": False,
            "message": "Please enter your email address."
        }, status=400)

    if not subject:
        return JsonResponse({
            "success": False,
            "message": "Please enter a subject."
        }, status=400)

    if not message:
        return JsonResponse({
            "success": False,
            "message": "Please enter your message."
        }, status=400)


    # -----------------------------------------
    # Privacy consent
    # -----------------------------------------

    if consent != "true":
        return JsonResponse({
            "success": False,
            "message": (
                "Please agree to the Privacy Policy "
                "before sending your message."
            )
        }, status=400)


    # -----------------------------------------
    # Validate visitor email
    # -----------------------------------------

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "message": "Please enter a valid email address."
        }, status=400)


    # -----------------------------------------
    # Validate input lengths
    # -----------------------------------------

    if len(name) > 100:
        return JsonResponse({
            "success": False,
            "message": "Your name is too long."
        }, status=400)

    if len(subject) > 200:
        return JsonResponse({
            "success": False,
            "message": "Your subject is too long."
        }, status=400)

    if len(message) > 5000:
        return JsonResponse({
            "success": False,
            "message": (
                "Your message is too long. "
                "Please keep it below 5,000 characters."
            )
        }, status=400)


    # -----------------------------------------
    # Normalize subject
    # -----------------------------------------

    subject = " ".join(subject.split())


    # -----------------------------------------
    # Prepare notification email
    # -----------------------------------------

    email_subject = f"Website Contact: {subject}"

    email_body = f"""\
New message received from the
Christ Promise Children's Home website.

----------------------------------------
Visitor Information
----------------------------------------

Name:
{name}

Email:
{email}

Subject:
{subject}

----------------------------------------
Message
----------------------------------------

{message}

----------------------------------------

Reply to:
{email}

Submitted through:
https://christpromisehome.com
"""


    # -----------------------------------------
    # Send email
    # -----------------------------------------

    try:

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )

    except Exception:
        logger.exception(
            "Failed to send Christ Promise Children's Home "
            "contact form email."
        )

        return JsonResponse({
            "success": False,
            "message": (
                "We couldn't send your message right now. "
                "Please try again in a few minutes."
            )
        }, status=500)


    # -----------------------------------------
    # Success
    # -----------------------------------------

    return JsonResponse({
        "success": True,
        "message": (
            "We have received your message. "
            "We will get back to you within a few hours."
        )
    }, status=200)
@require_POST
def send_donation_enquiry(request):

    # -----------------------------------------
    # Get submitted form data
    # -----------------------------------------

    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    message = request.POST.get("message", "").strip()
    consent = request.POST.get("consent")


    # -----------------------------------------
    # Validate required fields
    # -----------------------------------------

    if not email:
        return JsonResponse({
            "success": False,
            "message": "Please enter your email address."
        }, status=400)

    if not phone:
        return JsonResponse({
            "success": False,
            "message": "Please enter your phone number."
        }, status=400)


    # -----------------------------------------
    # Privacy consent
    # -----------------------------------------

    if consent != "true":
        return JsonResponse({
            "success": False,
            "message": (
                "Please agree to the Privacy Policy "
                "before continuing."
            )
        }, status=400)


    # -----------------------------------------
    # Validate visitor email
    # -----------------------------------------

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({
            "success": False,
            "message": "Please enter a valid email address."
        }, status=400)


    # -----------------------------------------
    # Validate input lengths
    # -----------------------------------------

    if len(phone) > 30:
        return JsonResponse({
            "success": False,
            "message": "Your phone number is too long."
        }, status=400)

    if len(message) > 3000:
        return JsonResponse({
            "success": False,
            "message": (
                "Your message is too long. "
                "Please keep it below 3,000 characters."
            )
        }, status=400)


    # -----------------------------------------
    # Prepare notification email
    # -----------------------------------------

    email_subject = "Website Donation Enquiry"

    email_body = f"""\
New donation enquiry received from the
Christ Promise Children's Home website.

----------------------------------------
Donor Information
----------------------------------------

Email:
{email}

Phone:
{phone}

----------------------------------------
Message
----------------------------------------

{message or "(No message provided)"}

----------------------------------------

Reply to:
{email}

Submitted through:
https://christpromisehome.com
"""


    # -----------------------------------------
    # Send email
    # -----------------------------------------

    try:

        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )

    except Exception:
        logger.exception(
            "Failed to send Christ Promise Children's Home "
            "donation enquiry email."
        )

        return JsonResponse({
            "success": False,
            "message": (
                "We couldn't send your enquiry right now. "
                "Please try again in a few minutes."
            )
        }, status=500)


    # -----------------------------------------
    # Success
    # -----------------------------------------

    return JsonResponse({
        "success": True,
        "message": (
            "We have received your donation enquiry. "
            "We will get back to you within a few hours."
        )
    }, status=200)