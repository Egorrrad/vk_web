from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    image = models.CharField(max_length=200)
    answers_count = models.IntegerField()
    answers = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)
