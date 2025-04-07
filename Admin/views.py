from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from Users.models import *
# Create your views here.

def index_view(request):
    return render(request, 'admin/index.html')

def profile_view(request):
    if request.method == 'POST':
        try:
            profile_photo = request.FILES.get('profile_photo', '')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')

            user = request.user

            if User.objects.filter(email=email).exists():
                if email != request.user.email:
                    return JsonResponse({'status':'error', 'message':f'Email address already exists.'})

            if Profile.objects.filter(phone_number=phone_number).exists():
                if phone_number != request.user.profile.phone_number:
                    return JsonResponse({'status':'error', 'message':'Phone number already exists.'})

            user.profile_photo = profile_photo if profile_photo != '' else user.profile_photo
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            profile = Profile.objects.get(user=user)
            profile.phone_number = phone_number
            profile.save()

            messages.success(request, f'{user.first_name} {user.last_name[0]} profile saved successfully.')
            return JsonResponse({'status':'success', 'success_url':'/admin/profile/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'admin/profile.html')

def create_teacher_view(request):
    if request.method == 'POST':
        try:
            profile_photo = request.FILES.get('profile_photo', '')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            experience = request.POST.get('experience')
            department = request.POST.get('department')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return JsonResponse({'status':'error', 'message':'Passwords does not match. Try again.'})

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status':'error', 'message':'Email address already exists.'})

            if Profile.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'status':'error', 'message':'Phone number already exists.'})
            
            user = User.objects.create_user(
                profile_photo = profile_photo,
                first_name = first_name, 
                last_name = last_name,
                email = email,
                password = password,
                role = 'Teacher'
            )
            Profile.objects.create(
                user = user,
                phone_number = phone_number,
                department = department,
                experience = float(experience)
            )

            messages.success(request, f'{user} created successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/admin/update/teacher/{user.id}/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'admin/create_teacher.html')

def update_teacher_view(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        try:
            profile_photo = request.FILES.get('profile_photo', '')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            experience = request.POST.get('experience')
            department = request.POST.get('department') 

            if User.objects.filter(email=email).exists():
                if email != user.email:
                    return JsonResponse({'status':'error', 'message':'Email address already exists.'})

            if Profile.objects.filter(phone_number=phone_number).exists():
                if phone_number != user.profile.phone_number:
                    return JsonResponse({'status':'error', 'message':'Phone number already exists.'})

            user.profile_photo = profile_photo if profile_photo != '' else user.profile_photo
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            profile = Profile.objects.get(user=user)
            profile.phone_number = phone_number
            profile.experience = float(experience)
            profile.department = department
            profile.save()

            messages.success(request, f'{user.first_name} {user.last_name[0]} profile updated successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/admin/update/teacher/{user.id}/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'admin/update_teacher.html', context={'user':user})

def list_users_view(request, role):
    users = User.objects.filter(role=role).all()
    return render(request, 'admin/list_users.html', context={'users':users, 'role':role})
