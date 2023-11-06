import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from AskMe.models import *


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными данными'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help=u'Количество создаваемых объектов')

    def handle(self, *args, **kwargs):
        """
        пользователей — равное ratio;
вопросов — ratio * 10;
ответы — ratio * 100;
тэгов - ratio;
оценок пользователей - ratio * 200;
        """
        total = kwargs['ratio']

        for i in range(total):
            try:
                User.objects.create_user(username=get_random_string(length=10), email='', password='123',
                                         first_name=get_random_string(length=10))

                Tag.objects.get_or_create(tag_name=get_random_string(length=5))
            except Exception as e:
                continue

        for i in range(total * 10):
            try:
                Question.objects.create(title=get_random_string(length=15), user_id=random.randint(1, total),
                                        content=get_random_string(length=200))
            except Exception as e:
                continue

        for i in range(random.randint(1, total * 100)):
            try:
                user = User.objects.get(id=random.randint(1, total))
                item = Question.objects.get(id=random.randint(1, total))
                item.answers.create(text=get_random_string(length=100), user=user)
            except Exception as e:
                continue

        for i in range(total * 200):
            try:
                user = User.objects.get(id=random.randint(1, total))
                item = Question.objects.get(id=random.randint(1, total))
                question_model_type = ContentType.objects.get_for_model(item)
                # добавление лайка
                Like.objects.create(content_type=question_model_type, object_id=item.id, user=user)
            except Exception as e:
                continue
