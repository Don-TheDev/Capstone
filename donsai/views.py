from django.shortcuts import redirect
from django.views.generic.base import RedirectView


def index(request):
    return redirect('/donsai/omnichat/')


def web(request):
    return redirect('/donsai/omnichat/')


def api(request):
    return redirect('/donsai/omnichat/')
