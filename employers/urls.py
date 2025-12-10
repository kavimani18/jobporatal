from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', views.register, name='employer_register'),
    path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
    path('dashboard/', login_required(views.employer_dashboard), name='employer_dashboard'),
    path('add-job/', login_required(views.add_job), name='add_job'),
    path('edit-job/<int:job_id>/', login_required(views.edit_job), name='edit_job'),
    path('delete-job/<int:job_id>/', login_required(views.delete_job), name='delete_job'),
    path('applications/<int:job_id>/', login_required(views.view_applications), name='view_applications'),
]
