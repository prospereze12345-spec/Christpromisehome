
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