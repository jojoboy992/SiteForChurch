import tempfile
from django import forms
from moviepy.editor import VideoFileClip
from .models import Post
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'video', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content...'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        # Check for both image and video
        if image and video:
            raise forms.ValidationError("You cannot post both a video and an image at the same time!")

        # Check for neither image nor video
        if not image and not video:
            raise forms.ValidationError("You must upload either an image or a video!")

        # Title length validation
        if title:
            if len(title) < 15 or len(title) > 21:
                raise forms.ValidationError(f"Title must be between 15 and 21 characters. {len(title)}")

        # Content length validation
        if content:
            if len(content) < 50 or len(content) > 100:
                raise forms.ValidationError(f"Content must be between 50 and 100 characters. Current length: {len(content)}")

        # Check image size
        if isinstance(image, InMemoryUploadedFile):
            img = PILImage.open(image)
            width, height = img.size
            min_width = 1080
            min_height = 566
            
            if width < min_width or height < min_height:
                raise forms.ValidationError(f"Image must be at least {min_width}x{min_height} pixels.")

        # Video length check
        if video:
            # Save the video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(video.read())
                temp_file_path = temp_file.name

            try:
                # Open the temp file in read-only mode for moviepy
                with VideoFileClip(temp_file_path) as clip:
                    duration = clip.duration
                    if duration > 60:
                        raise forms.ValidationError("Video cannot be longer than 1 minute!")
            except Exception as e:
                raise forms.ValidationError(f"Error processing video: {e}")
            finally:
                # Clean up the temporary file
                import os
                os.remove(temp_file_path)

        return cleaned_data
