from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'user',
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