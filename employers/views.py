from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group

from .models import JobPost
from .forms import JobPostForm, RegisterForm
from candidates.models import JobApplication


def _is_employer(user):
    """
    Helper to check if the logged-in user is an employer.
    """
    return user.is_authenticated and user.groups.filter(name="employer").exists()


def employer_required(view_func):
    """
    Decorator to ensure that only employer users can access a view.
    - Redirects unauthenticated users to the employer login page.
    - Blocks authenticated non-employer users.
    """
    return user_passes_test(
        _is_employer,
        login_url="login",  # employers login view name
    )(view_func)


# Employer Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Mark this account as an employer via Django Group
            employer_group, _ = Group.objects.get_or_create(name="employer")
            user.groups.add(employer_group)

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
@employer_required
def employer_dashboard(request):
    jobs = JobPost.objects.filter(employer=request.user)
    return render(request, 'employers/job_list.html', {'jobs': jobs})


# Add Job Post
@employer_required
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
@employer_required
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
@employer_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)
    job.delete()
    return redirect('employer_dashboard')


# View applications (placeholder)


@employer_required
def view_applications(request, job_id):
    """
    Employer can view applications ONLY for a specific job they own
    """
    job = get_object_or_404(JobPost, id=job_id, employer=request.user)

    applications = JobApplication.objects.filter(
        job=job
    ).select_related('job', 'user')

    return render(
        request,
        'employers/application.html',
        {
            'job': job,
            'applications': applications
        }
    )



