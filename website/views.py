
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
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


def contact(request):
    return render(request, "website/contact.html")


@require_POST
def send_contact_message(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    consent = request.POST.get("consent")

    # Validate required fields
    if not name or not email or not subject or not message:
        return JsonResponse(
            {
                "message": "Please complete all required fields."
            },
            status=400
        )

    # Privacy consent
    if consent != "true":
        return JsonResponse(
            {
                "message": "Please agree to the Privacy Policy before sending your message."
            },
            status=400
        )

    # Basic email validation
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {
                "message": "Please enter a valid email address."
            },
            status=400
        )

    # Prevent excessively large submissions
    if len(name) > 100:
        return JsonResponse(
            {"message": "Name is too long."},
            status=400
        )

    if len(subject) > 200:
        return JsonResponse(
            {"message": "Subject is too long."},
            status=400
        )

    if len(message) > 5000:
        return JsonResponse(
            {"message": "Message is too long."},
            status=400
        )

    # Email sent to the orphanage mailbox
    recipient = settings.CONTACT_EMAIL

    email_subject = f"Website Contact: {subject}"

    email_body = f"""
New message received from the Christ Promise Children's Home website.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

-----------------------------------
This message was submitted through:
https://christpromisehome.com
"""

    try:

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[email],
        )

        email_message.send(fail_silently=False)

    except Exception:
        return JsonResponse(
            {
                "message": (
                    "Our mail service is temporarily unavailable. "
                    "Please try again in a few minutes."
                )
            },
            status=500
        )

    return JsonResponse(
        {
            "success": True,
            "message": (
                "We have received your message. "
                "We will get back to you within a few hours."
            )
        },
        status=200
    )