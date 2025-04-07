import traceback
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from Course.models import *
from Course.services import *
# Create your views here.

def create_course_view(request):
    if request.method == 'POST':
        try:
            thumbnail = request.FILES.get('thumbnail', '')
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category')

            if Course.objects.filter(title__iexact=title).exists():
                return JsonResponse({'status':'error', 'message':'Same course title already exists.'})
            
            course = Course.objects.create(
                thumbnail = thumbnail,
                title = title,
                description = description,
                category = category,
                created_by = request.user
            )

            messages.success(request, f'{course.title} created successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/course/detail/{course.id}/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'course/create_course.html')

def detail_course_view(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'course/detail_course.html', context={'course':course})

def list_courses_view(request):
    courses = request.user.courses.all()
    return render(request, 'course/list_courses.html', context={'courses':courses})

def update_course_view(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        try:
            thumbnail = request.FILES.get('thumbnail', '')
            category = request.POST.get('category')
            title = request.POST.get('title')
            description = request.POST.get('description')

            courses = Course.objects.filter(title__iexact=title)
            if courses.exists() and course != courses[0]:
                return JsonResponse({'status':'error', 'message':'Same course title already exists.'})

            course.thumbnail = thumbnail if thumbnail != '' else course.thumbnail
            course.category = category
            course.title = title
            course.description = description
            course.save()
            messages.success(request, f'Course Information updated successfully.')
            return JsonResponse({'status':'success', 'success_url':f'/course/update/{course.id}/'})

        except Exception as error:
            return JsonResponse({'status':'error', 'message':f'ERROR: {error}'})
    return render(request, 'course/update_course.html', context={'course':course})

def delete_course_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
        messages.success(request, f'{course.title} deleted successfully.')
    except Exception as error:
        messages.error(request, f'ERROR: {error}')
    else:
        return redirect('list-courses-view')
    
def save_curriculum_view(request, course_id):
    if request.method == 'POST':
        try:
            course = Course.objects.get(id=course_id)
            curriculum, created = Curriculum.objects.get_or_create(course=course)
            
            section_ids_before = curriculum.sections.all().values_list('id', flat=True)
            section_ids_after = set()

            old_section_ids = request.POST.getlist('old_section_id[]')
            old_section_titles = request.POST.getlist('old_section_title[]')
            old_section_orders = request.POST.getlist('old_section_order[]')

            for section_id, section_title, section_order in zip(old_section_ids, old_section_titles, old_section_orders):
                section = Section.objects.get(id=int(section_id))
                section.title = section_title
                section.order = int(section_order)
                section.save()

                section_item_ids_before = section.curriculum_items.all().values_list('id', flat=True)
                section_item_ids_after = set()

                old_item_ids = request.POST.getlist(f'old_sections[{section_order}][items][item_id][]')
                old_item_types = request.POST.getlist(f'old_sections[{section_order}][items][type][]')
                old_item_orders = request.POST.getlist(f'old_sections[{section_order}][items][order][]')

                for item_id, item_type, item_order in zip(old_item_ids, old_item_types, old_item_orders):
                    curriculum_item = CurriculumItem.objects.get(id=int(item_id))
                    curriculum_item.type = item_type
                    curriculum_item.order = int(item_order)
                    curriculum_item.save()

                    if item_type == 'lesson':
                        video_id = request.POST.get(f'old_sections[{section_order}][items][{item_order}][video_id][]')
                        video_title = request.POST.get(f'old_sections[{section_order}][items][{item_order}][title][]')
                        video_file = request.FILES.get(f'old_sections[{section_order}][items][{item_order}][video_file][]',None)
                        note_file = request.FILES.get(f'old_sections[{section_order}][items][{item_order}][note_file][]', None)

                        lesson = Lesson.objects.get(id=int(video_id))
                        lesson.title = video_title
                        lesson.video_file = video_file if video_file else lesson.video_file
                        lesson.note_file = note_file if note_file else lesson.note_file
                        lesson.save()

                    else:
                        quiz_id = request.POST.get(f'old_sections[{section_order}][items][{item_order}][quiz_id][]')
                        quiz_question = request.POST.get(f'old_sections[{section_order}][items][{item_order}][question][]')
                        quiz = Quiz.objects.get(id=int(quiz_id))
                        quiz.question = quiz_question
                        quiz.save()

                        for option_number in range(1, 5):
                            option_id = request.POST.get(f'old_sections[{section_order}][items][{item_order}][options][{option_number}][option_id][]')
                            option_text = request.POST.get(f'old_sections[{section_order}][items][{item_order}][options][{option_number}][text][]')
                            is_correct = request.POST.get(f'old_sections[{section_order}][items][{item_order}][is_correct][]') == str(option_number)   

                            option = QuizOption.objects.get(id=int(option_id))
                            option.text = option_text
                            option.is_correct = is_correct
                            option.save()
                        
                    section_item_ids_after.add(int(item_id))
                    
                for id in section_item_ids_before:
                    if int(id) not in section_item_ids_after:
                        curriculum_item = CurriculumItem.objects.get(id=int(id))
                        curriculum_item.delete()

                item_types = request.POST.getlist(f'sections[{section_order}][items][type][]')
                item_orders = request.POST.getlist(f'sections[{section_order}][items][order][]')

                for item_type, item_order in zip(item_types, item_orders):
                    curriculum_item = CurriculumItem.objects.create(
                        section = section,
                        type = item_type,
                        order = int(item_order)
                    )

                    if item_type == 'lesson':
                        video_title = request.POST.get(f'sections[{section_order}][items][{item_order}][title][]')
                        video_file = request.FILES.get(f'sections[{section_order}][items][{item_order}][video_file][]')
                        note_file = request.FILES.get(f'sections[{section_order}][items][{item_order}][note_file][]', None)

                        lesson = Lesson.objects.create(
                            curriculum_item = curriculum_item,
                            title = video_title,
                            video_file = video_file,
                            note_file = note_file
                        )

                    else:
                        quiz_question = request.POST.get(f'sections[{section_order}][items][{item_order}][question][]')

                        quiz = Quiz.objects.create(
                            curriculum_item = curriculum_item,
                            question = quiz_question
                        )

                        for option_number in range(1, 5):
                            option_text = request.POST.get(f'sections[{section_order}][items][{item_order}][options][{option_number}][text][]')
                            is_correct = request.POST.get(f'sections[{section_order}][items][{item_order}][is_correct][]') == str(option_number)   
                            
                            quiz_option = QuizOption.objects.create(
                                quiz = quiz,
                                text = option_text,
                                is_correct = is_correct
                            )

                section_ids_after.add(int(section_id))

            for id in section_ids_before:
                if int(id) not in section_ids_after:
                    section = Section.objects.get(id=int(id))
                    section.delete()

            save_new_section_and_item(request, curriculum)

            messages.success(request, f'Course Curriculum for {course.title} saved successfully.')
            return JsonResponse({'status': 'success', 'success_url': f'/course/detail/{course.id}/'})
    
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def detail_exam_view(request, course_id): 
    course = Course.objects.get(id=course_id)
    exam, created = Exam.objects.get_or_create(course=course)

    if request.method == 'POST':
        try:

            question_ids_before = exam.questions.all().values_list('id', flat=True)
            question_ids_after = set()

            old_question_ids = request.POST.getlist('old_question_id[]')
            old_questions = request.POST.getlist('old_question[]')
            old_marks = request.POST.getlist('old_mark[]')
            old_orders = request.POST.getlist('old_question[order][]')

            for question_id, text, mark, order in zip(old_question_ids, old_questions, old_marks, old_orders):
                question = Question.objects.get(id=int(question_id))
                question.text = text
                question.mark = int(mark)
                question.save()

                for anwser_number in range(1, 5):
                    answer_id = request.POST.getlist(f'old_question[answer_id][{order}][]')
                    answer_text = request.POST.getlist(f'old_question[answer][{order}][]')
                    is_correct = request.POST.get(f'old_question[is_correct][{order}][]') == str(anwser_number)
                    print(answer_id,old_orders)
                    answer = Answer.objects.get(id=int(answer_id[anwser_number-1]))
                    answer.text = answer_text[anwser_number-1]
                    answer.is_correct = is_correct
                    answer.save()

                question_ids_after.add(int(question_id))

            for id in question_ids_before:
                if int(id) not in question_ids_after:
                    question = Question.objects.get(id=int(id))
                    question.delete()

            question_orders = request.POST.getlist('question[order][]')
            questions = request.POST.getlist('question[]')
            marks = request.POST.getlist('mark[]')

            total_marks = sum([int(x) for x in old_marks]) + sum([int(x) for x in marks])

            if total_marks > 70:
                return JsonResponse({'status':'error', 'message':f'Sum of Total Marks should not exceed 70 Marks. (Current: {total_marks})'})
            
            for text, mark, order in zip(questions, marks, question_orders):
                question = Question.objects.create(exam=exam, text=text,mark=int(mark))

                for anwser_number in range(1, 5):
                    answer_text = request.POST.getlist(f'question[answer][{order}][]')
                    is_correct = request.POST.get(f'question[is_correct][{order}][]') == str(anwser_number)
                    Answer.objects.create(question=question, text=answer_text[anwser_number-1], is_correct=is_correct)

            messages.success(request, f'Exam Questions for {course} created successfully.')
            return JsonResponse({'status': 'success', 'success_url': f'/course/detail/exam/{course.id}/'})
            
        except Exception as error:
            print(traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': f'ERROR: {error}'})

    return render(request, 'course/detail_exam.html', context={'exam':exam})