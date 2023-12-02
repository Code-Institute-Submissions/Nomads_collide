from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils.text import slugify
from django.shortcuts import render

# Create your models here.

CATEGORY = (
    ('albania', 'Albania'),
    ('andorra', 'Andorra'),
    ('austria', 'Austria'),
    ('belarus', 'Belarus'),
    ('belgium', 'Belgium'),
    ('bosnia-and-herzegovina', 'Bosnia and Herzegovina'),
    ('bulgaria', 'Bulgaria'),
    ('croatia', 'Croatia'),
    ('cyprus', 'Cyprus'),
    ('czech-republic', 'Czech Republic'),
    ('denmark', 'Denmark'),
    ('estonia', 'Estonia'),
    ('finland', 'Finland'),
    ('germany', 'Germany'),
    ('greece', 'Greece'),
    ('hungary', 'Hungary'),
    ('iceland', 'Iceland'),
    ('ireland', 'Ireland'),
    ('italy', 'Italy'),
    ('kosovo', 'Kosovo'),
    ('latvia', 'Latvia'),
    ('liechtenstein', 'Liechtenstein'),
    ('lithuania', 'Lithuania'),
    ('luxembourg', 'Luxembourg'),
    ('malta', 'Malta'),
    ('moldova', 'Moldova'),
    ('monaco', 'Monaco'),
    ('montenegro', 'Montenegro'),
    ('netherlands', 'Netherlands'),
    ('north-macedonia', 'North Macedonia'),
    ('norway', 'Norway'),
    ('poland', 'Poland'),
    ('portugal', 'Portugal'),
    ('romania', 'Romania'),
    ('russia', 'Russia'),
    ('san-marino', 'San Marino'),
    ('serbia', 'Serbia'),
    ('slovakia', 'Slovakia'),
    ('slovenia', 'Slovenia'),
    ('spain', 'Spain'),
    ('sweden', 'Sweden'),
    ('switzerland', 'Switzerland'),
    ('ukraine', 'Ukraine'),
    ('united-kingdom', 'United Kingdom'),
    ('vatican-city', 'Vatican City'),

)

STATUS = ((0, "Draft"), (1, "Published"))


class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="blog_owner")
    image = ResizedImageField(size=[400, None], quality=75, upload_to='blogs/', force_format='WEBP', blank=False, null=False)
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY, default='albania')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"The title of this blog is {self.title}"

    class Meta:
        ordering = ["-created_on"]

def blog_categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/blog_categories.html', {'categories': categories})

#class Comment(models.Model):
#    post = models.ForeignKey(
#        Blog, on_delete=models.CASCADE, related_name="comments")
#    author = models.ForeignKey(
#        User, on_delete=models.CASCADE, related_name="commenter")
#    body = models.TextField()
#    approved = models.BooleanField(default=False)
#    created_on = models.DateTimeField(auto_now_add=True)

#    class Meta:
#        ordering = ["-created_on"]

#    def __str__(self):
#        return f"Comment {self.body} by {self.author}"

#    def save(self, *args, **kwargs):
#         if not self.author_id:
#            self.author = User.objects.get(username='your_logged_in_username')  # Replace with the appropriate way to get the current user
#        super().save(*args, **kwargs)

