from django.shortcuts import render
from django.views.generic import ListView
from .models import Posts

class PostListView(ListView):
    model = Posts
    # template_name = 'posts/list_view.html'
    template_name = 'index.html'
    context_object_name = 'posts'
