from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def game(request):
    c = {}
    if request.method == "GET":
        return render_to_response('game.html', c)
    if request.method == "POST":
        print("posted game")