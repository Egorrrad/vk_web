from django.urls import path
from AskMe import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('question/<int:question_id>', views.question, name='question'),
    path('signup', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('settings', views.settings, name='settings'),
    path('hot', views.hot, name='hot_questions'),
#path('post_question', views.post_question, name='post_question'),


]
