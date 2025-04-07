from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from Users.models import *
from Course.models import *
# Create your views here.

def index_view(request):
    recent_courses = Course.objects.all().reverse()[:3]
    context = {
        'recent_courses':recent_courses
    }
    return render(request, 'users/index.html', context=context)

def register_view(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            institute = request.POST.get('institute')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return JsonResponse({'status':'error', 'message':'Passwords does not match.'})

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status':'error', 'message':'Email address already exists.'})
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                institute=institute,
                email=email,
                password=confirm_password,
                role='Student'
            )

            messages.success(request, f'{user} registered successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/login/Student/'})
        
        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'users/register.html')

def login_view(request, role):
    if request.method == 'POST':
        try:
            response = generate_otp_code(request, role)
            return JsonResponse(response)

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'users/login.html', context={'role':role})

def verify_otp_view(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            otp_code = request.POST.get('otp_code')
            otp_expiry = request.session.get('otp_expiry', 0)

            if timezone.now().timestamp() > otp_expiry:
                return JsonResponse({'status':'error', 'message':'OTP code expired! Try again.'})
            
            if otp_code == request.session.get('otp_code'):

                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'{user.first_name} {user.last_name[0]} logged in successfully.')
                    success_url = '/' if user.role == 'Student' else f'/{user.role.lower()}/'
                    return JsonResponse({'status':'success', 'success_url':success_url})
            return JsonResponse({'status':'error', 'message':'Invalid OTP Code! Try again.'})
            
        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return redirect(request.META.get('HTTP_REFERER', ''))

def change_password_view(request):
    if request.method == 'POST':
        try:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            email = request.user.email

            if new_password != confirm_password:
                    return JsonResponse({'status':'error', 'message':'Passwords does not match.'})

            user = authenticate(email=email, password=current_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                login(request,user)
                messages.success(request, 'Password updated successfully.')
                return JsonResponse({'status':'success', 'success_url':f'/{user.role.lower()}/profile/'})
            else:
                return JsonResponse({'status':'error', 'message':'Current password does not match.'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return redirect(request.META.get('HTTP_REFERER', ''))

def logout_view(request):
    try:
        user = request.user
        logout(request)
        messages.success(request, f'{user.first_name} {user.last_name[0]} logged out successfully.')
    except Exception as error:
        messages.error(request, f'ERROR: {error}')
    else:
        return redirect('index-view')
    
def delete_user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        deleted_user = user
        user.delete()
        messages.success(request, f'{deleted_user} deleted successfully.')
    except Exception as error:
        messages.error(request, f'ERROR: {error}')
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    

def course_detail_view(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'users/course_detail.html', context={'course':course})
