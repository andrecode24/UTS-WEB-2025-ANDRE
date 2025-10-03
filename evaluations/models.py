from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from internships.models import InternshipPlacement
from accounts.models import SupervisorProfile, User


class Evaluation(models.Model):
    """UTS and UAS evaluations by supervisors"""

    TYPE_CHOICES = [
        ('UTS', 'Ujian Tengah Semester'),
        ('UAS', 'Ujian Akhir Semester'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
    ]

    placement = models.ForeignKey(InternshipPlacement, on_delete=models.CASCADE, related_name='evaluations')
    supervisor = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE, related_name='evaluations')
    evaluation_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    period_month = models.IntegerField(help_text="Bulan ke berapa evaluasi ini (2 untuk UTS, terakhir untuk UAS)")

    # Penilaian Kualitas Kerja (1-5)
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Keakuratan dan ketelitian",
        null=True, blank=True
    )
    neatness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kerapihan hasil kerja",
        null=True, blank=True
    )
    task_completion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kemampuan menyelesaikan tugas",
        null=True, blank=True
    )
    creativity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kreativitas dan inovasi",
        null=True, blank=True
    )

    # Produktivitas (1-5)
    work_quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Jumlah pekerjaan diselesaikan",
        null=True, blank=True
    )
    work_speed = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kecepatan menyelesaikan tugas",
        null=True, blank=True
    )
    consistency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Konsistensi produktivitas",
        null=True, blank=True
    )

    # Pengetahuan (1-5)
    task_understanding = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Pemahaman tugas",
        null=True, blank=True
    )
    technical_skills = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Penguasaan technical skills",
        null=True, blank=True
    )
    theory_application = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Aplikasi teori ke praktik",
        null=True, blank=True
    )
    learning_willingness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kemauan belajar",
        null=True, blank=True
    )

    # Kedisiplinan (1-5)
    punctuality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Ketepatan waktu hadir",
        null=True, blank=True
    )
    rule_compliance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kepatuhan peraturan",
        null=True, blank=True
    )
    responsibility = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Tanggung jawab",
        null=True, blank=True
    )

    # Kerjasama (1-5)
    teamwork = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kemampuan kerja tim",
        null=True, blank=True
    )
    discussion_contribution = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kontribusi dalam diskusi",
        null=True, blank=True
    )
    respect_opinions = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Menghargai pendapat orang",
        null=True, blank=True
    )

    # Komunikasi (1-5)
    verbal_communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Komunikasi verbal",
        null=True, blank=True
    )
    written_communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Komunikasi tertulis",
        null=True, blank=True
    )
    presentation_skills = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Kemampuan presentasi",
        null=True, blank=True
    )

    # Sikap Profesional (1-5)
    appearance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Penampilan",
        null=True, blank=True
    )
    ethics = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Etika dan sopan santun",
        null=True, blank=True
    )
    accept_criticism = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Menerima kritik",
        null=True, blank=True
    )

    # Evaluasi Deskriptif
    achievements_description = models.TextField(
        blank=True,
        help_text="Pencapaian selama magang"
    )
    strengths = models.TextField(
        blank=True,
        help_text="Kekuatan mahasiswa"
    )
    improvements_needed = models.TextField(
        blank=True,
        help_text="Area yang perlu diperbaiki"
    )
    career_recommendation = models.TextField(
        blank=True,
        help_text="Rekomendasi karir"
    )

    # Penilaian Akhir
    overall_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        help_text="Overall rating (auto-calculated)"
    )
    pass_recommendation = models.BooleanField(
        default=False,
        help_text="Rekomendasi kelulusan"
    )
    rehire_willingness = models.BooleanField(
        default=False,
        help_text="Bersedia terima mahasiswa lagi?"
    )

    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    deadline = models.DateField()
    submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['placement', 'evaluation_type']
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'

    def __str__(self):
        return f"{self.evaluation_type} - {self.placement.student.full_name}"

    def calculate_overall_rating(self):
        """Calculate overall rating from all criteria"""
        criteria = [
            # Kualitas Kerja
            self.accuracy, self.neatness, self.task_completion, self.creativity,
            # Produktivitas
            self.work_quantity, self.work_speed, self.consistency,
            # Pengetahuan
            self.task_understanding, self.technical_skills, self.theory_application, self.learning_willingness,
            # Kedisiplinan
            self.punctuality, self.rule_compliance, self.responsibility,
            # Kerjasama
            self.teamwork, self.discussion_contribution, self.respect_opinions,
            # Komunikasi
            self.verbal_communication, self.written_communication, self.presentation_skills,
            # Sikap Profesional
            self.appearance, self.ethics, self.accept_criticism,
        ]

        # Filter out None values
        valid_scores = [score for score in criteria if score is not None]

        if valid_scores:
            self.overall_rating = sum(valid_scores) / len(valid_scores)
            self.save()
            return self.overall_rating
        return None

    def is_passing(self):
        """Check if student passes (minimum 3.0)"""
        if self.overall_rating:
            return self.overall_rating >= 3.0
        return False

    def get_category_averages(self):
        """Get average scores by category"""
        categories = {
            'Kualitas Kerja': [self.accuracy, self.neatness, self.task_completion, self.creativity],
            'Produktivitas': [self.work_quantity, self.work_speed, self.consistency],
            'Pengetahuan': [self.task_understanding, self.technical_skills, self.theory_application, self.learning_willingness],
            'Kedisiplinan': [self.punctuality, self.rule_compliance, self.responsibility],
            'Kerjasama': [self.teamwork, self.discussion_contribution, self.respect_opinions],
            'Komunikasi': [self.verbal_communication, self.written_communication, self.presentation_skills],
            'Sikap Profesional': [self.appearance, self.ethics, self.accept_criticism],
        }

        averages = {}
        for category, scores in categories.items():
            valid_scores = [s for s in scores if s is not None]
            if valid_scores:
                averages[category] = sum(valid_scores) / len(valid_scores)
            else:
                averages[category] = None

        return averages


class EvaluationReminder(models.Model):
    """Track reminders sent to supervisors"""

    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='reminders')
    sent_at = models.DateTimeField(auto_now_add=True)
    days_before_deadline = models.IntegerField()

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"Reminder for {self.evaluation} ({self.days_before_deadline} days before)"
