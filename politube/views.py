import random
from django.shortcuts import render

from pleniere.models import Pleniere, Deputy

def home(request):
    args = {}

    try:
      args['plenary'] = Pleniere.objects.latest()
    except Pleniere.DoesNotExist:
        pass

    deputies = Deputy.objects.all()
    if len(deputies) > 0:
        args['deputy'] = random.choice(deputies)

    return render(request, 'home.html', args)
