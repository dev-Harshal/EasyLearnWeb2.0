from django.urls import path
from Teacher.views import *

app_name = 'teacher'

urlpatterns = [
    path('', index_view, name='index-view'),
    path('profile/', profile_view, name='profile-view'),
    path('list/Student/', list_students_view, name='list-students-view'),
]
