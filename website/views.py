
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