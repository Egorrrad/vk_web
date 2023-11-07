from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class QuestionManager(models.Manager):
    def hot(self):
        return self.order_by("-likes")

    def new(self):
        return self.order_by("-created")


def user_directory_path(instance, filename):
    return 'user_{0}/ {1}'.format(instance.user.id, filename)


class Like(models.Model):
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=400, null=False, blank=False)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=400, null=False, blank=False)
    likes = GenericRelation(Like)
    accepted = models.BooleanField(default=False)
    comments = models.ManyToManyField('Comment', null=True, blank=True, related_name='answers')

    def __str__(self):
        return f"{self.user.first_name} answer"


class Tag(models.Model):
    tag_name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return f"{self.tag_name}"

    @property
    def total_tags(self):
        return self.questions.count()


class Profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)
    # answers_count = models.IntegerField(default=0)
    # answers = models.CharField(max_length=200)
    answers = models.ManyToManyField('Answer', null=True, blank=True, related_name='questions')
    # tags = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tag', related_name='questions')
    # likes = models.ManyToManyField('Like', null=True, blank=True, related_name='questions')
    likes = GenericRelation(Like)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    @property
    def total_likes(self):
        return self.likes.count()
