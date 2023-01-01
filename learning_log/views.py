from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .froms import TopicFroms, EntryFroms


# 创建你的视图


def index(request):
    return render(request, 'learning_log/index.html')


def topics(request):
    topics = Topic.objects.filter(owner=request.user.id).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_log/topics.html', context)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_log/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        from_ = TopicFroms()

    else:
        form_ = TopicFroms(data=request.POST)
        if form_.is_valid():
            new_topic = form_.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_log:new_topic')

    context = {'from': from_}
    return render(request, 'learning_log/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        from_ = EntryFroms()

    else:
        from_ = EntryFroms(data=request.POST)
        if from_.is_valid():
            new_entry = from_.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_log:topic', topic_id=topic_id)

    context = {'topic': topic, 'from': from_}
    return render(request, 'learning_log/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        from_ = EntryFroms(instance=entry)

    else:
        from_ = EntryFroms(instance=entry, data=request.POST)
        if from_.is_valid():
            from_.save()
            return redirect('learning_log:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'from': from_}
    return render(request, 'learning_log/edit_entry.html', context)
