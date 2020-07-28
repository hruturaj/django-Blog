from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from . import forms

# Create your views here.

class SignUp(CreateView):
    form_class = forms.userSignUpForm
    template_name = 'accounts/signUp.html'
    success_url = reverse_lazy('login')
