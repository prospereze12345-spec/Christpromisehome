
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






import logging

import requests

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_POST


logger = logging.getLogger(__name__)


# ============================================================
# BREVO EMAIL HELPER
# ============================================================

def send_brevo_email(
    *,
    recipient_email,
    reply_to_email,
    subject,
    text_content,
):
    """
    Send a transactional email through the Brevo HTTP API.

    Brevo sends the email using the verified
    contact@christpromisehome.com sender.

    Replies go directly to the website visitor through
    the Reply-To address.
    """

    api_key = getattr(settings, "BREVO_API_KEY", "").strip()
    api_url = getattr(
        settings,
        "BREVO_API_URL",
        "https://api.brevo.com/v3/smtp/email",
    )

    sender_email = getattr(
        settings,
        "BREVO_SENDER_EMAIL",
        "contact@christpromisehome.com",
    )

    sender_name = getattr(
        settings,
        "BREVO_SENDER_NAME",
        "Christ Promise Children's Home",
    )

    timeout = getattr(settings, "BREVO_TIMEOUT", 15)

    # --------------------------------------------------------
    # Configuration validation
    # --------------------------------------------------------

    if not api_key:
        raise RuntimeError(
            "BREVO_API_KEY is not configured."
        )

    if not recipient_email:
        raise RuntimeError(
            "Brevo recipient email is missing."
        )

    if not sender_email:
        raise RuntimeError(
            "Brevo sender email is missing."
        )

    # --------------------------------------------------------
    # Brevo API request
    # --------------------------------------------------------

    payload = {
        "sender": {
            "name": sender_name,
            "email": sender_email,
        },
        "to": [
            {
                "email": recipient_email,
            }
        ],
        "replyTo": {
            "email": reply_to_email,
        },
        "subject": subject,
        "textContent": text_content,
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    try:
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=timeout,
        )

    except requests.Timeout as exc:
        logger.exception(
            "Brevo API request timed out."
        )
        raise RuntimeError(
            "Brevo API request timed out."
        ) from exc

    except requests.RequestException as exc:
        logger.exception(
            "Brevo API request failed."
        )
        raise RuntimeError(
            "Unable to connect to the Brevo API."
        ) from exc

    # --------------------------------------------------------
    # Handle Brevo response
    # --------------------------------------------------------

    if not response.ok:
        # Log status and response body for server diagnostics.
        # NEVER log the API key.
        logger.error(
            "Brevo API returned HTTP %s: %s",
            response.status_code,
            response.text[:1000],
        )

        raise RuntimeError(
            f"Brevo API returned HTTP {response.status_code}."
        )

    # Brevo normally returns JSON containing messageId.
    try:
        response_data = response.json()
    except ValueError:
        response_data = {}

    logger.info(
        "Brevo email sent successfully. Message ID: %s",
        response_data.get("messageId", "unknown"),
    )

    return response_data


# ============================================================
# CONTACT FORM
# ============================================================

@require_POST
def send_contact_message(request):

    # --------------------------------------------------------
    # Get submitted form data
    # --------------------------------------------------------

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    consent = request.POST.get("consent")


    # --------------------------------------------------------
    # Validate required fields
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Privacy consent
    # --------------------------------------------------------

    if consent != "true":
        return JsonResponse({
            "success": False,
            "message": (
                "Please agree to the Privacy Policy "
                "before sending your message."
            )
        }, status=400)


    # --------------------------------------------------------
    # Validate visitor email
    # --------------------------------------------------------

    try:
        validate_email(email)

    except ValidationError:
        return JsonResponse({
            "success": False,
            "message": "Please enter a valid email address."
        }, status=400)


    # --------------------------------------------------------
    # Validate input lengths
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Normalize subject
    # --------------------------------------------------------

    subject = " ".join(subject.split())

    email_subject = f"Website Contact: {subject}"


    # --------------------------------------------------------
    # Prepare email body
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Send through Brevo
    # --------------------------------------------------------

    try:

        send_brevo_email(
            recipient_email=settings.CONTACT_EMAIL,
            reply_to_email=email,
            subject=email_subject,
            text_content=email_body,
        )

    except Exception:
        logger.exception(
            "Failed to send Christ Promise Children's Home "
            "contact form email through Brevo."
        )

        return JsonResponse({
            "success": False,
            "message": (
                "We couldn't send your message right now. "
                "Please try again in a few minutes."
            )
        }, status=500)


    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    return JsonResponse({
        "success": True,
        "message": (
            "We have received your message. "
            "We will get back to you within a few hours."
        )
    }, status=200)


# ============================================================
# DONATION ENQUIRY FORM
# ============================================================

@require_POST
def send_donation_enquiry(request):

    # --------------------------------------------------------
    # Get submitted form data
    # --------------------------------------------------------

    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    message = request.POST.get("message", "").strip()
    consent = request.POST.get("consent")


    # --------------------------------------------------------
    # Validate required fields
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Privacy consent
    # --------------------------------------------------------

    if consent != "true":
        return JsonResponse({
            "success": False,
            "message": (
                "Please agree to the Privacy Policy "
                "before continuing."
            )
        }, status=400)


    # --------------------------------------------------------
    # Validate visitor email
    # --------------------------------------------------------

    try:
        validate_email(email)

    except ValidationError:
        return JsonResponse({
            "success": False,
            "message": "Please enter a valid email address."
        }, status=400)


    # --------------------------------------------------------
    # Validate input lengths
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Prepare email
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Send through Brevo
    # --------------------------------------------------------

    try:

        send_brevo_email(
            recipient_email=settings.CONTACT_EMAIL,
            reply_to_email=email,
            subject=email_subject,
            text_content=email_body,
        )

    except Exception:
        logger.exception(
            "Failed to send Christ Promise Children's Home "
            "donation enquiry email through Brevo."
        )

        return JsonResponse({
            "success": False,
            "message": (
                "We couldn't send your enquiry right now. "
                "Please try again in a few minutes."
            )
        }, status=500)


    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    return JsonResponse({
        "success": True,
        "message": (
            "We have received your donation enquiry. "
            "We will get back to you within a few hours."
        )
    }, status=200)