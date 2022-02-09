# from django.conf.urls import url
# TODO: Import re_path and update urlpatterns (request for changes already made by others)
from django.urls import re_path, path

from .views import manifest, service_worker, offline

# Serve up serviceworker.js and manifest.json at the root
urlpatterns = [
    re_path(r'^serviceworker\.js$', service_worker, name='serviceworker'),
    re_path(r'^manifest\.json$', manifest, name='manifest'),
    re_path(r'^offline/$', offline, name='offline')
]
