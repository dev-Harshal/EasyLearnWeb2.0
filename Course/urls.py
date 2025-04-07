from django.urls import path
from Course.views import *

app_name = 'course'

urlpatterns = [
    path('create/', create_course_view, name='create-course-view'),    
    path('update/<int:course_id>/', update_course_view, name='update-course-view'),    
    path('delete/<int:course_id>/', delete_course_view, name='delete-course-view'),
    path('detail/<int:course_id>/', detail_course_view, name='detail-course-view'),
    path('list/courses/', list_courses_view, name='list-courses-view'),
    path('save/curriculum/<int:course_id>/', save_curriculum_view, name='save-curriculum-view'),
    path('detail/exam/<int:course_id>/', detail_exam_view, name='detail-exam-view')
]
