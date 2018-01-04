from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
		path('', views.index, name='index'),
		path('<int:question_id>/', views.detail, name='detail'),
		path('usermap/', views.userMap, name='userMap'),
		url(r'^login/$', auth_views.login, {'template_name': 'quora/login.html'}, name='login'),
		url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
		url(r'^signup/$', views.signup, name='signup'),
]