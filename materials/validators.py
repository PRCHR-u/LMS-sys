from rest_framework.serializers import ValidationError

class YoutubeURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get(self.field)
        if video_url and 'youtube.com' not in video_url:
            raise ValidationError('Only YouTube links are allowed.')
