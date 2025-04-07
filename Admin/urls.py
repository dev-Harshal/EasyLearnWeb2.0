from django.urls import path
from Admin.views import *

app_name = 'admin'

urlpatterns = [
    path('', index_view, name='index-view'),
    path('profile/', profile_view, name='profile-view'),
    path('create/teacher/', create_teacher_view, name='create-teacher-view'),
    path('update/teacher/<int:user_id>/', update_teacher_view, name='update-teacher-view'),
    path('list/<str:role>/', list_users_view, name='list-users-view')
]
