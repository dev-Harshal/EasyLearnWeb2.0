from django.contrib.auth import authenticate
import random
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

ROLE_CHOICES = (
    ('Admin', 'Admin'), 
    ('Student', 'Student'), 
    ('Teacher', 'Teacher')
)

DESIGNATION_CHOICES = (
    ('Staff Member', 'Staff Member'), 
    ('Professor', 'Professor'), 
    ('Ast.Professor', 'Ast.Professor')
)

DEPARTMENT_CHOICES = (
    ('Admin Department', 'Admin Department'), 
    ('Computer Engineering', 'Computer Engineering'), 
    ('Civil Engineering', 'Civil Engineering'), 
    ('Electronics Engineering', 'Electronics Engineering'), 
    ('Management Studies', 'Management Studies'), 
)

def check_phone_number(model, phone_number):  
    while True:
        if len(phone_number) == 10 and phone_number.isdigit():
            if model.objects.filter(phone_number=phone_number).exists():
                print('\033[1;91m' + 'Error: Phone number already exists.' + '\033[0m')
            else:
                return phone_number
        else:
            print('\033[1;91m' + 'Error: Phone number must be 10 digits.' + '\033[0m')
            phone_number = input('Phone Number: ')

def generate_otp_code(request, role):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = authenticate(email=email, password=password)
    if user is not None and user.role == role:
        otp_code = str(random.randint(1000,9999))
        request.session['otp_code'] = otp_code
        request.session['otp_expiry'] = (timezone.now() + timezone.timedelta(seconds= 30)).timestamp()
        print('OTP CODE: ',otp_code)
        email = EmailMessage(
            subject = 'Question Desk OTP',
            body = f"OTP CODE:{otp_code}",
            from_email=settings.EMAIL_HOST_USER,
            to=[str(email)],
        )
        email.send()
        return {'status':'success', 'message':'OTP code send successfully.'}
    else:
        return {'status':'error', 'message':'Invalid email address or password.'}