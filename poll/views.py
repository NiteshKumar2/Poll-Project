from django.shortcuts import render 
from django.shortcuts import redirect
from .forms import CreatePollForm,CreateUserForm
from .models import Poll

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'poll/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'poll/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def home(request):
    polls = Poll.objects.all()

    context = {
        'polls' : polls
    }
    return render(request, 'poll/home.html', context)

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')
    else:
        form = CreatePollForm()

    context = {'form' : form}
    return render(request, 'poll/create.html', context)

@login_required(login_url='login')
def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/results.html', context)

@login_required(login_url='login')
def delet(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    pol=poll.delete()

    context = {
        'pol' : pol
    }
    return render(request, 'poll/delet.html', context)

@login_required(login_url='login')
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        elif selected_option == 'option4':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form option')
    
        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'poll/vote.html', context)