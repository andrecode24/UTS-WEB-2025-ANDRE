from django import forms
from django.core.exceptions import ValidationError
from .models import MonthlyReport, ReportFeedback


class MonthlyReportForm(forms.ModelForm):
    """Monthly report form"""

    class Meta:
        model = MonthlyReport
        fields = [
            'company_profile',
            'job_description',
            'work_environment',
            'useful_skills',
            'needed_skills',
            'achievements',
            'challenges',
            'next_month_plan'
        ]
        widgets = {
            'company_profile': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tuliskan profil perusahaan (hanya untuk laporan bulan pertama)'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Jelaskan job description dan tugas yang Anda kerjakan (minimal 500 karakter)'
            }),
            'work_environment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsikan suasana lingkungan kerja (minimal 100 karakter)'
            }),
            'useful_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Skills dari kuliah yang berguna di pekerjaan ini (minimal 100 karakter)'
            }),
            'needed_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Skills yang dibutuhkan tapi belum dipelajari (minimal 100 karakter)'
            }),
            'achievements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Pencapaian bulan ini (minimal 100 karakter)'
            }),
            'challenges': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Kendala yang dihadapi (minimal 100 karakter)'
            }),
            'next_month_plan': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Rencana untuk bulan depan (minimal 100 karakter)'
            }),
        }
        labels = {
            'company_profile': 'Profil Perusahaan (Bulan Pertama Saja)',
            'job_description': 'Job Description & Tugas',
            'work_environment': 'Suasana Lingkungan Kerja',
            'useful_skills': 'Skills dari Kuliah yang Berguna',
            'needed_skills': 'Skills yang Dibutuhkan tapi Belum Dipelajari',
            'achievements': 'Achievement Bulan Ini',
            'challenges': 'Kendala yang Dihadapi',
            'next_month_plan': 'Rencana Bulan Depan',
        }

    def clean(self):
        cleaned_data = super().clean()

        # Check total word count
        total_words = 0
        fields_to_count = [
            'job_description', 'work_environment', 'useful_skills',
            'needed_skills', 'achievements', 'challenges', 'next_month_plan'
        ]

        for field in fields_to_count:
            value = cleaned_data.get(field, '')
            if value:
                total_words += len(value.split())

        if total_words < 500:
            raise ValidationError(f'Total laporan harus minimal 500 kata. Saat ini: {total_words} kata.')

        return cleaned_data


class ReportFeedbackForm(forms.ModelForm):
    """Report feedback form"""

    class Meta:
        model = ReportFeedback
        fields = ['content', 'requires_revision']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tuliskan feedback untuk laporan ini...'
            }),
            'requires_revision': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'content': 'Feedback',
            'requires_revision': 'Perlu Revisi?',
        }
