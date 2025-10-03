from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import User, StudentProfile
from .forms import StudentRegistrationForm, StudentProfileForm
from internships.models import JobPosting, Application, InternshipPlacement
from internships.forms import JobApplicationForm, InternshipConfirmationForm
from reports.models import MonthlyReport


def register(request):
    """Student registration"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        nim = request.POST.get('nim')
        program = request.POST.get('program')
        angkatan = request.POST.get('angkatan')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        whatsapp = request.POST.get('whatsapp')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Get file uploads
        konsultasi_mentor_doc = request.FILES.get('konsultasi_mentor_doc')
        sptjm_doc = request.FILES.get('sptjm_doc')

        # Validation
        if password != password_confirm:
            messages.error(request, 'Password tidak cocok!')
            return render(request, 'student/register.html')

        if not email.endswith('@student.prasetiyamulya.ac.id'):
            messages.error(request, 'Email harus menggunakan domain @student.prasetiyamulya.ac.id')
            return render(request, 'student/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return render(request, 'student/register.html')

        if StudentProfile.objects.filter(nim=nim).exists():
            messages.error(request, 'NIM sudah terdaftar!')
            return render(request, 'student/register.html')

        # Validate required documents
        if not konsultasi_mentor_doc:
            messages.error(request, 'Bukti konsultasi dengan mentor wajib diupload!')
            return render(request, 'student/register.html')

        if not sptjm_doc:
            messages.error(request, 'Bukti SPTJM wajib diupload!')
            return render(request, 'student/register.html')

        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role='STUDENT'
                )

                # Create student profile
                StudentProfile.objects.create(
                    user=user,
                    full_name=full_name,
                    nim=nim,
                    program=program,
                    angkatan=angkatan,
                    gender=gender,
                    whatsapp=whatsapp,
                    konsultasi_mentor_doc=konsultasi_mentor_doc,
                    sptjm_doc=sptjm_doc,
                    status='APPROVED',
                    approved_at=timezone.now()
                )

                messages.success(request, 'Registrasi berhasil! Silakan login.')
                return redirect('login')

        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')

    return render(request, 'student/register.html')


@login_required
def dashboard(request):
    """Student dashboard"""
    if request.user.role != 'STUDENT':
        messages.error(request, 'Akses ditolak!')
        return redirect('home')

    try:
        student = request.user.studentprofile
    except:
        messages.error(request, 'Profile tidak ditemukan!')
        return redirect('home')

    # Get active placement
    active_placement = InternshipPlacement.objects.filter(
        student=student,
        status='ACTIVE'
    ).first()

    # Get recent applications
    applications = Application.objects.filter(student=student).order_by('-applied_at')[:5]

    # Get available jobs
    available_jobs = JobPosting.objects.filter(status='OPEN').order_by('-created_at')[:5]

    context = {
        'student': student,
        'active_placement': active_placement,
        'applications': applications,
        'available_jobs': available_jobs,
    }

    return render(request, 'student/dashboard.html', context)


@login_required
def profile(request):
    """Student profile"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    student = request.user.studentprofile
    return render(request, 'student/profile.html', {'student': student})


@login_required
def edit_profile(request):
    """Edit student profile"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    student = request.user.studentprofile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile berhasil diupdate!')
            return redirect('student:profile')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'student/edit_profile.html', {'form': form, 'student': student})


@login_required
def job_list(request):
    """List of available jobs"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    jobs = JobPosting.objects.filter(status='OPEN').order_by('-created_at')
    return render(request, 'student/job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, job_id):
    """Job detail and application"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    job = get_object_or_404(JobPosting, id=job_id)
    student = request.user.studentprofile

    # Check if already applied
    existing_application = Application.objects.filter(
        student=student,
        job_posting=job
    ).first()

    if request.method == 'POST' and not existing_application:
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.job_posting = job
            application.status = 'SENT'
            application.save()

            messages.success(request, 'Aplikasi berhasil dikirim!')
            return redirect('student:applications')
    else:
        form = JobApplicationForm()

    context = {
        'job': job,
        'form': form,
        'existing_application': existing_application,
    }
    return render(request, 'student/job_detail.html', context)


@login_required
def my_applications(request):
    """My applications"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    student = request.user.studentprofile
    applications = Application.objects.filter(student=student).order_by('-applied_at')
    return render(request, 'student/applications.html', {'applications': applications})


@login_required
def reports(request):
    """Monthly reports - redirect to reports app"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    return redirect('reports:student_reports')


@login_required
def confirm_internship(request):
    """Confirm internship"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    student = request.user.studentprofile

    # Check if already has active internship
    active_internship = InternshipPlacement.objects.filter(
        student=student,
        status__in=['PENDING_CONFIRMATION', 'ACTIVE']
    ).first()

    if active_internship:
        messages.warning(request, 'Anda sudah memiliki internship aktif!')
        return redirect('student:dashboard')

    if request.method == 'POST':
        form = InternshipConfirmationForm(request.POST, request.FILES)
        if form.is_valid():
            placement = form.save(commit=False)
            placement.student = student
            placement.status = 'ACTIVE'
            placement.confirmed_at = timezone.now()
            placement.save()

            # Update student status
            student.status = 'ACTIVE'
            student.save()

            messages.success(request, 'Konfirmasi magang berhasil! Anda sudah bisa membuat laporan bulanan.')
            return redirect('student:dashboard')
    else:
        form = InternshipConfirmationForm()

    return render(request, 'student/confirm_internship.html', {'form': form})
