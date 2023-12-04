from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views.generic import (CreateView, ListView, 
DetailView, DeleteView, UpdateView)
from .models import Blog
#Comment
from .forms import BlogForm
#CommentForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Create your views here.

class AddPost(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'blog/add_post.html'
    model = Blog
    form_class = BlogForm
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddPost, self).form_valid(form)

    def test_func(self):
        # Check if the user is a staff member
        return self.request.user.is_staff

class BlogCategories(ListView):
    '''view all blogs'''
    template_name='blog/blog_categories.html'
    model = Blog
    context_object_name='blogs'
    

class ViewBlog(DetailView):
    '''view a single blog'''
    template_name='blog/view_blog.html'
    model = Blog
    context_object_name='blog'

class EditBlog(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/edit_blog.html'
    model = Blog
    fields = ['title', 'image', 'image_alt', 'content', 'category', 'status', 'excerpt',]
    success_url = '/blog/'

    def test_func(self):
        return self.request.user == self.get_object().user

class DeleteBlog(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a blog"""
    model = Blog
    success_url = '/blog/'

    def test_func(self):
        return self.request.user == self.get_object().user

def blog_home(request):
    recent_posts = Blog.objects.filter(status=1).order_by('-created_on')[:3]
    return render(request, 'blog/index.html', {'recent_posts': recent_posts})