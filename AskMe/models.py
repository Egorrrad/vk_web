from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=100, default = " ")
    content = models.CharField(max_length=3000, default = " ")
    image = models.CharField(max_length=200, default = " ")
    answers_count = models.IntegerField()
    answers = models.CharField(max_length=200, default = " ")
    tags = models.CharField(max_length=200, default = " ")
    likecount = models.IntegerField(default = 0)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)


