from django.urls import path
from AskMe import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask),
    path('login', views.login),
    path('question', views.question),
    path('signup', views.signup),
    path('tag', views.tag),
    path('settings', views.settings),
]
