from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, SupervisorProfile


class StudentRegistrationForm(forms.ModelForm):
    """Student registration form"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'nama.anda@student.prasetiyamulya.ac.id'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimal 8 karakter'
        }),
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Konfirmasi password'
        }),
        label='Konfirmasi Password'
    )

    class Meta:
        model = StudentProfile
        fields = ['full_name', 'nim', 'program', 'angkatan', 'gender', 'whatsapp', 'konsultasi_mentor_doc', 'sptjm_doc']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nim': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '8', 'pattern': '[0-9]{8}'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'angkatan': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.RadioSelect(),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'konsultasi_mentor_doc': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'sptjm_doc': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }
        labels = {
            'konsultasi_mentor_doc': 'Bukti Konsultasi dengan Mentor',
            'sptjm_doc': 'Bukti SPTJM (Surat Pernyataan Tanggung Jawab Mutlak)',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@student.prasetiyamulya.ac.id'):
            raise ValidationError('Email harus menggunakan domain @student.prasetiyamulya.ac.id')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email sudah terdaftar!')
        return email

    def clean_nim(self):
        nim = self.cleaned_data.get('nim')
        if StudentProfile.objects.filter(nim=nim).exists():
            raise ValidationError('NIM sudah terdaftar!')
        return nim

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError('Password tidak cocok!')

        return cleaned_data


class StudentProfileForm(forms.ModelForm):
    """Student profile update form"""

    class Meta:
        model = StudentProfile
        fields = ['full_name', 'whatsapp', 'ipk', 'skills', 'linkedin_url', 'github_url', 'cv', 'portfolio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'ipk': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pisahkan dengan koma (Python, Django, SQL, etc.)'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/yourname'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/yourname'}),
            'cv': forms.FileInput(attrs={'class': 'form-control'}),
            'portfolio': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Nama Lengkap',
            'whatsapp': 'WhatsApp',
            'ipk': 'IPK',
            'skills': 'Skills',
            'linkedin_url': 'LinkedIn URL',
            'github_url': 'GitHub URL',
            'cv': 'CV',
            'portfolio': 'Portfolio',
        }
