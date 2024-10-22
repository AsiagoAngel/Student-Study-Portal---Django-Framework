from django import forms
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm


# ------------  Notes Section  ------------------#

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


# -------- Homework Section ------------#

class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']


# -------- Common Section ------------ #

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Youtube Search :")


# -------- To Do Section ------------ #

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']

# -------- Login Section ------------ #

class UseRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
