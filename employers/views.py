from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import JobPost
from .forms import JobPostForm, RegisterForm


# Employer Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'employers/register.html', {'form': form})


# Employer Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('employer_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'employers/login.html')


# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')


# Employer Dashboard → List all job posts
@login_required
def employer_dashboard(request):
    jobs = JobPost.objects.filter(employer=request.user)
    return render(request, 'employers/job_list.html', {'jobs': jobs})


# Add Job Post
@login_required
def add_job(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        salary = request.POST.get("salary")
        location = request.POST.get("location")

        JobPost.objects.create(
            employer=request.user,
            title=title,
            description=description,
            salary=salary,
            location=location
        )

        return redirect("employer_dashboard")

    return render(request, "employers/add_job.html")


# Edit Job Post
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = JobPostForm(instance=job)

    return render(request, 'employers/edit_job.html', {'form': form})


# Delete Job Post
@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)
    job.delete()
    return redirect('employer_dashboard')


# View applications (placeholder)
@login_required
def view_applications(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)

    # Will be replaced when Candidate model is added
    applications = []

    return render(request, 'employers/applications.html', {
        'job': job,
        'applications': applications
    })
