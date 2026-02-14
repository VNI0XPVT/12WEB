
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
 print("OTP:", otp)

 request.session["user_id"] = user.id
 return render(request, "otp.html")

def verify_otp(request):
 otp = request.POST.get("otp")
 user = User.objects.get(id=request.session["user_id"])
 profile = Profile.objects.get(user=user)

 if profile.otp == otp:
  login(request, user)
  return redirect("/dashboard/")
 return redirect("/")

def dashboard(request):
 if not request.user.is_authenticated:
  return redirect("/")

 profile = Profile.objects.get(user=request.user)

 if not profile.is_active():
  return render(request, "subscription.html")

 if profile.wallet_balance < 100:
  return render(request, "wallet.html")

 return render(request, "dashboard.html", {
  "balance": profile.wallet_balance,
  "subscription": profile.subscription_expiry
 })

def activate_subscription(request):
 profile = Profile.objects.get(user=request.user)
 profile.subscription_expiry = timezone.now() + timedelta(days=30)
 profile.save()
 return redirect("/dashboard/")

def add_wallet(request):
 profile = Profile.objects.get(user=request.user)
 profile.wallet_balance += 100
 profile.save()
 return redirect("/dashboard/")
