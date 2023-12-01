from django.urls import path
from .views import AddPost, BlogCategories, ViewBlog, edit_comment, delete_comment

urlpatterns = [
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('blog_categories/', BlogCategories.as_view(), name='blog_categories'),
    path("blog/view_blog/", ViewBlog.as_view(), name='view_blog'),
    path('blog/<slug:slug>/edit_comment/<int:comment_id>', edit_comment, name='edit_comment'),
    path('blog/<slug:slug>/delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
]
