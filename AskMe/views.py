import datetime
import math

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from AskMe.forms import *
from AskMe.models import *


def makeQuestion(id: int, title: str, image_path: str, content: str, answers_count: int, answers: list, tags: list):
    question = {
        "id": id,
        "title": title,
        "image": image_path,
        "content": content,
        "answers_count": answers_count,
        "answers": answers,
        "tags": tags
    }
    return question


questions = [
    {
        "id": i,
        "title": f"quesion {i}",
        "content": f"aaaaaaaa {i}",
        "image": "img/bobr.jpeg",
        "answers_count": i,
        "answers": ["aaaaa", "aaaaaa"],
        "tags": ["tag1", "tag2"]
    } for i in range(10)
]


def paginate(request, objects, per_page=5):
    result = None
    first = end = 1
    num_page = 1
    pages_pagination = []
    try:
        # лучше использовать метод get, иначе исключения ловить надо
        page = request.GET.get('page', 1)  # дефолтное значение для get
        # можно закинуть сюда request
        # добавить обработку отсутсвтия страницы
        paginator = Paginator(objects, per_page)
        result = paginator.page(page)

        num_page = int(page)
    except Exception as e:
        print(e)

    all_pages = math.ceil(len(objects) / per_page)

    # pages_pagination = [i for i in range(1, all_pages)]
    i = num_page
    count = 0
    if i < all_pages:
        while count < 3:
            pages_pagination.append(i)
            i += 1
            if i == all_pages:
                break
            count += 1

    # print(pages_pagination)
    if num_page == 1:
        first = None
    if num_page == all_pages:
        end = None

    return result, {"first": first, "end": end, "enditem": all_pages, "items": pages_pagination}


def isEmptyQuestions(request, questionslist, pages_counter):
    if questionslist is None:
        return render(
            request,
            'errors/not_found_page.html',
            context={'pages': pages_counter}
        )
    return 0


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    questions = Question.objects.new()
    questionslist, pages_counter = paginate(request, questions)

    result = isEmptyQuestions(request, questionslist, pages_counter)
    if result != 0:
        return result

    return render(
        request,
        'index.html',
        context={'questions': questionslist, 'pages': pages_counter}
    )


def ask(request):
    """
    Функция отображения страницы для создания вопроса.
    """

    try:
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = QuestionForm(request.POST)

            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                data = form.cleaned_data

                print(data)

                post_question1 = Question(title=data["title"], content=data["content"])
                # сначала сохраним
                post_question1.save()

                post_question1.tags.create(tag_name=data["tags"])
                id = post_question1.id

                return redirect(question, question_id=id)



        # if a GET (or any other method) we'll create a blank form
        else:
            form = QuestionForm()
            return render(
                request,
                'ask.html',
                {"form": form}
            )
    except Exception as e:
        print(e)


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(index)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')

    form = LoginForm()
    return render(
        request,
        'login.html', context={"form": form}
    )


def logout_user(request):
    logout(request)
    return redirect(login_user)


def question(request, question_id):
    # item = questions[question_id]
    item = Question.objects.get(id=question_id)
    form = AddAnswerForm()

    try:
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = AddAnswerForm(request.POST)
            # print(form)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                data = form.cleaned_data

                print(data)

                item.answers.create(text=data["answer"], user_id=1)



        # if a GET (or any other method) we'll create a blank form
        else:
            form = AddAnswerForm()
            return render(
                request,
                'question.html',
                context={'item': item, 'form': form}
            )
    except Exception as e:
        print(e)

    form = AddAnswerForm()
    return render(
        request,
        'question.html',
        context={'item': item, 'form': form}
    )


def settings(request):
    return render(
        request,
        'settings.html'
    )


def signup(request):
        if request.method == 'POST':
            user_form = RegisterForm(request.POST)
            if user_form.is_valid():
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()
                return redirect(index)
            else:
                return render(
                    request,
                    'signup.html', context={"form": user_form}
                    )

        form = RegisterForm()
        return render(
        request,
        'signup.html', context={"form": form}
        )


def tag(request, tag_name):
    questions_with_tag = []
    """
    for k in questions:
        if tag_name in k["tags"]:
            questions_with_tag.append(k)
             """
    questions_with_tag = Tag.objects.get(tag_name=tag_name).questions.all()

    if len(questions_with_tag) == 0:
        return render(
            request,
            'errors/not_found_tag.html',
            context={'tag': tag_name}
        )

    questionslist, pages_counter = paginate(request, questions_with_tag)
    result = isEmptyQuestions(request, questionslist, pages_counter)
    if result != 0:
        return result

    return render(
        request,
        'tag.html',
        context={'tag': tag_name, 'questions': questionslist, 'pages': pages_counter}
    )


def hot(request):
    questions = Question.objects.hot()
    questionslist, pages_counter = paginate(request, questions)
    result = isEmptyQuestions(request, questionslist, pages_counter)
    if result != 0:
        return result
    return render(
        request,
        'hot_questions.html',
        context={'questions': questionslist, 'pages': pages_counter}
    )


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)
