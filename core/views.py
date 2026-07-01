from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

@login_required
def home(request):
    services = getattr(settings, 'SERVICES', [])
    return render(request, 'core/list.html', {'services': services})