from django.db import models
from django.core.validators import MinLengthValidator
from internships.models import InternshipPlacement
from accounts.models import User


class MonthlyReport(models.Model):
    """Monthly progress reports submitted by students"""

    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('REVIEWED', 'Reviewed'),
        ('REVISION_REQUESTED', 'Revision Requested'),
    ]

    MONTH_CHOICES = [
        (1, 'Januari'), (2, 'Februari'), (3, 'Maret'), (4, 'April'),
        (5, 'Mei'), (6, 'Juni'), (7, 'Juli'), (8, 'Agustus'),
        (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Desember'),
    ]

    placement = models.ForeignKey(InternshipPlacement, on_delete=models.CASCADE, related_name='monthly_reports')
    month = models.IntegerField(choices=MONTH_CHOICES, help_text="Month number (1, 2, 3, etc.)")
    year = models.IntegerField()

    # Company profile (first month only)
    company_profile = models.TextField(
        blank=True,
        help_text="Profil perusahaan (bulan pertama saja)"
    )

    # Monthly report content
    job_description = models.TextField(
        help_text="Job description dan tugas yang dikerjakan",
        validators=[MinLengthValidator(500, "Minimal 500 karakter")]
    )
    work_environment = models.TextField(
        help_text="Suasana lingkungan kerja",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )
    useful_skills = models.TextField(
        help_text="Skills dari kuliah yang berguna",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )
    needed_skills = models.TextField(
        help_text="Skills yang dibutuhkan tapi belum dipelajari",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )
    achievements = models.TextField(
        help_text="Achievement bulan ini",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )
    challenges = models.TextField(
        help_text="Kendala yang dihadapi",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )
    next_month_plan = models.TextField(
        help_text="Rencana bulan depan",
        validators=[MinLengthValidator(100, "Minimal 100 karakter")]
    )

    # Status and review
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['placement', 'month', 'year']
        verbose_name = 'Monthly Report'
        verbose_name_plural = 'Monthly Reports'

    def __str__(self):
        return f"{self.placement.student.full_name} - {self.month}/{self.year}"

    def get_deadline(self):
        """Get deadline for this report (30th of the month)"""
        from datetime import date
        return date(self.year, self.month, 30)

    def check_late_submission(self):
        """Check if report is submitted late"""
        if self.submitted_at:
            deadline = self.get_deadline()
            if self.submitted_at.date() > deadline:
                self.is_late = True
                self.save()
                return True
        return False

    def get_word_count(self):
        """Calculate total word count of report"""
        content = ' '.join([
            self.job_description,
            self.work_environment,
            self.useful_skills,
            self.needed_skills,
            self.achievements,
            self.challenges,
            self.next_month_plan
        ])
        return len(content.split())


class ReportFeedback(models.Model):
    """Feedback from admin or supervisor on monthly reports"""

    report = models.ForeignKey(MonthlyReport, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedbacks')
    content = models.TextField()
    requires_revision = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report Feedback'
        verbose_name_plural = 'Report Feedbacks'

    def __str__(self):
        return f"Feedback for {self.report}"
