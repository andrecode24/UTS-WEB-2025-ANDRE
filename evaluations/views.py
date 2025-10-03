from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Evaluation
from .forms import EvaluationForm


@login_required
def supervisor_evaluations(request):
    """List evaluations for supervisor"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    supervisor = request.user.supervisorprofile
    evaluations = Evaluation.objects.filter(supervisor=supervisor).order_by('-created_at')

    from datetime import date
    context = {
        'evaluations': evaluations,
        'today': date.today(),
    }
    return render(request, 'supervisor/evaluations.html', context)


@login_required
def evaluation_form(request, evaluation_id):
    """Evaluation form for supervisor"""
    if request.user.role != 'SUPERVISOR':
        return redirect('home')

    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    supervisor = request.user.supervisorprofile

    # Check ownership
    if evaluation.supervisor != supervisor:
        messages.error(request, 'Akses ditolak!')
        return redirect('supervisor:dashboard')

    # If already submitted, redirect to preview
    if evaluation.status == 'SUBMITTED':
        return redirect('supervisor:evaluation_preview', evaluation_id=evaluation.id)

    if request.method == 'POST':
        action = request.POST.get('action')
        form = EvaluationForm(request.POST, instance=evaluation)

        if form.is_valid():
            evaluation = form.save(commit=False)

            if action == 'submit':
                evaluation.status = 'SUBMITTED'
                evaluation.submitted_at = timezone.now()
                messages.success(request, 'Evaluasi berhasil disubmit!')
            else:  # save as draft
                evaluation.status = 'DRAFT'
                messages.success(request, 'Evaluasi berhasil disimpan sebagai draft.')

            evaluation.save()
            return redirect('supervisor:evaluations')
    else:
        form = EvaluationForm(instance=evaluation)

    # Get category averages
    category_averages = evaluation.get_category_averages()

    context = {
        'form': form,
        'evaluation': evaluation,
        'category_averages': category_averages,
        'placement': evaluation.placement,
        'student': evaluation.placement.student,
    }
    return render(request, 'supervisor/evaluation_form.html', context)


@login_required
def evaluation_preview(request, evaluation_id):
    """Preview evaluation before submit"""
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)

    # Check access
    if request.user.role == 'SUPERVISOR':
        if evaluation.supervisor != request.user.supervisorprofile:
            messages.error(request, 'Akses ditolak!')
            return redirect('supervisor:dashboard')
    elif request.user.role == 'STUDENT':
        if evaluation.placement.student != request.user.studentprofile:
            messages.error(request, 'Akses ditolak!')
            return redirect('student:dashboard')
    elif request.user.role != 'ADMIN':
        messages.error(request, 'Akses ditolak!')
        return redirect('home')

    category_averages = evaluation.get_category_averages()

    context = {
        'evaluation': evaluation,
        'category_averages': category_averages,
        'placement': evaluation.placement,
        'student': evaluation.placement.student,
    }
    return render(request, 'supervisor/evaluation_preview.html', context)
