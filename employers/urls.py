from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='employer_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('add-job/', views.add_job, name='add_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
]
