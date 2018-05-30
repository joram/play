from django.shortcuts import render


def create(request):
    return render(request, 'create.html')
