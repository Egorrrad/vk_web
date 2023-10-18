from django.shortcuts import render


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index1.html'
    )


def ask(request):
    """
    Функция отображения страницы для создания вопроса.
    """
    return render(
        request,
        'ask.html'
    )


def login(request):
    return render(
        request,
        'login.html'
    )

def question(request):
    return render(
        request,
        'question.html'
    )

def settings(request):
    return render(
        request,
        'settings.html'
    )

def signup(request):
    return render(
        request,
        'signup.html'
    )


def tag(request):
    return render(
        request,
        'tag.html'
    )