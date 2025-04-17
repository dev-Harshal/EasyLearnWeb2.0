from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from Users.models import *
from Course.models import *
# Create your views here.

def index_view(request):
    user_courses = Course.objects.filter(created_by=request.user).all()
    total_courses = user_courses.count()
    
    total_videos = Lesson.objects.filter(
        curriculum_item__section__curriculum__course__created_by=request.user
    ).count()

    total_notes = Lesson.objects.filter(
        curriculum_item__section__curriculum__course__created_by=request.user,
        note_file__isnull=False
    ).exclude(note_file='').count()

    total_quizzes = Quiz.objects.filter(
        curriculum_item__section__curriculum__course__created_by=request.user
    ).count()

    unique_student_count = WatchedContent.objects.filter(
        item__section__curriculum__course__created_by=request.user
    ).values('user').distinct().count()


    unique_result_students = Result.objects.filter(
        course__created_by=request.user
    ).values('user').distinct().count()

    context = {
        "total_courses":total_courses,
        "total_videos":total_videos,
        "total_notes":total_notes,
        "total_quizzes":total_quizzes,
        "unique_student_count":unique_student_count,
        "unique_result_students":unique_result_students
    }

    return render(request, 'teacher/index.html', context=context)

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
            return JsonResponse({'status':'success', 'success_url':'/teacher/profile/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'teacher/profile.html')

def list_students_view(request):
    users = User.objects.filter(role='Student')
    return render(request, 'teacher/list_students.html', context={'users':users})