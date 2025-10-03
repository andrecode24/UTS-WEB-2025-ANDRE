from django import forms
from .models import Application, InternshipPlacement


class JobApplicationForm(forms.ModelForm):
    """Job application form"""

    class Meta:
        model = Application
        fields = ['cover_letter', 'cv']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Tuliskan cover letter Anda di sini...'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
        }
        labels = {
            'cover_letter': 'Cover Letter',
            'cv': 'Upload CV (PDF)'
        }


class InternshipConfirmationForm(forms.ModelForm):
    """Internship confirmation form"""

    class Meta:
        model = InternshipPlacement
        fields = [
            'company_name', 'company_address', 'company_industry',
            'position', 'start_date', 'end_date',
            'supervisor_name', 'supervisor_email', 'supervisor_whatsapp', 'supervisor_position',
            'acceptance_letter'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Technology, Finance, FMCG'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Engineer Intern'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supervisor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'supervisor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'supervisor_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'supervisor_position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Senior Manager'}),
            'acceptance_letter': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }
        labels = {
            'company_name': 'Nama Perusahaan',
            'company_address': 'Alamat Perusahaan',
            'company_industry': 'Bidang Usaha',
            'position': 'Posisi',
            'start_date': 'Tanggal Mulai',
            'end_date': 'Tanggal Selesai',
            'supervisor_name': 'Nama Supervisor',
            'supervisor_email': 'Email Supervisor',
            'supervisor_whatsapp': 'WhatsApp Supervisor',
            'supervisor_position': 'Jabatan Supervisor',
            'acceptance_letter': 'Surat Penerimaan (PDF, max 5MB)',
        }
