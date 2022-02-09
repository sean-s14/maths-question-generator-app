from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Json
from django.http import JsonResponse
import json

# My Stuff
from .models import Topic, SubTopic, Preset, History
from .forms import PresetForm, HistoryForm, TestForm
from .utils import generate_questions


def home(request):
    topics = Topic.objects.all()
    # print(topics[0]._meta.get_fields())
    context = {'active': 'home', 'topics': topics}
    return render(request, 'generator/home.html', context)


@login_required
def preset_list(request):
    presets = Preset.objects.filter(user=request.user).order_by('-date_modified')
    context = {'active': 'presets', 'presets': presets}
    return render(request, 'generator/preset_list.html', context)


@login_required
def preset_detail(request, slug):
    preset = get_object_or_404(Preset, slug=slug)
    context = {'preset': preset}
    return render(request, 'generator/preset_detail.html', context)


@login_required
def preset_create(request):
    context = {}

    if request.method == 'POST':
        form = PresetForm(request.POST)
        form_topics = form['topics'].value()
        form_sub_topics = form['sub_topics'].value()
        print(request.POST.get('begin'))

        if not (form_topics or form_sub_topics):
            messages.error(request,'You must select a topic')
            return redirect('generator:preset_create')

        if form.is_valid():
            print('Form is valid!')

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()

            messages.success(request, 'New topic created!')

            if request.POST.get('begin') == 'Save & Begin Test':
                return redirect('generator:test', slug=instance.slug)

            return redirect('generator:preset_list')

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
def preset_edit(request, slug):
    context = {}
    preset = Preset.objects.get(slug=slug)

    if request.method == 'POST':
        form = PresetForm(request.POST, instance=preset)
        form_topics = form['topics'].value()
        form_sub_topics = form['sub_topics'].value()

        if not (form_topics or form_sub_topics):
            # Generate error messages
            messages.error(request,'You must select a topic')
            return redirect('generator:preset_edit', slug=slug)

        if form.is_valid():
            print('Form is valid!')
            form.save()
            return redirect('generator:preset_detail', slug=slug)

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


@login_required
def preset_delete(request, slug):
    # TODO: Verify that user owns preset
    preset = None
    if request.method == 'POST':
        try:
            preset = Preset.objects.get(slug=slug)
            title = preset.title
            preset.delete()
            messages.success(request, f'Preset {title} has been deleted')
            return redirect('generator:preset_list')
        except Preset.DoesNotExist as e:
            print(e)
    
    messages.error(request, 'Unable to delete preset that does not exist')
    return redirect('generator:preset_detail', slug=slug)


# TODO: Make two seperate test urls (one for logged in users one for anonymous users)
@login_required
def test(request, slug):
    preset = get_object_or_404(Preset, slug=slug)

    sub_topics = preset.sub_topics.values()
    question_count = preset.question_count
    sub_topics = [sub_topic['title'] for sub_topic in sub_topics]
    questions = generate_questions(question_count=question_count, sub_topics=sub_topics)

    context = {'is_temp': False, 'questions': questions, 'preset': preset}
    return render(request, 'generator/test.html', context)


def test_create(request):
    context = {}

    if request.method == 'POST':
        form = TestForm(request.POST)
        
        if form.is_valid():
            questions   = form.cleaned_data.get('question_count')
            sub_topics  = form.cleaned_data.get('sub_topics')

            timer       = form.cleaned_data.get('timer')
            timer_type  = form.cleaned_data.get('timer_type')
            timer_length = form.cleaned_data.get('timer_length')

            sub_topics = [sub_topic.title for sub_topic in sub_topics]
            questions = generate_questions(questions, sub_topics)

            context = {'questions': questions}
            # TODO: Change this
            return render(request, 'generator/test.html', context)
    else:
        form = TestForm()
        topics = Topic.objects.all()
        sub_topics = SubTopic.objects.all()
        context = {'topics': topics, 'sub_topics': sub_topics}
        
    context = {**context, 'is_temp': True, 'form': form}
    return render(request, 'generator/preset_create.html', context)

@login_required
def history_view(request):

    print('History View was hit')

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
    
    print('Requesting history.html')
    history = History.objects.filter(user=request.user).order_by('-date_created')
    context = {'history': history}
    return render(request, 'generator/history.html', context)