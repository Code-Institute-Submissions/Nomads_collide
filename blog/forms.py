from django import forms
from .models import Blog
#Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        form_class = Blog
        fields = [
            'title',
            'image',
            'image_alt',
            'content',
            'category',
            'status',
            'excerpt',
            ]
                  
        labels = {
            'title': 'Blog title',
            'image': 'Blog image',
            'image_alt': 'Describe image',
            'content': 'Blog content',
            'category': 'Country',
            'status': 'Publish or Draft',
            'excerpt': 'Blog description',
            }


    def save(self, commit=True):
        instance = super(BlogForm, self).save(commit=False)

        # Prepopulate the slug based on the title
        instance.slug = instance.title.lower().replace(' ', '-')

        if commit:
            instance.save()

        return instance

#class CommentForm(forms.ModelForm):
#    class Meta:
#        model = Comment
#        fields = ('body',)