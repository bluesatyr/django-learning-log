from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import EntryForm, TopicForm

def index(request):
    """The home page for the learning log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics"""
    topics = Topic.objects.order_by('date_added') # get Topics from the database and order by date_added
    context = {'topics': topics} # key referenced in template: data sent to the template (similar to React props) 
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added') # minus-sign sorts in reverse order
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No POST data submitted; create a blank form
        form = TopicForm()
    else: 
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs/new_topic.html')
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Add a new entry"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No POST data submitted; create a blank form
        form = EntryForm()
    else: 
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # create new_entry object but don't save to database yet
            new_entry = form.save(commit=False)
            # assign the topic to the object
            new_entry.topic = topic
            # update the database
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
