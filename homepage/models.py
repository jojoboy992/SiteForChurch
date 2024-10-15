from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=21, help_text="Maximum 30 characters.")
    content = models.TextField(help_text="Maximum 150 characters.")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Set published to True when creating a new post
        if self.pk is None:  # Check if the object is new (not saved to the database yet)
            self.published = True
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
