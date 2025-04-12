from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse, HttpResponse
from Users.models import *
from Course.models import *
import json
from django.shortcuts import get_object_or_404
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

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
    sections = course.curriculum.sections.all()
    
    completed = False
    course_items_id = CurriculumItem.objects.filter(section__curriculum__course__id=course_id).values_list('id', flat=True)
    watched_items_id = WatchedContent.objects.filter(user=request.user, item__in=CurriculumItem.objects.filter(section__curriculum__course__id=course_id)).values_list('item__id', flat=True)
    
    if sorted(course_items_id) == sorted(watched_items_id):
        completed = True
    watched_items_ids = [int(x) for x in watched_items_id]

    certificate_status = "Locked"
    if Result.objects.filter(user=request.user, course=course).exists():
        certificate_status = "Unlocked"

    return render(request, 'users/course_detail.html', context={'course':course, 'completed':completed, 'watched_items_ids':watched_items_ids, 'certificate_status':certificate_status})

def checkbox_action(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("value")
        checked = data.get("checked")
        print(item_id)
        curriculum_item = CurriculumItem.objects.get(id=int(item_id))

        if checked:
            if not WatchedContent.objects.filter(user=request.user, item=curriculum_item).exists():    
                WatchedContent.objects.create(user=request.user, item=curriculum_item)
        else:
            watched_content = WatchedContent.objects.get(user=request.user, item=curriculum_item)
            watched_content.delete()
        return JsonResponse({"status": "success", "message":""})
    
    return JsonResponse({"status": "error", "message":""}, status=400)

def exam_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        question_ids = request.POST.getlist('question_id[]')
        obtained_total_marks = 0
        result_status = 'Fail'
        for question_id in question_ids:
            answer_id = request.POST.get(f'question[answer][{question_id}]')
            if answer_id:
                answer = Answer.objects.get(id=answer_id)
                if answer.is_correct:
                    obtained_total_marks = obtained_total_marks + Question.objects.get(id=int(question_id)).mark

        if obtained_total_marks >= (70 * 0.7):
            result_status = 'Pass'
            result = Result.objects.create(user=request.user, course=course, status=result_status, obtained_marks=int(obtained_total_marks))
            messages.success(request, f'Congratulations you have successfully unlocked the Certification.')
            return redirect('course-details-view', course_id=int(course.id))    

        messages.error(request, f'Passing Criteria not fullfilled.Try Again.')
        return redirect('course-details-view', course_id=int(course.id))    
    return render(request, 'users/exam.html', context={'course':course})

def generate_certificate(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    name = f'{user}'
    course_title = course.title

    # Massive canvas size for very large text
    width, height = 2500, 1725  # Increased canvas size
    img = Image.new('RGB', (width, height), color='#e6f0ff')
    draw = ImageDraw.Draw(img)

    # Load extremely large fonts
    try:
        # Giant font sizes
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 11000)  # 500px size
        name_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 1050)    # 450px size
        body_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 950)    # 350px size
        footer_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 850)  # 250px size
    except IOError:
        # Fallback with the largest possible default fonts
        title_font = ImageFont.load_default(size=50)
        name_font = ImageFont.load_default(size=45)
        body_font = ImageFont.load_default(size=35)
        footer_font = ImageFont.load_default(size=25)

    # Calculate total content height for vertical centering
    content_elements = [
        ("🎓 CERTIFICATE OF COMPLETION", title_font, '#005a9c'),
        ("This is to certify that", body_font, 'black'),
        (name, name_font, '#005a9c'),
        ("has successfully completed the course", body_font, 'black'),
        (course_title, name_font, '#005a9c')
    ]
    
    total_content_height = 0
    spacing = 150  # Space between elements
    
    # First pass to calculate total height
    for text, font, _ in content_elements:
        bbox = draw.textbbox((0, 0), text, font=font)
        total_content_height += (bbox[3] - bbox[1]) + spacing
    
    # Remove extra spacing from last element
    total_content_height -= spacing
    
    # Calculate starting Y position for vertical centering
    start_y = (height - total_content_height) / 2

    # Draw border
    border_color = '#005a9c'
    draw.rectangle([(80, 80), (width - 80, height - 80)], outline=border_color, width=40)

    # Draw all centered content
    current_y = start_y
    
    for text, font, color in content_elements:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        draw.text((x, current_y), text, font=font, fill=color)
        current_y += text_height + spacing

    # Draw footer at bottom (centered)
    footer_text = "🎓 EASY LEARN | E-Learning Academy"
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_width = bbox[2] - bbox[0]
    footer_x = (width - footer_width) / 2
    draw.text((footer_x, height - 300), footer_text, fill=border_color, font=footer_font)

    # Save to buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    if request.GET.get('download') == 'true':
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename=certificate_{course.id}.png'
    else:
        response = HttpResponse(buffer.getvalue(), content_type='image/png')

    return response