from django.urls import path
from .views import (
    home,
    preset_list,
    preset_detail,
    preset_create,
    preset_edit,
    test,
    history_view
)

app_name = 'generator'
urlpatterns = [
    path('presets/', preset_list, name='preset_list'),
    path('presets/<str:id>/', preset_detail, name='preset_detail'),
    path('preset_create/', preset_create, name='preset_create'),
    path('preset_edit/<str:id>/', preset_edit, name='preset_edit'),
    path('test/<str:id>/', test, name='test'),
    # path('history/<str:id>/', history_view, name='history_create'),
    path('history/', history_view, name='history'),
    path('', home, name='home')
]