# home/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import Blog

class Index(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_posts = Blog.objects.filter(status=1).order_by('-created_on')[:3]
        context['recent_posts'] = recent_posts
        return context

    

