from datetime import date

from django.db import models
from django.contrib.auth import get_user_model

from apps.files.models import File
from apps.utils.language import sample_analyze_sentiment

class Diary(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    voice_file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    like = models.ManyToManyField(get_user_model(), related_name='likes')
    created_at = models.DateField(default=date.today)
    title = models.CharField(default='음성일기', max_length=256)
    content = models.TextField()
    score = models.FloatField()
    magnitude = models.FloatField()

    
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.author.username + self.title
    
    def _like(self, user):
        self.like.add(user)
    
    def _unlike(self, user):
        self.like.remove(user)

    def update_score(self):
        sentiment = sample_analyze_sentiment(self.content)
        self.score = sentiment[0]
        self.magnitude = sentiment[1]
        self.save()
        