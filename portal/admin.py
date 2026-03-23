from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Student, Subject, Grade, Feedback


class StudentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model  = Student
        fields = ('student_no', 'first_name', 'last_name', 'email', 'course', 'year_level')


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