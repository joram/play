from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.profile.forms import ProfileForm


@login_required
def view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect("profile")
    else:
        form = ProfileForm(initial={"email": request.user.email})

    return render(request, "profile/view.html", {"form": form})
