from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from internships.models import JobPosting


def home(request):
    """Landing page"""
    # Show featured job postings
    featured_jobs = JobPosting.objects.filter(status='OPEN').order_by('-created_at')[:6]

    context = {
        'featured_jobs': featured_jobs,
    }
    return render(request, 'core/home.html', context)


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.email}!')

            # Redirect based on role
            if user.role == 'STUDENT':
                return redirect('student:dashboard')
            elif user.role == 'SUPERVISOR':
                return redirect('supervisor:dashboard')
            elif user.role == 'ADMIN':
                return redirect('/admin/')
        else:
            messages.error(request, 'Email atau password salah.')

    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('home')
