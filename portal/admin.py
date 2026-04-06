from django.contrib import admin
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Student, Subject, Grade, Feedback


class StudentCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(),
                                help_text='Leave blank for inactive student (admin-added)')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(),
                                help_text='Leave blank for inactive student')

    class Meta:
        model  = Student
        fields = ('student_no', 'first_name', 'last_name', 'course', 'year_level')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        student = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            student.set_password(password1)
        else:
            student.is_active = False  # Inactive if no password
        if commit:
            student.save()
        return student


class StudentChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model  = Student
        fields = ('student_no', 'first_name', 'last_name', 'email', 'course', 'year_level')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form           = StudentChangeForm
    add_form       = StudentCreationForm
    list_display   = ('student_no', 'last_name', 'first_name', 'email', 'course', 'year_level')
    search_fields  = ('student_no', 'last_name', 'first_name', 'email')
    list_filter    = ('course', 'year_level', 'is_staff')
    ordering       = ('student_no',)
    fieldsets = (
        (None,            {'fields': ('student_no', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'course', 'year_level')}),
        ('Permissions',   {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': (
            'student_no', 'first_name', 'last_name', 'email',
            'course', 'year_level', 'password1', 'password2',
        )}),
    )

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ('code', 'title', 'units')
    search_fields = ('code', 'title')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ('student', 'subject', 'semester', 'school_yr',
                     'prelim', 'midterm', 'semi','final', 'remarks')
    list_filter   = ('semester', 'school_yr', 'remarks')
    search_fields = ('student__student_no', 'student__last_name', 'subject__code')
    raw_id_fields = ('student', 'subject')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display    = ('name', 'email', 'subject', 'submitted')
    readonly_fields = ('submitted',)