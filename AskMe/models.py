from django.contrib.auth.models import User
from django.db import models


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by("-likes")

    def new(self):
        return self.order_by("-date")


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    text = models.CharField(max_length=400, null=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name} answer"


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tag_name}"


class Profile(models.Model):
    #user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, null=True, blank=True)


class Like(models.Model):
    count = models.IntegerField(default=0)
    # user = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    answers_count = models.IntegerField(default=0)
    # answers = models.CharField(max_length=200)
    answers = models.ManyToManyField('Answer', null=True, blank=True, related_name='questions')
    # tags = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tag', related_name='questions')
    likes = models.ForeignKey('Like', on_delete=models.CASCADE, default=Like)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = QuestionManager()
