from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import MonthlyReport, ReportFeedback
from .forms import MonthlyReportForm, ReportFeedbackForm
from internships.models import InternshipPlacement


@login_required
def student_reports(request):
    """Student monthly reports list"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    try:
        student = request.user.studentprofile
        # Get active placement
        placement = InternshipPlacement.objects.filter(
            student=student,
            status='ACTIVE'
        ).first()

        if not placement:
            messages.warning(request, 'Anda belum memiliki magang aktif.')
            return redirect('student:dashboard')

        # Get all reports for this placement
        reports = MonthlyReport.objects.filter(placement=placement).order_by('-year', '-month')

        context = {
            'placement': placement,
            'reports': reports,
        }
        return render(request, 'student/reports.html', context)

    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('student:dashboard')


@login_required
def create_report(request):
    """Create new monthly report"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    student = request.user.studentprofile
    placement = InternshipPlacement.objects.filter(
        student=student,
        status='ACTIVE'
    ).first()

    if not placement:
        messages.warning(request, 'Anda belum memiliki magang aktif.')
        return redirect('student:dashboard')

    # Get current month/year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Check if report already exists
    existing_report = MonthlyReport.objects.filter(
        placement=placement,
        month=current_month,
        year=current_year
    ).first()

    if existing_report:
        return redirect('reports:edit_report', report_id=existing_report.id)

    if request.method == 'POST':
        action = request.POST.get('action')

        form = MonthlyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.placement = placement
            report.month = current_month
            report.year = current_year

            if action == 'submit':
                report.status = 'SUBMITTED'
                report.submitted_at = timezone.now()
                report.check_late_submission()
                messages.success(request, 'Laporan berhasil disubmit!')
            else:  # save as draft
                report.status = 'DRAFT'
                messages.success(request, 'Laporan berhasil disimpan sebagai draft.')

            report.save()
            return redirect('reports:student_reports')
    else:
        form = MonthlyReportForm()

    context = {
        'form': form,
        'placement': placement,
        'month': current_month,
        'year': current_year,
    }
    return render(request, 'student/report_form.html', context)


@login_required
def edit_report(request, report_id):
    """Edit monthly report"""
    if request.user.role != 'STUDENT':
        return redirect('home')

    report = get_object_or_404(MonthlyReport, id=report_id)
    student = request.user.studentprofile

    # Check ownership
    if report.placement.student != student:
        messages.error(request, 'Akses ditolak!')
        return redirect('student:dashboard')

    # Can't edit if already reviewed
    if report.status == 'REVIEWED':
        messages.warning(request, 'Laporan yang sudah di-review tidak bisa diedit.')
        return redirect('reports:student_reports')

    if request.method == 'POST':
        action = request.POST.get('action')

        form = MonthlyReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)

            if action == 'submit':
                report.status = 'SUBMITTED'
                report.submitted_at = timezone.now()
                report.check_late_submission()
                messages.success(request, 'Laporan berhasil disubmit!')
            else:  # save as draft
                report.status = 'DRAFT'
                messages.success(request, 'Laporan berhasil disimpan sebagai draft.')

            report.save()
            return redirect('reports:student_reports')
    else:
        form = MonthlyReportForm(instance=report)

    context = {
        'form': form,
        'report': report,
        'placement': report.placement,
    }
    return render(request, 'student/report_form.html', context)


@login_required
def view_report(request, report_id):
    """View report detail"""
    report = get_object_or_404(MonthlyReport, id=report_id)

    # Check access
    if request.user.role == 'STUDENT':
        if report.placement.student != request.user.studentprofile:
            messages.error(request, 'Akses ditolak!')
            return redirect('student:dashboard')
    elif request.user.role == 'SUPERVISOR':
        if report.placement.supervisor != request.user.supervisorprofile:
            messages.error(request, 'Akses ditolak!')
            return redirect('supervisor:dashboard')
    elif request.user.role != 'ADMIN':
        messages.error(request, 'Akses ditolak!')
        return redirect('home')

    feedbacks = ReportFeedback.objects.filter(report=report).order_by('-created_at')

    context = {
        'report': report,
        'feedbacks': feedbacks,
        'word_count': report.get_word_count(),
    }
    return render(request, 'student/report_detail.html', context)
