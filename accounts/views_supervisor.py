from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from internships.models import InternshipPlacement
from evaluations.models import Evaluation


@login_required
def dashboard(request):
    """Supervisor dashboard"""
    if request.user.role != 'SUPERVISOR':
        messages.error(request, 'Akses ditolak!')
        return redirect('home')

    try:
        supervisor = request.user.supervisorprofile
    except:
        messages.error(request, 'Profile tidak ditemukan!')
        return redirect('home')

    # Get students under supervision
    students = InternshipPlacement.objects.filter(
        supervisor=supervisor,
        status='ACTIVE'
    ).select_related('student')

    # Get pending evaluations
    pending_evaluations = Evaluation.objects.filter(
        supervisor=supervisor,
        status='PENDING'
    ).count()

    context = {
        'supervisor': supervisor,
        'students': students,
        'pending_evaluations': pending_evaluations,
    }

    return render(request, 'supervisor/dashboard.html', context)


@login_required
def students(request):
    """List of students under supervision"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    supervisor = request.user.supervisorprofile
    students = InternshipPlacement.objects.filter(
        supervisor=supervisor
    ).select_related('student')

    return render(request, 'supervisor/students.html', {'students': students})


@login_required
def evaluations(request):
    """List of evaluations - redirect to evaluations app"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    # Import here to avoid circular import
    from evaluations.views import supervisor_evaluations
    return supervisor_evaluations(request)


@login_required
def evaluation_form(request, evaluation_id):
    """Evaluation form - redirect to evaluations app"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    # Import here to avoid circular import
    from evaluations.views import evaluation_form as eval_form_view
    return eval_form_view(request, evaluation_id)


@login_required
def evaluation_preview(request, evaluation_id):
    """Evaluation preview - redirect to evaluations app"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    # Import here to avoid circular import
    from evaluations.views import evaluation_preview as eval_preview_view
    return eval_preview_view(request, evaluation_id)
