from django.shortcuts import render
from django.core.paginator import Paginator

questions = [
    {
        "id": i,
        "title": f"quesion {i}",
        "content": f"aaaaaaaa {i}",
        "answers": i,
        "tags": ["tag1", "tag2"]
    } for i in range(10)
]


def paginate(request, objects, per_page=5):
    result = None
    pages_pagination = []
    try:
        page = request.GET.get('page')
        # можно закинуть сюда request
        # добавить обработку отсутсвтия страницы
        paginator = Paginator(objects, per_page)
        result = paginator.page(page)

        num_page=int(page)+1
        for i in range(num_page, num_page + 3):
            pages_pagination.append(i)
        pages_pagination.append("...")
        # тут надо знать сколько всего страниц чтобы красиво было
        for i in range(num_page + 10, num_page + 13):
            pages_pagination.append(i)

    except Exception as e:
        print(e)

    return result, pages_pagination


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    questionslist, pages = paginate(request, questions)

    print(pages)


    return render(
        request,
        'index.html',
        context={'questions': questionslist, 'pages': pages}
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


def question(request, question_id):
    item = questions[question_id]
    return render(
        request,
        'question.html',
        context={'item': item}
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


def test(request):
    return render(
        request,
        'test.html'
    )
