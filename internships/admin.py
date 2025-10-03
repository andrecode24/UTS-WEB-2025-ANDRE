from django.contrib import admin
from django.utils.html import format_html
from .models import Company, JobPosting, Application, InternshipPlacement


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'website', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'industry', 'description', 'address')
        }),
        ('Contact & Branding', {
            'fields': ('website', 'logo')
        }),
    )


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'work_type', 'location', 'status_badge', 'application_deadline']
    list_filter = ['status', 'work_type', 'company', 'created_at']
    search_fields = ['title', 'description', 'company__name']
    ordering = ['-created_at']

    fieldsets = (
        ('Job Information', {
            'fields': ('company', 'title', 'description', 'requirements', 'benefits')
        }),
        ('Work Details', {
            'fields': ('work_type', 'location', 'duration_months', 'slots_available')
        }),
        ('Status', {
            'fields': ('status', 'application_deadline')
        }),
    )

    def status_badge(self, obj):
        colors = {
            'OPEN': 'green',
            'CLOSED': 'red',
            'DRAFT': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job_posting', 'status_badge', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['student__full_name', 'student__nim', 'job_posting__title']
    ordering = ['-applied_at']

    fieldsets = (
        ('Application Info', {
            'fields': ('student', 'job_posting')
        }),
        ('Documents', {
            'fields': ('cover_letter', 'cv')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
    )

    readonly_fields = ['applied_at']

    def status_badge(self, obj):
        colors = {
            'SENT': 'blue',
            'UNDER_REVIEW': 'orange',
            'ACCEPTED': 'green',
            'REJECTED': 'red',
            'WITHDRAWN': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_under_review', 'mark_accepted', 'mark_rejected']

    def mark_under_review(self, request, queryset):
        updated = queryset.update(status='UNDER_REVIEW')
        self.message_user(request, f'{updated} applications marked as under review.')
    mark_under_review.short_description = 'Mark as under review'

    def mark_accepted(self, request, queryset):
        updated = queryset.update(status='ACCEPTED')
        self.message_user(request, f'{updated} applications marked as accepted.')
    mark_accepted.short_description = 'Mark as accepted'

    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated} applications marked as rejected.')
    mark_rejected.short_description = 'Mark as rejected'


@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    list_display = ['student', 'company_name', 'position', 'start_date', 'end_date', 'status_badge']
    list_filter = ['status', 'start_date', 'company_industry']
    search_fields = ['student__full_name', 'student__nim', 'company_name', 'supervisor_name']
    ordering = ['-created_at']

    fieldsets = (
        ('Student', {
            'fields': ('student', 'supervisor')
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_address', 'company_industry')
        }),
        ('Position Details', {
            'fields': ('position', 'start_date', 'end_date')
        }),
        ('Supervisor Information', {
            'fields': ('supervisor_name', 'supervisor_email', 'supervisor_whatsapp', 'supervisor_position')
        }),
        ('Documents', {
            'fields': ('acceptance_letter',)
        }),
        ('Status', {
            'fields': ('status', 'confirmed_by', 'confirmed_at')
        }),
    )

    readonly_fields = ['confirmed_at', 'created_at']

    def status_badge(self, obj):
        colors = {
            'PENDING_CONFIRMATION': 'orange',
            'ACTIVE': 'green',
            'COMPLETED': 'blue',
            'TERMINATED': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['confirm_placement', 'complete_placement']

    def confirm_placement(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for placement in queryset.filter(status='PENDING_CONFIRMATION'):
            placement.status = 'ACTIVE'
            placement.confirmed_by = request.user
            placement.confirmed_at = timezone.now()
            placement.save()

            # Update student status
            placement.student.status = 'ACTIVE'
            placement.student.save()

            updated += 1

        self.message_user(request, f'{updated} placements confirmed.')
    confirm_placement.short_description = 'Confirm placement'

    def complete_placement(self, request, queryset):
        updated = 0
        for placement in queryset.filter(status='ACTIVE'):
            placement.status = 'COMPLETED'
            placement.save()

            # Update student status
            placement.student.status = 'COMPLETED'
            placement.student.save()

            updated += 1

        self.message_user(request, f'{updated} placements completed.')
    complete_placement.short_description = 'Mark as completed'
