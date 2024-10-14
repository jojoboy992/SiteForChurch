from django import forms
from moviepy.editor import VideoFileClip
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title...'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        if image and video:
            raise forms.ValidationError("You cannot post both a video and an image at the same time!")

        if video:
            # Use the video file directly
            video_file = video.file  # This is a file-like object
            # Create a VideoFileClip directly from the file-like object
            try:
                with VideoFileClip(video_file.name) as clip:
                    duration = clip.duration  # Duration in seconds
                    if duration > 60:  # Check if the duration is greater than 60 seconds
                        raise forms.ValidationError("Video cannot be longer than 1 minute!")
            except Exception as e:
                raise forms.ValidationError(e)

        return cleaned_data
