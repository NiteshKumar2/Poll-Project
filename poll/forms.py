from django.forms import ModelForm
from .models import Poll

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'option_one', 'option_two', 'option_three' , 'option_four']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']