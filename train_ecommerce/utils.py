from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    try:

        api = KavenegarAPI('4A46746644386C69505A736C6C4959522F66587A427A78633052744B3373694345785A4D49503772352F6F3D')
        msg = f'your verification code is \n {code}'
        params = {'sender': '', 'receptor': phone_number, 'message': msg}

        response = api.sms_send(params)
        print(response)

    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.user.is_authenticated and self.user.is_admin
