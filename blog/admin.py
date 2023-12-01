from django.contrib import admin
from .models import Blog, Comment

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author',
        'image',
        'image_alt',
        'content',
        'category',
        'created_on',
        'status',
        'excerpt',
        'updated_on',
    )

    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'commenter', 'body', 'approved', 'created_on')
    list_filter = ('approved', 'blog__title', 'commenter__username')
    actions = ['approve_comments']

    def approve_comments(modeladmin, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"