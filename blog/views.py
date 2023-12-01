from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView
from .models import Lessons, Comment
from .forms import LessonForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect



# Create your views here.


class AddLesson(LoginRequiredMixin, CreateView):
    template_name = 'lessons/add_lesson.html'
    model = Lessons
    form_class = LessonForm
    success_url = '/lessons'

    @method_decorator(permission_required('lessons.add_lessons', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except PermissionDenied:
            messages.error(self.request, "You don't have permission to access this page.")
            return HttpResponseRedirect('home')

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(AddLesson, self).form_valid(form)

class LessonList(ListView):
    '''view all lessons'''
    template_name='lessons/modules.html'
    model = Lessons
    context_object_name='lessons'

class LessonDetail(DetailView):
    '''view a single lesson'''
    template_name='lessons/lesson_detail.html'
    model = Lessons
    context_object_name='lesson'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        comments = lesson.comments.filter(approved=True).order_by("-created_on")
        comment_count = lesson.comments.filter(approved=True).count()
        comment_form = CommentForm()

        context["comments"] = comments
        context["comment_count"] = comment_count
        context["comment_form"] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.commenter = request.user
            comment.lesson = lesson
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

        return redirect('lesson_detail', slug=lesson.slug)

def edit_comment(request, slug, comment_id):
    """
    view to edit comments
    """
    if request.method == "POST":

        queryset = Lessons.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.commenter == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                'Error updating comment!')

    return HttpResponseRedirect(reverse('lesson_detail', args=[slug]))


def delete_comment(request, slug, comment_id):
    """
    view to delete comment
    """
    queryset = Lessons.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.commenter == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                            'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('lesson_detail', args=[slug]))