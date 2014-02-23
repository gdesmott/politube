import random
from django.shortcuts import render

from plenary.models import Plenary, Deputy

def home(request):
    args = {}

    try:
      args['plenary'] = Plenary.objects.latest()
    except Plenary.DoesNotExist:
        pass

    deputies = Deputy.objects.all()
    if len(deputies) > 0:
        args['deputy'] = random.choice(deputies)

    return render(request, 'home.html', args)

def about(request):
    return render(request, 'about.html')
