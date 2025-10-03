from django.contrib import admin
from django.utils.html import format_html
from .models import MonthlyReport, ReportFeedback


@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'month', 'year', 'status_badge', 'word_count', 'is_late', 'submitted_at']
    list_filter = ['status', 'is_late', 'year', 'month']
    search_fields = ['placement__student__full_name', 'placement__student__nim']
    ordering = ['-year', '-month']

    fieldsets = (
        ('Report Info', {
            'fields': ('placement', 'month', 'year')
        }),
        ('Company Profile (Bulan Pertama)', {
            'fields': ('company_profile',),
            'classes': ('collapse',)
        }),
        ('Laporan Bulanan', {
            'fields': (
                'job_description',
                'work_environment',
                'useful_skills',
                'needed_skills',
                'achievements',
                'challenges',
                'next_month_plan'
            )
        }),
        ('Status', {
            'fields': ('status', 'submitted_at', 'is_late', 'reviewed_by', 'reviewed_at')
        }),
    )

    readonly_fields = ['submitted_at', 'reviewed_at', 'created_at']

    def student_name(self, obj):
        return obj.placement.student.full_name
    student_name.short_description = 'Student'

    def word_count(self, obj):
        count = obj.get_word_count()
        color = 'green' if count >= 500 else 'red'
        return format_html(
            '<span style="color: {};">{} words</span>',
            color,
            count
        )
    word_count.short_description = 'Word Count'

    def status_badge(self, obj):
        colors = {
            'DRAFT': 'gray',
            'SUBMITTED': 'blue',
            'REVIEWED': 'green',
            'REVISION_REQUESTED': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_reviewed', 'request_revision']

    def mark_reviewed(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for report in queryset.filter(status='SUBMITTED'):
            report.status = 'REVIEWED'
            report.reviewed_by = request.user
            report.reviewed_at = timezone.now()
            report.save()
            updated += 1
        self.message_user(request, f'{updated} reports marked as reviewed.')
    mark_reviewed.short_description = 'Mark as reviewed'

    def request_revision(self, request, queryset):
        updated = queryset.filter(status='SUBMITTED').update(status='REVISION_REQUESTED')
        self.message_user(request, f'{updated} reports need revision.')
    request_revision.short_description = 'Request revision'


@admin.register(ReportFeedback)
class ReportFeedbackAdmin(admin.ModelAdmin):
    list_display = ['report', 'reviewer', 'requires_revision', 'created_at']
    list_filter = ['requires_revision', 'created_at']
    search_fields = ['report__placement__student__full_name', 'content']
    ordering = ['-created_at']

    fieldsets = (
        ('Feedback Info', {
            'fields': ('report', 'reviewer', 'requires_revision')
        }),
        ('Feedback Content', {
            'fields': ('content',)
        }),
    )

    readonly_fields = ['created_at']
