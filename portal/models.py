from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

def current_school_year():
    year = datetime.now().year
    return f"{year} - {year+1}"

class Semester(models.Model):
    semester = models.CharField(max_length=10, choices=[('1st', '1st Semester'), ('2nd', '2nd Semester')], default='1st')
    
    def update_semester(self, new_semester):
        self.semester = new_semester
        self.save()
        
    def get_semester(self):
        return self.semester

class SchoolYear(models.Model):
    sy = models.CharField(max_length=20, default=current_school_year, unique=True)
    
    def update_sy(self, new_sy):
        self.sy = new_sy
        self.save()
    
    def get_sy(self):
        return self.sy  
    
    def __str__(self):
        return self.sy

class StudentManager(BaseUserManager):
    def create_user(self, student_no, password=None, **extra_fields):
        if not student_no:
            raise ValueError('Student number is required')
        user = self.model(student_no=student_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(student_no, password, **extra_fields)


COURSE_CHOICES = [
    ('BSIT',   'BS Information Technology'),
    ('BSHM',   'BS Hospitality Management'),
    ('BEED',   'BS Education (Elementary)'),
    ('BSED',   'BS Education'),
    ('BSTM',   'BS Tourism Management'),
    ('BSCRIM', 'BS Criminology'),
]
DEPT_CHOICES = [
    ('IT', 'Information Technology'),
    ('BEED', 'Bachelor of Elementary Education (BEED)'),
    ('BSED', 'Bachelor of Secondary Education (BSED)'),
    ('HTM', 'Hospitality/Tourism'),
    ('GE', 'General Education'),
    ('CRIM', 'Criminology'),
]
  

YEAR_CHOICES = [(i, f'{i}{"st" if i==1 else "nd" if i==2 else "rd" if i==3 else "th"} Year') for i in range(1, 5)]


class Student(AbstractBaseUser):
    student_no  = models.CharField(max_length=20, unique=True)
    last_name   = models.CharField(max_length=100)
    first_name  = models.CharField(max_length=100)
    email       = models.EmailField(unique=True)
    course      = models.CharField(max_length=10, choices=COURSE_CHOICES, default='BSIT')
    year_level  = models.IntegerField(choices=YEAR_CHOICES, default=1)
    created_at  = models.DateTimeField(auto_now_add=True)

    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'student_no'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = StudentManager()

    def __str__(self):
        return f'{self.last_name}, {self.first_name} ({self.student_no})'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def year_suffix(self):
        y = self.year_level
        return f'{y}{"st" if y==1 else "nd" if y==2 else "rd" if y==3 else "th"}'


class Subject(models.Model):
    code       = models.CharField(max_length=20, unique=True)
    title      = models.CharField(max_length=200)
    units      = models.IntegerField(default=3)
    department = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.code} — {self.title}'


SEMESTER_CHOICES = [('1st', '1st Semester'), ('2nd', '2nd Semester'), ('Summer', 'Summer')]
REMARKS_CHOICES  = [('PASSED', 'Passed'), ('FAILED', 'Failed'), ('INC', 'Incomplete'), ('', 'Pending')]


class Grade(models.Model):
    student   = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject   = models.ForeignKey(Subject, on_delete=models.CASCADE)
    section   = models.ForeignKey('ClassSection', on_delete=models.CASCADE)

    semester  = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1st')
    defsy = current_school_year()
    school_yr = models.CharField(max_length=20, default=defsy)
    

    prelim  = models.FloatField(null=True, blank=True)
    midterm = models.FloatField(null=True, blank=True)
    semi    = models.FloatField(null=True, blank=True)
    final   = models.FloatField(null=True, blank=True)

    remarks = models.CharField(max_length=10, choices=REMARKS_CHOICES, blank=True, default='')

    class Meta:
        ordering = ['-school_yr', 'semester', 'subject__code']
        unique_together = ['student', 'subject', 'semester', 'school_yr']

    def __str__(self):
        return f'{self.student.student_no} — {self.subject.code}: {self.final}'

class Feedback(models.Model):
    name      = models.CharField(max_length=200)
    email     = models.EmailField(blank=True)
    subject   = models.CharField(max_length=200, blank=True)
    message   = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.name} ({self.submitted:%Y-%m-%d})'
    

class Teacher(models.Model):
    name       = models.CharField(max_length=200)
    teacher_id = models.CharField(max_length=20, unique=True, default="")
    email      = models.EmailField(blank=True)
    password   = models.CharField(max_length=128)
    department = models.CharField(max_length=100, blank=True)
    subjects   = models.ManyToManyField(Subject, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):

        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
    

class Admin(models.Model):
    admin_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class ClassSection(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    section_name = models.CharField(max_length=50)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1st')
    school_yr = models.CharField(max_length=20, default=SchoolYear.get_sy())
    students = models.ManyToManyField(Student, blank=True)
   
    class Meta:
        unique_together = ['teacher', 'subject', 'section_name', 'semester', 'school_yr']

    def __str__(self):
        return f'{self.subject.code} - {self.section_name} ({self.teacher.name})'
    
