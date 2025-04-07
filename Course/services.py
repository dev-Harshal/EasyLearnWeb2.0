from Course.models import *

def save_new_section_and_item(request, curriculum):
    section_titles = request.POST.getlist('section_title[]')
    section_orders = request.POST.getlist('section_order[]')

    for section_title, section_order in zip(section_titles, section_orders):

        section = Section.objects.create(
            curriculum = curriculum,
            title = section_title,
            order = int(section_order)
        )

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