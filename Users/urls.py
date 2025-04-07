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


    path('course/detail/<int:course_id>/', course_detail_view, name='course-detail-view')
]
