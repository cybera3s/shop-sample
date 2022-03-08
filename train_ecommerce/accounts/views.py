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
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            cd = form.cleaned_data
            send_otp_code(cd['phone'], random_code)

            OtpCode.objects.create(phone_number=cd['phone'], code=random_code)
            request.session['user_registeration_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return redirect('home:home')


class UserRegisterVerifyCodeView(View):
    def get(self, request):
        ...

    def post(self, request):
        ...
