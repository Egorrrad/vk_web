from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url
from django.urls import path
from AskMe import views
from AskMe.models import Question, LikeDis, Answer

urlpatterns = [
    path('', views.index, name='index'),
    path('ask', views.ask, name='ask'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout_user'),
    path('question/<int:question_id>', views.question, name='question'),
    
    path('api/question/<int:id>/like/',
         login_required(views.VotesView.as_view(model=Question, vote_type=LikeDis.LIKE)),
         name='question_like'),
    path('api/question/<int:id>/dislike/',
         login_required(views.VotesView.as_view(model=Question, vote_type=LikeDis.DISLIKE)),
         name='question_dislike'),
    path('api/answer/<int:id>/like/',
         login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDis.LIKE)),
         name='answer_like'),
    path('api/answer/<int:id>/dislike/',
         login_required(views.VotesView.as_view(model=Answer, vote_type=LikeDis.DISLIKE)),
         name='answer_dislike'),
    path('signup', views.signup, name='signup'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('settings', views.settings, name='settings'),
    path('hot', views.hot, name='hot_questions'),

    # path('post_question', views.post_question, name='post_question'),


]

'''
urlpatterns+= [
    url(r'^article/(?P<pk>\d+)/like/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDis.LIKE)),
        name='article_like'),
    url(r'^article/(?P<pk>\d+)/dislike/$',
        login_required(views.VotesView.as_view(model=Question, vote_type=LikeDis.DISLIKE)),
        name='article_dislike'),
]

'''
