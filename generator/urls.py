from django.urls import path
from .views import (
    home,
    preset_list,
    preset_detail,
    preset_create,
    preset_edit,
    preset_delete,
    test_create,
    test,
    history_view
)

app_name = 'generator'
urlpatterns = [
    path('presets/', preset_list, name='preset_list'),
    path('presets/<str:slug>/', preset_detail, name='preset_detail'),
    path('preset/create/', preset_create, name='preset_create'),
    path('preset/edit/<str:slug>/', preset_edit, name='preset_edit'),
    path('preset/delete/<str:slug>/', preset_delete, name='preset_delete'),
    path('test/create/', test_create, name='test_create'),
    path('test/<str:slug>/', test, name='test'),
    path('history/', history_view, name='history'),
    path('', home, name='home')
]