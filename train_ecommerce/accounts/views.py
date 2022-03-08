from django.shortcuts import render

# Create your views here.
from django.views import View
from .forms import *


class UserRegisterView(View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form':form})

    def post(self, request):
        ...
