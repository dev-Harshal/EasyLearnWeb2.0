from django.urls import path
from Users.views import *

urlpatterns = [
    path('', index_view, name='index-view'),
    path('register/', register_view, name='register-view'),
    path('login/<str:role>/', login_view, name='login-view'),
    path('verify-otp/', verify_otp_view, name='verify-otp-view'),
    path('change-password/', change_password_view, name='change-password-view'),
    path('logout/', logout_view, name='logout-view'),
    path('delete/<int:user_id>/', delete_user_view, name="delete-user-view"),


    path('course/details/<int:course_id>/', course_detail_view, name='course-details-view'),
    path('toggle-watched/', checkbox_action, name='checkbox_action'),
    path('exam/<int:course_id>/',exam_view, name='exam-view'),
    path('certificate/<int:course_id>/', generate_certificate, name='generate_certificate'),
    
]
