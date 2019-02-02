from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def index(request):
    return render(request, "home.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")


def send_to_login(request):
    return redirect("/login")
