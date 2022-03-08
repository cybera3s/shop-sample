import random
from utils import send_otp_code
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .forms import *
from .models import *


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

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
        return redirect('home:home')


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtmCode.objects.get(phone_number=user_session['phone'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['code'] == code_instance.code:
                user = User.objects.create_user(user_session['phone_number'], user_session['email'],
                                                user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'registered', 'success')
            else:
                messages.error(request, 'wrong code!', 'danger')
                return redirect('accounts:verify_code')

        return redirect('home:home')