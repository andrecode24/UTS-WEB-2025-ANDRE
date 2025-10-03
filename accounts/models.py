from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_size(value):
    """Validate file size is max 5MB"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("File size tidak boleh lebih dari 5MB")
    return value


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with role-based access"""

    ROLE_CHOICES = [
        ('STUDENT', 'Student'),
        ('SUPERVISOR', 'Supervisor'),
        ('ADMIN', 'Admin'),
    ]

    username = None  # Remove username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True)
    is_email_verified = models.BooleanField(default=False)
    force_password_change = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        # Auto-set first_name and last_name from full_name if provided
        if hasattr(self, 'studentprofile'):
            self.first_name = self.studentprofile.full_name.split()[0] if self.studentprofile.full_name else ''
            self.last_name = ' '.join(self.studentprofile.full_name.split()[1:]) if len(self.studentprofile.full_name.split()) > 1 else ''
        super().save(*args, **kwargs)


class StudentProfile(models.Model):
    """Extended profile for students"""

    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('ACTIVE', 'Active (Has Internship)'),
        ('AT_RISK', 'At Risk (No Internship > 2 months)'),
        ('COMPLETED', 'Completed'),
    ]

    PROGRAM_CHOICES = [
        ('MN', 'S1 Manajemen'),
        ('BP', 'S1 Bisnis Pariwisata'),
        ('AK', 'S1 Akuntansi'),
        ('EB', 'S1 Ekonomi Bisnis'),
        ('CSE', 'S1 Computer Systems Engineering'),
        ('FBT', 'S1 Food Business Technology'),
        ('PDI', 'S1 Product Design Innovation'),
        ('DBT', 'S1 Digital Business Technology'),
        ('BM', 'S1 Business Mathematics'),
        ('EBT', 'S1 Energy Business Technology'),
        ('HBI', 'S1 Hukum Bisnis Internasional'),
    ]

    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    full_name = models.CharField(max_length=255)
    nim = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(r'^\d{8}$', 'NIM must be exactly 8 digits'),
        ]
    )
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES)
    angkatan = models.CharField(max_length=4)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    whatsapp = models.CharField(max_length=20)

    # Documents
    konsultasi_mentor_doc = models.FileField(
        upload_to='student_docs/konsultasi/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
        ],
        help_text="Bukti konsultasi dengan mentor (PDF, max 5MB)"
    )
    sptjm_doc = models.FileField(
        upload_to='student_docs/sptjm/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
        ],
        help_text="SPTJM - Surat Pernyataan Tanggung Jawab Mutlak (PDF, max 5MB)"
    )

    # Profile completion
    cv = models.FileField(upload_to='student_docs/cv/', blank=True)
    portfolio = models.FileField(upload_to='student_docs/portfolio/', blank=True)
    ipk = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return f"{self.nim} - {self.full_name}"

    def clean(self):
        # Validate email domain
        if self.user.email and not self.user.email.endswith('@student.prasetiyamulya.ac.id'):
            raise ValidationError({
                'user': 'Email must use @student.prasetiyamulya.ac.id domain'
            })

    def check_at_risk_status(self):
        """Check if student should be marked as at-risk (no internship > 2 months)"""
        if self.status == 'APPROVED' and self.approved_at:
            from internships.models import InternshipPlacement
            has_internship = InternshipPlacement.objects.filter(
                student=self,
                status='ACTIVE'
            ).exists()

            if not has_internship:
                days_since_approval = (timezone.now() - self.approved_at).days
                if days_since_approval > 60:
                    self.status = 'AT_RISK'
                    self.save()
                    return True
        return False

    def get_skills_list(self):
        """Return skills as a list"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]


class SupervisorProfile(models.Model):
    """Extended profile for supervisors"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisorprofile')
    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=20)

    # Auto-generated credentials info
    is_first_login = models.BooleanField(default=True)
    credentials_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Supervisor Profile'
        verbose_name_plural = 'Supervisor Profiles'

    def __str__(self):
        return f"{self.full_name} - {self.company_name}"


class AdminProfile(models.Model):
    """Extended profile for admin users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adminprofile')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'

    def __str__(self):
        return f"{self.full_name} (Admin)"
