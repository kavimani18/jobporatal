from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group

from employers.models import JobPost
from .forms import CandidateRegisterForm, ApplicationForm
from .models import JobApplication


def _is_candidate(user):
    """
    Helper to check if the logged-in user is a candidate.
    """
    return user.is_authenticated and user.groups.filter(name="candidate").exists()


def candidate_required(view_func):
    """
    Decorator to ensure that only candidate users can access a view.
    - Redirects unauthenticated users to the candidate login page.
    - Blocks authenticated non-candidate users.
    """
    return user_passes_test(
        _is_candidate,
        login_url="candidates:login",
    )(view_func)


# ⭐ Homepage
def homepage(request):
    return render(request, 'candidates/homepage.html')


#  Candidate Register
def register(request):
    if request.method == "POST":
        form = CandidateRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Mark this account as a candidate via Django Group
            candidate_group, _ = Group.objects.get_or_create(name="candidate")
            user.groups.add(candidate_group)

            login(request, user)
            return redirect('candidates:login')  # Redirect to login page after successful registration
    else:
        form = CandidateRegisterForm()

    return render(request, 'candidates/register.html', {'form': form})




#  PUBLIC — Show all jobs (no login required)
def all_jobs(request):
    jobs = JobPost.objects.all().order_by('-created_at')
    return render(request, 'candidates/all_jobs.html', {'jobs': jobs})


#  APPLY — Candidate Login Required
@candidate_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user   # link logged-in user
            application.save()
            return redirect('candidates:application_success')
    else:
        form = ApplicationForm()

    return render(request, 'candidates/apply_job.html', {
        'form': form,
        'job': job
    })



#  Application Success Page
@candidate_required
def application_success(request):
    return render(request, 'candidates/app_success.html')


#  Logout View
def user_logout(request):
    logout(request)
    return redirect('candidates:all_jobs')