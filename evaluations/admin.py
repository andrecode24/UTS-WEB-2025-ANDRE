from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Evaluation, EvaluationReminder


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'evaluation_type', 'supervisor', 'overall_rating', 'status_badge', 'deadline', 'days_remaining']
    list_filter = ['evaluation_type', 'status', 'deadline', 'placement__company_name']
    search_fields = ['placement__student__full_name', 'placement__student__nim', 'supervisor__full_name', 'placement__company_name']
    ordering = ['-created_at']
    date_hierarchy = 'deadline'

    fieldsets = (
        ('Evaluation Info', {
            'fields': ('placement', 'supervisor', 'evaluation_type', 'period_month', 'deadline')
        }),
        ('Kualitas Kerja', {
            'fields': ('accuracy', 'neatness', 'task_completion', 'creativity'),
            'classes': ('collapse',)
        }),
        ('Produktivitas', {
            'fields': ('work_quantity', 'work_speed', 'consistency'),
            'classes': ('collapse',)
        }),
        ('Pengetahuan', {
            'fields': ('task_understanding', 'technical_skills', 'theory_application', 'learning_willingness'),
            'classes': ('collapse',)
        }),
        ('Kedisiplinan', {
            'fields': ('punctuality', 'rule_compliance', 'responsibility'),
            'classes': ('collapse',)
        }),
        ('Kerjasama', {
            'fields': ('teamwork', 'discussion_contribution', 'respect_opinions'),
            'classes': ('collapse',)
        }),
        ('Komunikasi', {
            'fields': ('verbal_communication', 'written_communication', 'presentation_skills'),
            'classes': ('collapse',)
        }),
        ('Sikap Profesional', {
            'fields': ('appearance', 'ethics', 'accept_criticism'),
            'classes': ('collapse',)
        }),
        ('Evaluasi Deskriptif', {
            'fields': ('achievements_description', 'strengths', 'improvements_needed', 'career_recommendation'),
            'classes': ('collapse',)
        }),
        ('Penilaian Akhir', {
            'fields': ('overall_rating', 'pass_recommendation', 'rehire_willingness')
        }),
        ('Status', {
            'fields': ('status', 'submitted_at')
        }),
    )

    readonly_fields = ['submitted_at', 'created_at']

    def student_name(self, obj):
        return obj.placement.student.full_name
    student_name.short_description = 'Student'

    def status_badge(self, obj):
        colors = {
            'PENDING': 'orange',
            'DRAFT': 'blue',
            'SUBMITTED': 'green',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def days_remaining(self, obj):
        """Display days remaining until deadline"""
        from datetime import date
        if obj.status == 'SUBMITTED':
            return format_html('<span style="color: green;">✓ Completed</span>')

        today = date.today()
        delta = (obj.deadline - today).days

        if delta < 0:
            return format_html('<span style="color: red; font-weight: bold;">⚠ {} days overdue</span>', abs(delta))
        elif delta == 0:
            return format_html('<span style="color: orange; font-weight: bold;">⏰ Due today!</span>')
        elif delta <= 3:
            return format_html('<span style="color: orange;">{} days</span>', delta)
        else:
            return format_html('<span style="color: gray;">{} days</span>', delta)
    days_remaining.short_description = 'Time Remaining'

    actions = ['calculate_ratings', 'mark_submitted', 'send_reminder']

    def calculate_ratings(self, request, queryset):
        updated = 0
        for evaluation in queryset:
            evaluation.calculate_overall_rating()
            updated += 1
        self.message_user(request, f'{updated} evaluations calculated.')
    calculate_ratings.short_description = 'Calculate overall ratings'

    def mark_submitted(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='DRAFT').update(
            status='SUBMITTED',
            submitted_at=timezone.now()
        )
        self.message_user(request, f'{updated} evaluations marked as submitted.')
    mark_submitted.short_description = 'Mark as submitted'

    def send_reminder(self, request, queryset):
        """Send reminder notification to supervisors"""
        from notifications.models import Notification
        count = 0
        for evaluation in queryset.filter(status__in=['PENDING', 'DRAFT']):
            Notification.send_to_user(
                user=evaluation.supervisor.user,
                title=f'Reminder: Evaluasi {evaluation.get_evaluation_type_display()}',
                message=f'Anda memiliki evaluasi yang perlu diselesaikan untuk mahasiswa {evaluation.placement.student.full_name}. Deadline: {evaluation.deadline.strftime("%d %B %Y")}',
                notification_type='WARNING',
                category='EVALUATION',
                link=f'/supervisor/evaluations/{evaluation.id}/'
            )
            count += 1
        self.message_user(request, f'{count} reminder(s) sent to supervisors.')
    send_reminder.short_description = 'Send reminder to supervisors'

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('placement__student', 'supervisor')


@admin.register(EvaluationReminder)
class EvaluationReminderAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'days_before_deadline', 'sent_at']
    list_filter = ['days_before_deadline', 'sent_at']
    search_fields = ['evaluation__placement__student__full_name']
    ordering = ['-sent_at']

    def has_add_permission(self, request):
        return False
