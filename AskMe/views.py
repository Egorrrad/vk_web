import datetime
import math

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect


from AskMe.forms import *
from AskMe.helpers import *
from AskMe.models import *




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
        context={'questions': questionslist, 'pages': pages_counter, 'tags_popular': get_popular_tags()}
    )


def ask(request):
    """
    Функция отображения страницы для создания вопроса.
    """

    try:
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                print(data)

                if request.user.is_authenticated:
                    user = User.objects.get(username=request.user)
                    post_question1 = Question.objects.create(title=data["title"], content=data["content"],
                                                             user=user)

                    question_model_type = ContentType.objects.get_for_model(post_question1)
                    # добавление лайка
                    # Like.objects.create(content_type=question_model_type, object_id=post_question1.id, user=user)

                    tags = str(data["tags"]).split(" ")
                    for elem in tags:
                        tag_elem = Tag.objects.get_or_create(tag_name=elem)
                        post_question1.tags.add(tag_elem[0].id)
                        # post_question1.tags.create(id=tag_elem[0].id)

                    id = post_question1.id

                    return redirect(question, question_id=id)
                else:
                    # raise forms.ValidationError('You must be logged in')
                    form.add_error('title', "You must be logged in!")
                    return render(
                        request,
                        'ask.html',
                        {"form": form}
                    )

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
                form.add_error('username', 'Invalid login or password')
    else:
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
        if request.method == "POST":
            form = AddAnswerForm(request.POST)
            if form.is_valid():
                if request.user.is_authenticated:
                    data = form.cleaned_data
                    item.answers.create(text=data["answer"], user = request.user)
                else:
                    form.add_error('answer', "You must be logged in!")
                    return render(
                        request,
                        'question.html',
                        context={'item': item, 'form': form}
                    )

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
    user_now = request.user
    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(username=user_now.username)
            # user.profile.image
            print(data)
            user.username = data["username"]
            user.first_name = data["first_name"]
            user.email = data["email"]
            user.save()
            if request.FILES:
                add_image_profile(user, request)

            return render(
                request,
                'settings.html', context={"form": form}
            )

        else:
            print(form.is_valid())

    user = User.objects.get(username=user_now.username)
    form = SettingsForm(initial={'username': user.username, 'first_name': user.first_name,
                                 'email': user.email,
                                 # 'image': profile.image.url
                                 })
    # print(form)
    # form.set_values(user_now.username, user_now.email, user_now.first_name)
    return render(
        request,
        'settings.html', context={"form": form}
    )


def signup(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = User.objects.get(username=new_user.username)
            print(user)
            if request.FILES:
                add_image_profile(user, request)
            login(request, new_user)
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
