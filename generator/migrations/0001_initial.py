# Generated by Django 4.0.1 on 2022-01-25 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('parent_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True)),
                ('question_count', models.IntegerField(blank=True, default=5, null=True)),
                ('difficulty', models.CharField(blank=True, choices=[('EASY', 'easy'), ('NORMAL', 'normal'), ('HARD', 'hard'), ('MIXED', 'mixed')], default='EASY', max_length=6, null=True)),
                ('timer', models.BooleanField(blank=True, default=False, null=True)),
                ('timer_type', models.CharField(blank=True, choices=[('SW', 'stopwatch'), ('CD', 'countdown')], default='SW', max_length=9, null=True)),
                ('timer_length', models.IntegerField(blank=True, null=True)),
                ('best_record', models.IntegerField(blank=True, null=True)),
                ('average_time', models.IntegerField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('sub_topics', models.ManyToManyField(to='generator.SubTopic')),
                ('topics', models.ManyToManyField(to='generator.Topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('time_completed_in', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('preset', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='generator.preset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]