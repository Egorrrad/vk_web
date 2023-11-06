import math

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render

from AskMe.models import Profile, Tag


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


def add_image_profile(user, request):
    file = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save("user_" + str(user.id) + "/avatar." + str(file.name).split(".")[1], file)
    # file_url = fs.url(filename)
    profile = Profile.objects.get_or_create(user=user)[0]
    profile.image = filename
    profile.save()


def get_popular_tags():
    tags = Tag.objects.all()
    array = []
    for k in tags:
        array.append([k.tag_name, k.total_tags])

    # print(array)

    def custom_key(people):
        return people[1]

    array.sort(key=custom_key, reverse=True)
    # print(array[:7])
    tags = []
    for k in array[:7]:
        tags.append(k[0])
    return tags
