from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import StudentProfile, SupervisorProfile


class Company(models.Model):
    """Company/organization offering internships"""

    INDUSTRY_CHOICES = [
        ('TECH', 'Technology'),
        ('FINANCE', 'Finance & Banking'),
        ('RETAIL', 'Retail & E-commerce'),
        ('FMCG', 'FMCG'),
        ('AUTOMOTIVE', 'Automotive'),
        ('CONSULTING', 'Consulting'),
        ('MANUFACTURING', 'Manufacturing'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    description = models.TextField(blank=True)
    address = models.TextField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class JobPosting(models.Model):
    """Internship job postings"""

    TYPE_CHOICES = [
        ('ONSITE', 'On-site'),
        ('REMOTE', 'Remote'),
        ('HYBRID', 'Hybrid'),
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('DRAFT', 'Draft'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    benefits = models.TextField(blank=True)
    work_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ONSITE')
    location = models.CharField(max_length=255)
    duration_months = models.IntegerField(default=6, help_text="Internship duration in months")
    slots_available = models.IntegerField(default=1)
    application_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'

    def __str__(self):
        return f"{self.title} at {self.company.name}"


class Application(models.Model):
    """Student applications to job postings"""

    STATUS_CHOICES = [
        ('SENT', 'Sent'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    cv = models.FileField(
        upload_to='applications/cv/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SENT')
    notes = models.TextField(blank=True, help_text="Internal notes from company/admin")

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['student', 'job_posting']  # One application per student per job

    def __str__(self):
        return f"{self.student.full_name} → {self.job_posting.title}"


class InternshipPlacement(models.Model):
    """Confirmed internship placements"""

    STATUS_CHOICES = [
        ('PENDING_CONFIRMATION', 'Pending Confirmation'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('TERMINATED', 'Terminated'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='placements')
    supervisor = models.ForeignKey(
        SupervisorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_students'
    )

    # Company info
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    company_industry = models.CharField(max_length=100)

    # Position info
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    # Supervisor info (will be used to create supervisor account)
    supervisor_name = models.CharField(max_length=255)
    supervisor_email = models.EmailField()
    supervisor_whatsapp = models.CharField(max_length=20)
    supervisor_position = models.CharField(max_length=255)

    # Documents
    acceptance_letter = models.FileField(
        upload_to='internship_docs/acceptance_letters/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )

    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_CONFIRMATION')
    confirmed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='confirmed_placements'
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internship Placement'
        verbose_name_plural = 'Internship Placements'

    def __str__(self):
        return f"{self.student.full_name} at {self.company_name}"

    def get_duration_months(self):
        """Calculate duration in months"""
        delta = self.end_date - self.start_date
        return delta.days // 30
