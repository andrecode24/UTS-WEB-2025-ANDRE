from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from accounts.models import User, StudentProfile, SupervisorProfile, AdminProfile
from internships.models import Company, JobPosting, Application, InternshipPlacement
from evaluations.models import Evaluation
from reports.models import MonthlyReport


class Command(BaseCommand):
    help = 'Seed database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()

        # Create Admin
        self.stdout.write('Creating admin user...')
        admin_user = User.objects.create_superuser(
            email='admin@prasetiyamulya.ac.id',
            password='admin123',
            role='ADMIN'
        )
        AdminProfile.objects.create(
            user=admin_user,
            full_name='Admin COOP',
            phone_number='081234567890'
        )

        # Create Companies
        self.stdout.write('Creating companies...')
        companies_data = [
            {
                'name': 'PT Tokopedia',
                'industry': 'TECH',
                'description': 'Leading e-commerce platform in Indonesia',
                'address': 'Wisma 77 Tower 2, Jakarta Selatan',
                'website': 'https://www.tokopedia.com'
            },
            {
                'name': 'PT Bank Central Asia',
                'industry': 'FINANCE',
                'description': 'Largest private bank in Indonesia',
                'address': 'Menara BCA, Jakarta Pusat',
                'website': 'https://www.bca.co.id'
            },
            {
                'name': 'PT Gojek Indonesia',
                'industry': 'TECH',
                'description': 'Super-app providing on-demand services',
                'address': 'Pasaraya Blok M, Jakarta Selatan',
                'website': 'https://www.gojek.com'
            },
            {
                'name': 'PT Unilever Indonesia',
                'industry': 'FMCG',
                'description': 'Leading FMCG company',
                'address': 'Graha Unilever, BSD City',
                'website': 'https://www.unilever.co.id'
            },
            {
                'name': 'PT Astra International',
                'industry': 'AUTOMOTIVE',
                'description': 'Diversified automotive company',
                'address': 'Jl. Gaya Motor Raya, Jakarta Utara',
                'website': 'https://www.astra.co.id'
            },
        ]

        companies = []
        for company_data in companies_data:
            company = Company.objects.create(**company_data)
            companies.append(company)
            self.stdout.write(f'  Created company: {company.name}')

        # Create Job Postings
        self.stdout.write('Creating job postings...')
        job_postings_data = [
            {
                'company': companies[0],
                'title': 'Software Engineer Intern',
                'description': 'Work on cutting-edge e-commerce platform',
                'requirements': 'Computer Science student, familiar with Python/Java',
                'benefits': 'Monthly allowance, learning opportunity, mentorship',
                'work_type': 'HYBRID',
                'location': 'Jakarta Selatan',
                'duration_months': 6,
                'slots_available': 3,
                'application_deadline': datetime.now().date() + timedelta(days=30),
                'status': 'OPEN'
            },
            {
                'company': companies[1],
                'title': 'Data Analyst Intern',
                'description': 'Analyze banking data and create insights',
                'requirements': 'Statistics/Computer Science background, SQL knowledge',
                'benefits': 'Competitive allowance, certificate',
                'work_type': 'ONSITE',
                'location': 'Jakarta Pusat',
                'duration_months': 6,
                'slots_available': 2,
                'application_deadline': datetime.now().date() + timedelta(days=25),
                'status': 'OPEN'
            },
            {
                'company': companies[2],
                'title': 'Business Analyst Intern',
                'description': 'Support product and business teams',
                'requirements': 'Business/Management student, analytical thinking',
                'benefits': 'Monthly stipend, flexible hours',
                'work_type': 'HYBRID',
                'location': 'Jakarta Selatan',
                'duration_months': 5,
                'slots_available': 2,
                'application_deadline': datetime.now().date() + timedelta(days=20),
                'status': 'OPEN'
            },
            {
                'company': companies[3],
                'title': 'Marketing Intern',
                'description': 'Support marketing campaigns and brand management',
                'requirements': 'Marketing/Communication student, creative mindset',
                'benefits': 'Allowance, product training',
                'work_type': 'ONSITE',
                'location': 'BSD City',
                'duration_months': 6,
                'slots_available': 3,
                'application_deadline': datetime.now().date() + timedelta(days=15),
                'status': 'OPEN'
            },
            {
                'company': companies[4],
                'title': 'Finance Intern',
                'description': 'Assist finance team with analysis and reporting',
                'requirements': 'Accounting/Finance student, Excel proficiency',
                'benefits': 'Competitive allowance, certification',
                'work_type': 'ONSITE',
                'location': 'Jakarta Utara',
                'duration_months': 6,
                'slots_available': 2,
                'application_deadline': datetime.now().date() + timedelta(days=18),
                'status': 'OPEN'
            },
        ]

        job_postings = []
        for job_data in job_postings_data:
            job = JobPosting.objects.create(**job_data)
            job_postings.append(job)
            self.stdout.write(f'  Created job: {job.title} at {job.company.name}')

        # Create Students
        self.stdout.write('Creating students...')
        students_data = [
            {'email': 'budi.santoso@student.prasetiyamulya.ac.id', 'name': 'Budi Santoso', 'nim': '20210001', 'program': 'SI', 'angkatan': '2021', 'gender': 'L'},
            {'email': 'siti.nurhaliza@student.prasetiyamulya.ac.id', 'name': 'Siti Nurhaliza', 'nim': '20210002', 'program': 'MN', 'angkatan': '2021', 'gender': 'P'},
            {'email': 'andre.wijaya@student.prasetiyamulya.ac.id', 'name': 'Andre Wijaya', 'nim': '20220003', 'program': 'SI', 'angkatan': '2022', 'gender': 'L'},
            {'email': 'dewi.lestari@student.prasetiyamulya.ac.id', 'name': 'Dewi Lestari', 'nim': '20220004', 'program': 'AK', 'angkatan': '2022', 'gender': 'P'},
            {'email': 'rudi.hartono@student.prasetiyamulya.ac.id', 'name': 'Rudi Hartono', 'nim': '20220005', 'program': 'BS', 'angkatan': '2022', 'gender': 'L'},
            {'email': 'maria.angela@student.prasetiyamulya.ac.id', 'name': 'Maria Angela', 'nim': '20230006', 'program': 'MN', 'angkatan': '2023', 'gender': 'P'},
            {'email': 'ferry.gunawan@student.prasetiyamulya.ac.id', 'name': 'Ferry Gunawan', 'nim': '20230007', 'program': 'SI', 'angkatan': '2023', 'gender': 'L'},
            {'email': 'lisa.kurnia@student.prasetiyamulya.ac.id', 'name': 'Lisa Kurnia', 'nim': '20230008', 'program': 'AK', 'angkatan': '2023', 'gender': 'P'},
            {'email': 'tommy.wijaya@student.prasetiyamulya.ac.id', 'name': 'Tommy Wijaya', 'nim': '20240009', 'program': 'BS', 'angkatan': '2024', 'gender': 'L'},
            {'email': 'nina.sari@student.prasetiyamulya.ac.id', 'name': 'Nina Sari', 'nim': '20240010', 'program': 'MN', 'angkatan': '2024', 'gender': 'P'},
        ]

        students = []
        for i, student_data in enumerate(students_data):
            user = User.objects.create_user(
                email=student_data['email'],
                password='student123',
                role='STUDENT'
            )

            # Create different status scenarios
            if i < 5:
                status = 'ACTIVE'  # First 5 students active (has internship)
                approved_at = timezone.now() - timedelta(days=30)
            else:
                status = 'APPROVED'  # Rest are approved
                approved_at = timezone.now() - timedelta(days=5)

            student = StudentProfile.objects.create(
                user=user,
                full_name=student_data['name'],
                nim=student_data['nim'],
                program=student_data['program'],
                angkatan=student_data['angkatan'],
                gender=student_data['gender'],
                whatsapp=f'0812345678{i:02d}',
                status=status,
                approved_at=approved_at,
                ipk=round(random.uniform(3.0, 4.0), 2),
                skills='Python, Django, SQL, JavaScript' if student_data['program'] == 'SI' else 'Excel, PowerPoint, Data Analysis',
                linkedin_url=f'https://linkedin.com/in/{student_data["name"].lower().replace(" ", "-")}',
            )
            students.append(student)
            self.stdout.write(f'  Created student: {student.full_name} ({student.status})')

        # Create Applications
        self.stdout.write('Creating applications...')
        for i, student in enumerate(students[:5]):  # First 5 students apply
            if student.status in ['APPROVED', 'ACTIVE']:
                job = random.choice(job_postings)
                Application.objects.create(
                    student=student,
                    job_posting=job,
                    cover_letter=f'I am very interested in the {job.title} position...',
                    status=random.choice(['SENT', 'UNDER_REVIEW', 'ACCEPTED']),
                )
                self.stdout.write(f'  Created application for {student.full_name}')

        # Create Supervisors (2-3 supervisors with realistic names)
        self.stdout.write('Creating supervisors...')
        supervisors_data = [
            {
                'full_name': 'Andi Wijaya',
                'email': 'andi.wijaya@tokopedia.com',
                'company': companies[0],  # Tokopedia
                'position': 'Senior Engineering Manager',
                'whatsapp': '081234567801'
            },
            {
                'full_name': 'Sarah Wijaya',
                'email': 'sarah.wijaya@gojek.com',
                'company': companies[2],  # Gojek
                'position': 'Product Manager',
                'whatsapp': '081234567802'
            },
            {
                'full_name': 'Michael Chen',
                'email': 'michael.chen@bca.co.id',
                'company': companies[1],  # BCA
                'position': 'Head of Data Analytics',
                'whatsapp': '081234567803'
            },
        ]

        supervisors = []
        for sup_data in supervisors_data:
            sup_user = User.objects.create_user(
                email=sup_data['email'],
                password='supervisor123',
                role='SUPERVISOR'
            )
            supervisor = SupervisorProfile.objects.create(
                user=sup_user,
                full_name=sup_data['full_name'],
                company_name=sup_data['company'].name,
                position=sup_data['position'],
                whatsapp=sup_data['whatsapp'],
                is_first_login=True,
                credentials_sent_at=timezone.now() - timedelta(days=25)
            )
            supervisors.append(supervisor)
            self.stdout.write(f'  Created supervisor: {supervisor.full_name} at {supervisor.company_name}')

        # Create Internship Placements for ACTIVE students
        self.stdout.write('Creating internship placements...')
        active_students = [s for s in students if s.status == 'ACTIVE']
        placements = []

        for i, student in enumerate(active_students):
            # Distribute students across supervisors (round-robin)
            supervisor = supervisors[i % len(supervisors)]
            company_index = i % len(companies)
            company = companies[company_index]

            placement = InternshipPlacement.objects.create(
                student=student,
                supervisor=supervisor,
                company_name=company.name,
                company_address=company.address,
                company_industry=company.get_industry_display(),
                position=random.choice(['Software Engineer Intern', 'Data Analyst Intern', 'Business Analyst Intern', 'Marketing Intern']),
                start_date=datetime.now().date() - timedelta(days=60),
                end_date=datetime.now().date() + timedelta(days=120),
                supervisor_name=supervisor.full_name,
                supervisor_email=supervisor.user.email,
                supervisor_whatsapp=supervisor.whatsapp,
                supervisor_position=supervisor.position,
                status='ACTIVE',
                confirmed_by=admin_user,
                confirmed_at=timezone.now() - timedelta(days=55)
            )
            placements.append(placement)
            self.stdout.write(f'  Created placement: {student.full_name} -> {supervisor.full_name} at {company.name}')

            # Create Monthly Reports
            report = MonthlyReport.objects.create(
                placement=placement,
                month=1,
                year=datetime.now().year,
                company_profile=f'{company.name} is a leading company in {company.get_industry_display()}. ' * 10,
                job_description='Working on various data analysis tasks and supporting business intelligence team. ' * 10,
                work_environment='Professional and collaborative environment with supportive team members. ' * 10,
                useful_skills='Python programming, SQL queries, and data visualization learned from university. ' * 10,
                needed_skills='Advanced machine learning techniques and cloud computing platforms. ' * 10,
                achievements='Successfully completed data cleaning project and created dashboard. ' * 10,
                challenges='Learning new tools and adapting to fast-paced environment. ' * 10,
                next_month_plan='Focus on advanced analytics and machine learning projects. ' * 10,
                status='REVIEWED',
                submitted_at=timezone.now() - timedelta(days=20),
                reviewed_by=admin_user,
                reviewed_at=timezone.now() - timedelta(days=15)
            )
            self.stdout.write(f'  Created monthly report for {student.full_name}')

        # Create Evaluations (UTS and UAS)
        self.stdout.write('Creating evaluations...')
        for placement in placements:
            # UTS Evaluation (Mid-term, bulan ke-3)
            uts = Evaluation.objects.create(
                placement=placement,
                supervisor=placement.supervisor,
                evaluation_type='UTS',
                period_month=3,
                status='PENDING',
                deadline=datetime.now().date() + timedelta(days=14)
            )
            self.stdout.write(f'  Created UTS evaluation for {placement.student.full_name}')

            # UAS Evaluation (Final, bulan ke-6)
            uas = Evaluation.objects.create(
                placement=placement,
                supervisor=placement.supervisor,
                evaluation_type='UAS',
                period_month=6,
                status='PENDING',
                deadline=datetime.now().date() + timedelta(days=45)
            )
            self.stdout.write(f'  Created UAS evaluation for {placement.student.full_name}')

        self.stdout.write(self.style.SUCCESS('\n=== Data Seeding Completed ==='))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(f'  - 1 Admin user (admin@prasetiyamulya.ac.id / admin123)')
        self.stdout.write(f'  - {len(companies)} Companies')
        self.stdout.write(f'  - {len(job_postings)} Job Postings')
        self.stdout.write(f'  - {len(students)} Students (all with password: student123)')
        self.stdout.write(f'  - {len(supervisors)} Supervisors (all with password: supervisor123)')
        self.stdout.write(f'  - {Application.objects.count()} Applications')
        self.stdout.write(f'  - {InternshipPlacement.objects.count()} Internship Placements')
        self.stdout.write(f'  - {MonthlyReport.objects.count()} Monthly Reports')
        self.stdout.write(f'  - {Evaluation.objects.count()} Evaluations (UTS + UAS)')

        self.stdout.write(self.style.SUCCESS('\n=== Login Credentials ==='))
        self.stdout.write('Admin:')
        self.stdout.write('  Email: admin@prasetiyamulya.ac.id')
        self.stdout.write('  Password: admin123')

        self.stdout.write('\nStudents (all password: student123):')
        self.stdout.write('  - budi.santoso@student.prasetiyamulya.ac.id')
        self.stdout.write('  - siti.nurhaliza@student.prasetiyamulya.ac.id')
        self.stdout.write('  - andre.wijaya@student.prasetiyamulya.ac.id')

        self.stdout.write('\nSupervisors (all password: supervisor123):')
        for supervisor in supervisors:
            student_count = InternshipPlacement.objects.filter(supervisor=supervisor).count()
            self.stdout.write(f'  - {supervisor.user.email} ({supervisor.full_name}) - {student_count} mahasiswa')
