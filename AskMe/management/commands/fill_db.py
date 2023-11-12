import random

from faker import Faker
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
        fake = Faker()
        # images_pack = "vk_web/static/img/test"
        last_user_id = 1
        el = User.objects.last()
        if el is not None:
            last_user_id = el.id
        last_tag_id = 1
        el = Tag.objects.last()
        if el is not None:
            last_tag_id = el.id

        for i in range(total):
            try:
                name = fake.name().split(" ")
                user = User.objects.create_user(username=get_random_string(length=10), email=fake.email(),
                                                password='123',
                                                first_name=name[0], last_name=name[1])
                filename = 'test/' + str(random.randint(1, 7)) + '.jpeg'
                profile = Profile.objects.get_or_create(user=user)[0]
                profile.image = filename
                profile.save()

                Tag.objects.get_or_create(tag_name=fake.country())
            except Exception as e:
                continue

        for i in range(total * 10):
            try:
                question = Question.objects.create(title=fake.city(),
                                                   user_id=random.randint(last_user_id, last_user_id + total),
                                                   content=fake.text())
                tag_elem = Tag.objects.get(id=random.randint(last_tag_id, last_tag_id + total))
                question.tags.add(tag_elem.id)
            except Exception as e:
                continue

        last_question_id = 1
        el = Question.objects.last()
        if el is not None:
            last_question_id = el.id

        for i in range(random.randint(1, total * 100)):
            try:
                user = User.objects.get(id=random.randint(last_user_id, last_user_id + total))
                item = Question.objects.get(id=random.randint(last_question_id, last_question_id + total))
                item.answers.create(text=fake.text(), user=user)
            except Exception as e:
                continue

        for i in range(total * 200):
            try:
                user = User.objects.get(id=random.randint(last_user_id, last_user_id + total))
                item = Question.objects.get(id=random.randint(last_question_id, last_question_id + total))
                question_model_type = ContentType.objects.get_for_model(item)
                # добавление лайка
                list = [-1, 1]
                if LikeDis.objects.filter(object_id=item.id, user=user).exists():
                    continue
                else:
                    LikeDis.objects.create(content_type=question_model_type, object_id=item.id, user=user,
                                           vote=list[random.randint(0, 1)])
            except Exception as e:
                continue
