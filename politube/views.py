import random
from django.shortcuts import render

from pleniere.models import Pleniere, Deputy

def home(request):
    plenary = Pleniere.objects.latest('')
    deputy = random.choice(Deputy.objects.all())
    return render(request, 'home.html', { 'plenary': plenary, 'deputy': deputy })
