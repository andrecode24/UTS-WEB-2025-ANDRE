from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, StudentProfile, SupervisorProfile, AdminProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'role', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Security', {'fields': ('force_password_change', 'is_email_verified')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['nim', 'full_name', 'program', 'angkatan', 'status_badge', 'created_at']
    list_filter = ['status', 'program', 'angkatan', 'gender']
    search_fields = ['nim', 'full_name', 'user__email']
    ordering = ['-created_at']

    fieldsets = (
        ('User Account', {'fields': ('user',)}),
        ('Personal Information', {
            'fields': ('full_name', 'nim', 'program', 'angkatan', 'gender', 'whatsapp')
        }),
        ('Documents', {
            'fields': ('konsultasi_mentor_doc', 'sptjm_doc')
        }),
        ('Profile Completion', {
            'fields': ('cv', 'portfolio', 'ipk', 'skills', 'linkedin_url', 'github_url')
        }),
        ('Status', {
            'fields': ('status', 'approved_at')
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def status_badge(self, obj):
        colors = {
            'APPROVED': 'green',
            'ACTIVE': 'blue',
            'AT_RISK': 'red',
            'COMPLETED': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_at_risk']

    def mark_at_risk(self, request, queryset):
        updated = queryset.update(status='AT_RISK')
        self.message_user(request, f'{updated} students marked as at-risk.')
    mark_at_risk.short_description = 'Mark as at-risk'


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company_name', 'position', 'user_email', 'is_first_login', 'created_at']
    list_filter = ['is_first_login', 'company_name']
    search_fields = ['full_name', 'company_name', 'user__email']
    ordering = ['-created_at']

    fieldsets = (
        ('User Account', {'fields': ('user',)}),
        ('Supervisor Information', {
            'fields': ('full_name', 'company_name', 'position', 'whatsapp')
        }),
        ('Account Status', {
            'fields': ('is_first_login', 'credentials_sent_at')
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'credentials_sent_at']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user_email', 'phone_number', 'created_at']
    search_fields = ['full_name', 'user__email']
    ordering = ['-created_at']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
