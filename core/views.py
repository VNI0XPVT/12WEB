import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
from .models import Profile


def login_page(request):
    return render(request, "login.html")


def send_otp(request):

    email = request.POST.get("email")
    password = request.POST.get("password")

    user, created = User.objects.get_or_create(username=email, email=email)

    if created:
        user.set_password(password)
        user.save()

    otp = str(random.randint(100000, 999999))

    profile = Profile.objects.get(user=user)
    profile.otp = otp
    profile.save()

    print("OTP:", otp)  # demo — email me send karna real site me

    request.session["user_id"] = user.id
    return render(request, "otp.html")


def verify_otp(request):

    otp = request.POST.get("otp")
    user = User.objects.get(id=request.session["user_id"])
    profile = Profile.objects.get(user=user)

    if profile.otp == otp:
        login(request, user)
        return redirect("/dashboard/")
    else:
        return redirect("/")
