from django.shortcuts import render
from .models import Topic

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