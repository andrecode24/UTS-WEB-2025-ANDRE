from django import forms
from .models import Evaluation


class EvaluationForm(forms.ModelForm):
    """Evaluation form for UTS/UAS"""

    class Meta:
        model = Evaluation
        fields = [
            # Kualitas Kerja
            'accuracy', 'neatness', 'task_completion', 'creativity',
            # Produktivitas
            'work_quantity', 'work_speed', 'consistency',
            # Pengetahuan
            'task_understanding', 'technical_skills', 'theory_application', 'learning_willingness',
            # Kedisiplinan
            'punctuality', 'rule_compliance', 'responsibility',
            # Kerjasama
            'teamwork', 'discussion_contribution', 'respect_opinions',
            # Komunikasi
            'verbal_communication', 'written_communication', 'presentation_skills',
            # Sikap Profesional
            'appearance', 'ethics', 'accept_criticism',
            # Evaluasi Deskriptif
            'achievements_description', 'strengths', 'improvements_needed', 'career_recommendation',
            # Penilaian Akhir
            'pass_recommendation', 'rehire_willingness',
        ]

        # Create widgets for all rating fields (1-5)
        rating_widget = forms.RadioSelect(
            choices=[(i, str(i)) for i in range(1, 6)],
            attrs={'class': 'form-check-inline'}
        )

        widgets = {
            # Kualitas Kerja
            'accuracy': rating_widget,
            'neatness': rating_widget,
            'task_completion': rating_widget,
            'creativity': rating_widget,
            # Produktivitas
            'work_quantity': rating_widget,
            'work_speed': rating_widget,
            'consistency': rating_widget,
            # Pengetahuan
            'task_understanding': rating_widget,
            'technical_skills': rating_widget,
            'theory_application': rating_widget,
            'learning_willingness': rating_widget,
            # Kedisiplinan
            'punctuality': rating_widget,
            'rule_compliance': rating_widget,
            'responsibility': rating_widget,
            # Kerjasama
            'teamwork': rating_widget,
            'discussion_contribution': rating_widget,
            'respect_opinions': rating_widget,
            # Komunikasi
            'verbal_communication': rating_widget,
            'written_communication': rating_widget,
            'presentation_skills': rating_widget,
            # Sikap Profesional
            'appearance': rating_widget,
            'ethics': rating_widget,
            'accept_criticism': rating_widget,
            # Deskriptif
            'achievements_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'improvements_needed': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'career_recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # Final
            'pass_recommendation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rehire_willingness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        labels = {
            # Kualitas Kerja
            'accuracy': 'Keakuratan dan Ketelitian',
            'neatness': 'Kerapihan Hasil Kerja',
            'task_completion': 'Kemampuan Menyelesaikan Tugas',
            'creativity': 'Kreativitas dan Inovasi',
            # Produktivitas
            'work_quantity': 'Jumlah Pekerjaan Diselesaikan',
            'work_speed': 'Kecepatan Menyelesaikan Tugas',
            'consistency': 'Konsistensi Produktivitas',
            # Pengetahuan
            'task_understanding': 'Pemahaman Tugas',
            'technical_skills': 'Penguasaan Technical Skills',
            'theory_application': 'Aplikasi Teori ke Praktik',
            'learning_willingness': 'Kemauan Belajar',
            # Kedisiplinan
            'punctuality': 'Ketepatan Waktu Hadir',
            'rule_compliance': 'Kepatuhan Peraturan',
            'responsibility': 'Tanggung Jawab',
            # Kerjasama
            'teamwork': 'Kemampuan Kerja Tim',
            'discussion_contribution': 'Kontribusi dalam Diskusi',
            'respect_opinions': 'Menghargai Pendapat Orang',
            # Komunikasi
            'verbal_communication': 'Komunikasi Verbal',
            'written_communication': 'Komunikasi Tertulis',
            'presentation_skills': 'Kemampuan Presentasi',
            # Sikap Profesional
            'appearance': 'Penampilan',
            'ethics': 'Etika dan Sopan Santun',
            'accept_criticism': 'Menerima Kritik',
            # Deskriptif
            'achievements_description': 'Pencapaian Selama Magang',
            'strengths': 'Kekuatan Mahasiswa',
            'improvements_needed': 'Area yang Perlu Diperbaiki',
            'career_recommendation': 'Rekomendasi Karir',
            # Final
            'pass_recommendation': 'Rekomendasi Kelulusan',
            'rehire_willingness': 'Bersedia Terima Mahasiswa Lagi?',
        }

    def save(self, commit=True):
        evaluation = super().save(commit=False)
        # Auto-calculate overall rating
        evaluation.calculate_overall_rating()
        if commit:
            evaluation.save()
        return evaluation
