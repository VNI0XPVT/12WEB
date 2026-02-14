from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page),
    path("send-otp/", views.send_otp),
    path("verify-otp/", views.verify_otp),
    path("dashboard/", views.dashboard),
    path("activate-subscription/", views.activate_subscription),
    path("add-wallet/", views.add_wallet),
]
