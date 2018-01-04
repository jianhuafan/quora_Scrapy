from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Question, Answer
# Create your views here.
@login_required
def index(request):
	question_list = Question.objects.all()
	template = loader.get_template('quora/index.html')
	context = {
		'question_list': question_list,
	}
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
		answer_list = Answer.objects.filter(question_title=question.question_title)
		context = {
			'question': question,
			'answer_list': answer_list,
		}
	except Question.DoesNotExist:
		raise Http404('Question does not exist')
	return render(request, 'quora/detail.html', context)

def userMap(request):
	return render(request, 'quora/geochart.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'quora/signup.html', {'form': form})
