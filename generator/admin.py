from django.contrib import admin
from .models import Topic, SubTopic, Preset, History

admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Preset)
admin.site.register(History)