import random

from django.contrib.auth.mixins import LoginRequiredMixin

from utils import send_otp_code
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta, datetime


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_otp_code(cd['phone'], random_code)

            OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify_code.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['code'] == code_instance.code:
                if code_instance.is_active:
                    user = User.objects.create_user(user_session['phone_number'], user_session['email'],
                                                    user_session['full_name'], user_session['password'])
                    code_instance.delete()
                    messages.success(request, 'registered successfully', 'success')
                else:
                    messages.error(request, 'code is expired!', 'danger')
                    return redirect('accounts:register')
            else:
                messages.error(request, 'wrong code!', 'danger')
                return redirect(self.template_name)

        return redirect('accounts:user_register')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                request.session['user_login_info'] = {
                    'phone_number': cd['phone'],
                    'password': cd['password'],
                }
                return redirect('home:home')

            messages.error(request, 'username or password is wrong', 'error')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logged out')
        return redirect('home:home')
