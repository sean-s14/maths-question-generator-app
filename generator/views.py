from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import JsonResponse
import json

from .models import Topic, SubTopic, Preset, History
from .forms import PresetForm, HistoryForm
# from django.core.paginator import Paginator
from maths_question_generator import basic_arithmetic

def home(request):
    topics = Topic.objects.all()
    # print(topics[0]._meta.get_fields())
    context = {'active': 'home', 'topics': topics}
    return render(request, 'generator/home.html', context)


@login_required
def preset_list(request):
    presets = Preset.objects.filter(user=request.user)
    context = {'active': 'presets', 'presets': presets}
    return render(request, 'generator/preset_list.html', context)


@login_required
def preset_detail(request, id):
    preset = get_object_or_404(Preset, pk=id)
    context = {'preset': preset}
    return render(request, 'generator/preset_detail.html', context)


@login_required
def preset_create(request):
    context = {}

    if request.method == 'POST':
        form = PresetForm(request.POST)
        form_topics = form['topics'].value()
        form_sub_topics = form['sub_topics'].value()

        if not (form_topics or form_sub_topics):
            messages.error(request,'You must select a topic')
            return redirect('/preset_create/')

        if form.is_valid():
            print('Form is valid!')
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/preset_create/')

        else:
            print('Form is NOT valid...')
    
    else:
        form = PresetForm()
        topics = Topic.objects.all()
        sub_topics = SubTopic.objects.all()
        context = {'topics': topics, 'sub_topics': sub_topics}

    context = {**context, 'active': 'preset_create', 'form': form}
    return render(request, 'generator/preset_create.html', context)


@login_required
def preset_edit(request, id):
    context = {}
    preset = Preset.objects.get(id=id)

    if request.method == 'POST':
        form = PresetForm(request.POST, instance=preset)
        form_topics = form['topics'].value()
        form_sub_topics = form['sub_topics'].value()

        if not (form_topics or form_sub_topics):
            # Generate error messages
            messages.error(request,'You must select a topic')
            return redirect(f'/preset_edit/{id}')

        if form.is_valid():
            print('Form is valid!')
            form.save()
            return redirect(f'/presets/{id}/')

        print('Form is NOT valid...')
    
    else:
        form = PresetForm(instance=preset)
        # TODO: Add topics and sub-topics to context
        # Use jQuery to select the options on the rendered form that
        # correspond to the selected topic/sub-topic
        topics = Topic.objects.all()
        sub_topics = SubTopic.objects.all()
        context = {'topics': topics, 'sub_topics': sub_topics, 'form': form}

    context = {**context, 'preset': preset}
    return render(request, 'generator/preset_create.html', context)

# TODO: Make two seperate test urls (one for logged in users one for anonymous users)
def test(request, id):
    preset = get_object_or_404(Preset, pk=id)

    sub_topics = [sub_topic['title'] for sub_topic in preset.sub_topics.values()]

    add = True if 'Addition' in sub_topics else False
    sub = True if 'Subtraction' in sub_topics else False
    mul = True if 'Multiplication' in sub_topics else False
    div = True if 'Division' in sub_topics else False

    questions = []
    while len(questions) < preset.question_count:
        q_and_a = basic_arithmetic(
        add=add,
        sub=sub,
        mul=mul,
        div=div,
        min_res=0,
        max_res=1000
        )
        questions.append(q_and_a)


    context = {'questions': questions, 'preset': preset}
    return render(request, 'generator/test.html', context)


@login_required
def history_view(request):

    if request.method == 'POST':
        json_request = json.loads(request.body)
        form = HistoryForm(json_request)
        
        if form.is_valid():
            print('Form is valid!')
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return JsonResponse({'response': 'Success!'})
        else:
            print('Form is NOT valid...')
            return JsonResponse({'response': 'Failure...'})
    
    history = History.objects.all().order_by('-date_created')
    context = {'history': history}
    return render(request, 'generator/history.html', context)