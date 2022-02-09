from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import app_settings

def service_worker(request):
    print(request)
    response = HttpResponse(
        open(app_settings.PWA_SERVICE_WORKER_PATH).read(), 
        content_type='application/javascript'
    )
    return response
    # TODO: Request to add this line
    # return render(request, 'serviceworker.js', {}, content_type='application/javascript')


def manifest(request):
    print(request)
    return render(request, 'manifest.json', {
        setting_name: getattr(app_settings, setting_name)
        for setting_name in dir(app_settings)
        if setting_name.startswith('PWA_')
    }, content_type='application/json')


def offline(request):
    print(request)
    print('Custom Offline Page...')
    # return redirect('custom_auth:account_view')
    return render(request, "offline.html")
