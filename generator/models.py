from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# from django.contrib.auth import get_user_model
from django.conf import settings

USER = settings.AUTH_USER_MODEL

class Topic(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class SubTopic(models.Model):
    title        = models.CharField(max_length=100, unique=True)
    parent_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Preset(models.Model):

    class TimerChoices(models.TextChoices):
        STOPWATCH = 'SW', _('stopwatch')
        COUNTDOWN = 'CD', _('countdown')

    class DifficultyChoices(models.TextChoices):
        EASY = 'EASY', _('easy')
        NORMAL = 'NORMAL', _('normal')
        HARD = 'HARD', _('hard')
        MIXED = 'MIXED', _('mixed')

    user            = models.ForeignKey(USER, on_delete=models.CASCADE)
    title           = models.CharField(max_length=100)  # TODO: Check for duplicate titles/slugs in views.py
    slug            = models.SlugField(max_length=100, blank=True, null=True)  # Slugify in the save method
    question_count  = models.IntegerField(default=5, blank=True, null=True)

    difficulty = models.CharField(
        max_length=6,
        choices=DifficultyChoices.choices,
        default=DifficultyChoices.EASY,
        blank=True,
        null=True
    )

    topics      = models.ManyToManyField(Topic)
    sub_topics  = models.ManyToManyField(SubTopic)
    timer       = models.BooleanField(default=False, blank=True, null=True)

    timer_type = models.CharField(
        max_length=9,
        choices=TimerChoices.choices,
        default=TimerChoices.STOPWATCH,
        blank=True,
        null=True
    )

    timer_length    = models.IntegerField(blank=True, null=True)
    best_record     = models.IntegerField(blank=True, null=True)

    # TODO: Added average_time field (update views.py & html files) 
    average_time    = models.IntegerField(blank=True, null=True)
    date_created    = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_modified   = models.DateTimeField(auto_now=True, blank=True, null=True)  # auto-now?

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Preset, self).save(*args, **kwargs)


class History(models.Model):
    user                = models.ForeignKey(USER, on_delete=models.CASCADE)
    preset              = models.ForeignKey(Preset, on_delete=models.SET_NULL, null=True, blank=True)
    score               = models.IntegerField()
    time_completed_in   = models.IntegerField()  # Milliseconds
    date_created        = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.date_created)