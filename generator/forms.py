from django.forms import ModelForm, widgets, TextInput
from django.utils.translation import gettext_lazy as _
from .models import Topic, SubTopic, Preset, History


class PresetForm(ModelForm):

    class Meta:
        model = Preset
        fields = (
            'title', 'question_count', 'difficulty', 'topics', 'sub_topics',
            'timer', 'timer_type', 'timer_length'
        )
        labels = {
            'question_count': _('Questions'),
            'sub_topics': _('Sub Topics'),
            'timer_type': _('Timer Type'),
            'timer_length': _('Timer Length')
        }


class HistoryForm(ModelForm):

    class Meta:
        model = History
        fields = ['preset', 'score', 'time_completed_in']