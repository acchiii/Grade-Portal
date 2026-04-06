from django import forms
from django.contrib.auth import authenticate
from .models import Student, Feedback, COURSE_CHOICES, DEPT_CHOICES, Teacher, Subject, Grade, ClassSection


class LoginForm(forms.Form):
    student_no = forms.CharField(label='Student Number', max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'e.g. 2312100'}))
    password   = forms.CharField(label='Password',
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Enter your portal password'}))

    def clean(self):
        data = super().clean()
        sno  = data.get('student_no')
        pwd  = data.get('password')
        if sno and pwd:
            user = authenticate(username=sno, password=pwd)
            if user is None:
                raise forms.ValidationError('Incorrect Student Number or Password. Please try again.')
            data['user'] = user
        return data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Portal Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'}))

    class Meta:
        model  = Student
        fields = ['last_name', 'first_name', 'student_no', 'email', 'course', 'year_level']
        widgets = {
            'last_name':  forms.TextInput(attrs={'placeholder': 'Enter here...'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter here...'}),
            'student_no': forms.TextInput(attrs={'placeholder': 'e.g 2312100'}),
            'email':      forms.TextInput(attrs={'placeholder': 'e.g rojen@gmail.com'}),
            'course':     forms.Select(),
            'year_level': forms.Select(),
        }
        labels = {
            'last_name':  'Last Name',
            'first_name': 'First Name',
            'student_no': 'Student Number',
            'email':      'Email',
            'course':     'Course / Program',
            'year_level': 'Year Level',
        }

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data['password'])
        if commit:
            student.save()
        return student


class AdminStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure required attrs
        self.fields['student_no'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['course'].widget.attrs['required'] = True
        self.fields['year_level'].widget.attrs['required'] = True

    class Meta:
        model = Student
        fields = ['student_no', 'last_name', 'first_name', 'course', 'year_level']
        widgets = {
            'student_no': forms.TextInput(attrs={
                'placeholder': 'e.g. 2312100',
                'required': 'required',
                'autocomplete': 'off'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter last name',
                'required': 'required'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter first name', 
                'required': 'required'
            }),
            'course': forms.Select(attrs={'required': 'required'}),
            'year_level': forms.Select(attrs={'required': 'required'}),
        }
        labels = {
            'student_no': 'Student Number',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'course': 'Course',
            'year_level': 'Year Level',
        }
        error_messages = {
            'student_no': {
                'required': 'Student number is required.',
            },
            'last_name': {
                'required': 'Last name is required.',
            },
            'first_name': {
                'required': 'First name is required.',
            },
        }

    def clean_student_no(self):
        value = self.cleaned_data.get('student_no', '').strip()
        if not value:
            raise forms.ValidationError('Student number is required.')
        return value

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        if not value:
            raise forms.ValidationError('Last name is required.')
        return value

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        if not value:
            raise forms.ValidationError('First name is required.')
        return value


class StudentRegisterForm(forms.Form):
    student_no = forms.CharField(label='Student Number', max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter your student ID e.g. 2312100'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Create your portal password'}))

    def clean_student_no(self):
        student_no = self.cleaned_data['student_no']
        if Student.objects.filter(student_no=student_no, is_active=True).exists():
            raise forms.ValidationError('This student ID is already registered and active.')
        return student_no


class FeedbackForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('', '— Select a topic —'),
        ('Grade Inquiry',         'Grade Inquiry'),
        ('Transcript Request',    'Transcript Request'),
        ('Enrollment Concern',    'Enrollment Concern'),
        ('Portal Technical Issue','Portal Technical Issue'),
        ('Other',                 'Other'),
    ]
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, required=False,
                                label='Subject / Concern')

    class Meta:
        model  = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name':    forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email':   forms.TextInput(attrs={'placeholder': 'your@email.com'}),
            'message': forms.Textarea(attrs={'placeholder': 'Describe your concern in detail...'}),
        }
        labels = {
            'name':    'Full Name',
            'email':   'Email Address',
            'message': 'Message',
        }


class SubjectForm(forms.ModelForm):
 
  department = forms.ChoiceField(label='Course / Department', choices=DEPT_CHOICES, required=False)
  class Meta:
        model = Subject
        fields = ['code', 'title', 'units', 'department']



class TeacherForm(forms.ModelForm):
    course = forms.ChoiceField(label='', choices=DEPT_CHOICES, required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = Teacher
        fields = ['name', 'teacher_id', 'email', 'subjects', 'department',]
        widgets = {
                'subjects': forms.SelectMultiple(attrs={'size': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set department based on course selection via JavaScript
        self.fields['department'].widget.attrs['readonly'] = True
        self.fields['department'].widget.attrs['hidden'] = True
        # self.fields['department'].help_text = ''
        # 'Department will be set automatically based on course selection'
        self.fields['teacher_id'].help_text = 'Unique identifier for the teacher (e.g., T001)'

    def clean_teacher_id(self):
        teacher_id = self.cleaned_data.get('teacher_id')
        if not teacher_id:
            raise forms.ValidationError('Teacher ID is required.')
        return teacher_id

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        if course:
            # Map course to department
            department_mapping = {
                'BSIT': 'College of Computer Studies',
                'BSHM': 'College of Hospitality Management',
                'BEED': 'College of Education',
                'BSED': 'College of Education',
                'BSTM': 'College of Tourism Management',
                'BSCRIM': 'College of Criminal Justice',
            }
            cleaned_data['department'] = department_mapping.get(course, '')
        return cleaned_data


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'semester', 'school_yr', 'prelim', 'midterm', 'semi','final', 'remarks']
        widgets = {
            'student': forms.Select(),
            'subject': forms.Select(),
            'semester': forms.Select(),
            'school_yr': forms.TextInput(attrs={'placeholder': 'e.g. 2026-2027'}),
            'prelim': forms.NumberInput(attrs={'step': '0.01'}),
            'midterm': forms.NumberInput(attrs={'step': '0.01'}),
            'semi': forms.NumberInput(attrs={'step': '0.01'}),
            'final': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ClassSectionForm(forms.ModelForm):
    class Meta:
        model = ClassSection
        fields = ['subject', 'section_name', 'semester', 'school_yr', 'students'] #students ang last
        widgets = {
            'subject': forms.Select(),
            'section_name': forms.TextInput(attrs={'placeholder': 'e.g. A, B, 1, 2'}),
            'semester': forms.Select(),
            'school_yr': forms.TextInput(attrs={'placeholder': 'e.g. 2026-2027'}),
            'students': forms.TextInput(attrs={'placeholder': 'Select Manually Later', 'disabled':''}),
        }
