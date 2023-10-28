from django.shortcuts import render
from django.core.paginator import Paginator

question1 = {
    "id",
    "title",
    "content",
    "answers_count",
    "answers",
    "tags"
}


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
    num_page = 1
    pages_pagination = []
    try:
        # лучше использовать метод get, иначе исключения ловить надо
        page = request.GET.get('page', 1)  # дефолтное значение для get
        # можно закинуть сюда request
        # добавить обработку отсутсвтия страницы
        paginator = Paginator(objects, per_page)
        result = paginator.page(page)

        num_page = int(page) + 1
    except Exception as e:
        print(e)

    for i in range(num_page, num_page + 3):
        pages_pagination.append(i)
    pages_pagination.append("...")
    # тут надо знать сколько всего страниц чтобы красиво было
    for i in range(num_page + 10, num_page + 13):
        pages_pagination.append(i)

    return result, pages_pagination


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


def tag(request, tag_name):
    questions_with_tag = []
    for k in questions:
        if tag_name in k["tags"]:
            questions_with_tag.append(k)

    if len(questions_with_tag)==0:
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
    questionslist, pages_counter = paginate(request, questions)
    result = isEmptyQuestions(request, questionslist, pages_counter)
    if result != 0:
        return result
    return render(
        request,
        'hot_questions.html',
        context={'questions': questionslist, 'pages': pages_counter}
    )


def test(request):
    return render(
        request,
        'test.html'
    )


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)
