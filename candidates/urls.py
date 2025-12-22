from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from . import views

app_name = 'candidates'

# Custom LoginView to ensure fields are empty
class CustomLoginView(auth_views.LoginView):
    template_name = 'candidates/login.html'
    authentication_form = AuthenticationForm
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ensure all fields are empty (no initial values)
        form.fields['username'].initial = None
        form.fields['password'].initial = None
        return form

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('jobs/', views.all_jobs, name='all_jobs'),

    # apply — login required (Django auto redirects)
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),

    path('success/', views.application_success, name='application_success'),
]

