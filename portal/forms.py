from django import forms
from .models import *

class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput, label='Student Number', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput, label='Password' )

class RegisterForm(forms.Form):
    pass

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Teacher
        fields = ['name', 'teacher_id', 'email', 'department', 'password', 'subjects']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'prelim', 'midterm', 'semi', 'final', 'remarks']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'title', 'units', 'department']

class ClassSectionForm(forms.ModelForm):
    class Meta:
        model = ClassSection
        fields = ['section_name', 'subject', 'semester', 'school_yr']
        widgets = {
            'semester': forms.Select(choices=SEMESTER_CHOICES),
        }

class AdminStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_no', 'last_name', 'first_name', 'course', 'year_level']

class StudentRegisterForm(forms.Form):
    student_no = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class BulkStudentImportForm(forms.Form):
    json_file = forms.FileField(label='JSON Students File')
