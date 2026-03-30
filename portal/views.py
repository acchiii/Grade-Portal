from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Grade, Feedback, Teacher, Admin, Subject, ClassSection, SchoolYear, Semester, COURSE_CHOICES, current_school_year
from .forms  import LoginForm, RegisterForm, FeedbackForm, TeacherForm, GradeForm, SubjectForm, ClassSectionForm
from django.db.models import Prefetch
from django.contrib.auth import login, logout
from django.contrib import messages



def get_standing(gwa):
    if gwa is None:    return 'N/A'
    if gwa <= 1.5:     return ' '
    if gwa <= 1.75:    return ' '
    if gwa <= 2.0:     return ' '
    if gwa <= 3.0:     return ' '
    return 'Needs Improvement'

def standing_color(gwa):
    if gwa is None:    return 'var(--text-light)'
    if gwa <= 2.0:     return 'var(--sky)'
    if gwa <= 3.0:     return 'var(--green)'
    return 'var(--red)'



def index(request):
    return render(request, 'portal/index.html', {
        'current':       'index',
        'sy': SchoolYear.objects.first().get_sy() if SchoolYear.objects.exists() else current_school_year(),
        'semester': Semester.objects.first().get_semester() if Semester.objects.exists() else '1st',
        'grading_scale': [],
        
    })

def admin_login(request):
    if request.method == 'GET':
        return redirect('index')
    
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        password   = request.POST.get('password')

        try:
            admin = Admin.objects.get(admin_id=admin_id)
            if admin.check_password(password):
             
             request.session.flush()
             request.session['admin_id'] = admin.admin_id
             return redirect('admin_panel')
            else:
                return render(request, 'portal/index.html', {
                'error_message': 'Wrong Password!' 
            })
        
        except Admin.DoesNotExist:
            request.session['error'] = "Invalid Credentials!"
            return render(request, 'portal/index.html', {
                'error_message': 'Invalid Credentials!'
            })
        
    


def admin_panel(request):

    admin_id = request.session.get('admin_id')
    if not admin_id:
        request.session['error'] = "Something is wrong!"
        return render(request, 'portal/index.html', {
                'error_message': 'Invalid Credentials!'
            })
    
    students  = Student.objects.all().order_by('id')
    feedback  = Feedback.objects.all().order_by('-submitted')
    grades    = Grade.objects.all()

    grade_rows = []
    return render(request, 'portal/admin_panel.html', {
        'current':    'admin',
        'students':   students,
        'feedback':   feedback,
        'grade_rows': grade_rows,
    })


def section_view(request, section_name, subject_code, semester, school_yr):

    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)

    section = get_object_or_404(
        ClassSection.objects.prefetch_related('students'),
        section_name=section_name,
        teacher=teacher,
        subject__code=subject_code,
        semester=semester,
        school_yr=school_yr
    )

    students = section.students.all().prefetch_related(
        Prefetch(
            'grades',
            queryset=Grade.objects.filter(
                section=section,
                subject=section.subject
            ),
            to_attr='section_grades'
        )
    )


    for student in students:
        grades = Grade.objects.filter(
            student=student,
            subject=section.subject,
            semester=section.semester,
            school_yr=section.school_yr
        )
        if grades.exists():
            grade = grades.first()
            if not grade.section_id:
                grade.section = section
                grade.save()
        else:
            grade = Grade.objects.create(
                student=student,
                subject=section.subject,
                section=section,
                semester=section.semester,
                school_yr=section.school_yr
            )

    if request.method == "POST":
        save_count = 0
        error_count = 0
        for student in students:
            try:
                grade = Grade.objects.get(
                    student=student,
                    subject=section.subject,
                    semester=section.semester,
                    school_yr=section.school_yr
                )
                updated = False
                prelim_val = request.POST.get(f'prelim_{student.id}')
                if prelim_val is not None:
                    grade.prelim = float(prelim_val) if prelim_val.strip() else None
                    updated = True
                midterm_val = request.POST.get(f'midterm_{student.id}')
                if midterm_val is not None:
                    grade.midterm = float(midterm_val) if midterm_val.strip() else None
                    updated = True
                semi_val = request.POST.get(f'semi_{student.id}')
                if semi_val is not None:
                    grade.semi = float(semi_val) if semi_val.strip() else None
                    updated = True
                final_val = request.POST.get(f'final_{student.id}')
                if final_val is not None:
                    grade.final = float(final_val) if final_val.strip() else None
                    updated = True

                remarks_val = request.POST.get(f'remarks_{student.id}')
                if remarks_val is not None:
                    grade.remarks = remarks_val if remarks_val.strip() else ''
                    updated = True

                if updated:
                   
                    if not grade.remarks and grade.final is not None:
                        grade.remarks = 'PASSED' if grade.final <= 3.0 else 'FAILED'

                    grade.save()
                    
                    grade.section = section
                    grade.save()
                save_count += 1
            except Exception as e:
                error_count += 1
                messages.error(request, f"Error saving for {student}: {str(e)}")

        if error_count == 0:
            messages.success(request, f"Successfully saved grades for {save_count} students!")
        elif save_count > 0:
            messages.warning(request, f"Saved {save_count} students, {error_count} errors.")
        else:
            messages.error(request, f"Failed to save grades: {error_count} errors.")

        return redirect('section_view', section_name, subject_code, semester, school_yr)

    return render(request, 'portal/teacher_section_view.html', {
    'section': section,
    'students': students,
})

def add_student_to_section(request, section_id):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    section = get_object_or_404(ClassSection, id=section_id, teacher=teacher)

    if request.method == "POST":
        student_id = request.POST.get('student_id')

        student = get_object_or_404(Student, id=student_id)

        # Add student to section
        section.students.add(student)

        # Create grade if not exists
        Grade.objects.get_or_create(
            student=student,
            subject=section.subject,
            section=section,
            semester=section.semester,
            school_yr=section.school_yr
        )

        return redirect('section_view', 
                        section.section_name,
                        section.subject.code,
                        section.semester,
                        section.school_yr)

    # students not yet in section
    students = Student.objects.exclude(id__in=section.students.values_list('id', flat=True))

    return render(request, 'portal/add_student.html', {
        'section': section,
        'students': students
    })
def bulk_add_students(request, section_id):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    section = get_object_or_404(ClassSection, id=section_id, teacher=teacher)

    if request.method == "POST":
        student_ids = request.POST.getlist('students')

        for sid in student_ids:
            student = Student.objects.filter(id=sid).first()
            if not student:
                continue

            # add to M2M safely
            section.students.add(student)

            # ensure grade exists
            Grade.objects.get_or_create(
                student=student,
                subject=section.subject,
                section=section,
                semester=section.semester,
                school_yr=section.school_yr
            )

        return redirect('section_view',
                        section.section_name,
                        section.subject.code,
                        section.semester,
                        section.school_yr)

    # exclude already added students
    students = Student.objects.exclude(
        id__in=section.students.values_list('id', flat=True)
    )

    return render(request, 'portal/bulk_add_students.html', {
        'section': section,
        'students': students
    })
def teacher_view(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login') 
    
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        del request.session['teacher_id']
        return redirect('teacher_login')
    
    subjects = teacher.subjects.all()
    sections = ClassSection.objects.filter(teacher=teacher)

    grades = Grade.objects.filter(
        subject__in=subjects
    ).select_related('student', 'subject')

    subject_grades = {}

    for grade in grades:
        subj_code = getattr(grade.subject, 'code', str(grade.subject.id))

        if subj_code not in subject_grades:
            subject_grades[subj_code] = {
                'subject': grade.subject,
                'grades': []
            }

        subject_grades[subj_code]['grades'].append(grade)
    
    return render(request, 'portal/teacher.html', {
        'teacher': teacher,
        'sections': sections,
        'subjects': subjects,
        'subject_grades': subject_grades,
    })



def teacher_login(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        password = request.POST.get('password')
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
            if teacher.check_password(password):
                # request.session.flush() 
                request.session['teacher_id'] = teacher.id
                return redirect('teacher')
            else:
                error_message = 'Invalid credentials'
        except Teacher.DoesNotExist:
            error_message = 'Teacher not found'
            
    return render(request, 'portal/teacher_login.html', {
        'error_message': error_message if 'error_message' in locals() else None
    })

def admin_add_teacher(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.set_password(form.cleaned_data['password'])
            teacher.save()
            form.save_m2m()  # Save many-to-many relationships (subjects)
            return redirect('admin_panel')
    else:
        form = TeacherForm()
    
    return render(request, 'portal/admin_add_teacher.html', {'form': form})

def admin_subjects(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    
    subjects = Subject.objects.all()
    return render(request, 'portal/admin_subjects.html', {'subjects': subjects})

def admin_teachers(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    
    course_filter = request.GET.get('course', '')
    teachers = Teacher.objects.all()
    
    if course_filter:
        teachers = teachers.filter(department__icontains=course_filter)
    
    return render(request, 'portal/admin_teachers.html', {
        'teachers': teachers,
        'course_filter': course_filter,
        'course_choices': COURSE_CHOICES
    })

def admin_add_subject(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('index')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_subjects')
    else:
        form = SubjectForm()
    
    return render(request, 'portal/admin_add_subject.html', {'form': form})

def teacher_add_grade(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
    
    teacher = Teacher.objects.get(id=teacher_id)
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        form.fields['subject'].queryset = teacher.subjects.all()  # Restrict to teacher's subjects
        if form.is_valid():
            grade = form.save()
            return redirect('teacher')
    else:
        form = GradeForm()
        form.fields['subject'].queryset = teacher.subjects.all()
    
    return render(request, 'portal/teacher_add_grade.html', {'form': form, 'teacher': teacher})

def teacher_create_section(request):
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
    
    teacher = Teacher.objects.get(id=teacher_id)
    
    if request.method == 'POST':
        form = ClassSectionForm(request.POST)
        form.fields['subject'].queryset = teacher.subjects.all()  # Only subjects teacher teaches
        if form.is_valid():
            section = form.save(commit=False)
            section.teacher = teacher
            section.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('teacher')
    else:
        form = ClassSectionForm()
        form.fields['subject'].queryset = teacher.subjects.all()
    
    return render(request, 'portal/teacher_create_section.html', {'form': form, 'teacher': teacher})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('grades')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.cleaned_data['user'])
        return redirect('grades')
    return render(request, 'portal/login.html', {'form': form, 'current': 'login'})


def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('grades')
    form = RegisterForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        form.save()
        success = True
        form = RegisterForm()   # reset
    return render(request, 'portal/register.html', {
        'form': form, 'success': success, 'current': 'register'
    })


@login_required
def grades_view(request):
    student = request.user
    semester_filter = request.GET.get('semester', '')
    
    base_query = Grade.objects.filter(student=student).select_related('subject')
    
    if semester_filter:
        base_query = base_query.filter(semester=semester_filter)
    
    rows = base_query.order_by('-school_yr', 'semester', 'subject__code')

    # Group by semester only (separate 1st/2nd sem different years)
    semester_groups = {}
    for r in rows:
        key = r.semester
        if key not in semester_groups:
            semester_groups[key] = []
        semester_groups[key].append(r)
    
    # Prepare grade_rows per semester
    all_grade_rows = []
    total_units, weighted_sum = 0, 0.0
    for semester, semester_rows in semester_groups.items():
        semester_grade_rows = []
        semester_units = 0
        semester_weighted = 0.0
        for r in semester_rows:
            rem = r.remarks or ''
            if rem == 'PASSED':   pill, gcls = 'pill-pass', 'grade-pass'
            elif rem == 'FAILED': pill, gcls = 'pill-fail', 'grade-fail'
            elif rem == 'INC':    pill, gcls = 'pill-inc',  'grade-inc'
            else:                 pill, gcls = '',           ''
            row_data = {'grade': r, 'pill': pill, 'gcls': gcls, 'rem': rem or 'PENDING'}
            semester_grade_rows.append(row_data)
            if r.final is not None and r.remarks == 'PASSED':
                semester_units += r.subject.units
                semester_weighted += r.final * r.subject.units
                total_units += r.subject.units
                weighted_sum += r.final * r.subject.units
        all_grade_rows.append({
            'semester': semester,
            'rows': semester_grade_rows,
            'gwa': round(semester_weighted / semester_units, 2) if semester_units > 0 else None
        })
    
    gwa = round(weighted_sum / total_units, 2) if total_units > 0 else None

    semesters = sorted(set(Grade.objects.filter(student=student).values_list('semester', flat=True)))

    return render(request, 'portal/grades.html', {
        'current':     'grades',
        'student':     student,
        'grade_rows':  all_grade_rows,
        'row_count':   sum(len(group['rows']) for group in all_grade_rows),
        'total_units': total_units,
        'gwa':         gwa,
        'gwa_fmt':     f'{gwa:.2f}' if gwa else '—',
        'standing':    get_standing(gwa),
        'stand_color': standing_color(gwa),
        'semesters':   semesters,
        'semester_filter': semester_filter,
    })



def profile_view(request, pk):
    if not request.user.is_authenticated :
        return redirect('login')
    if not request.user.is_staff and request.user.pk != pk:
        return redirect('profile', pk=request.user.pk)

    profile = get_object_or_404(Student, pk=pk)
    is_own  = (request.user.pk == pk)
    fields  = [
        ('Student No.',     profile.student_no),
        ('Full Name',       f'{profile.last_name}, {profile.first_name}'),
        ('Email',           profile.email),
        ('Course',          profile.course),
        ('Year Level',      profile.year_suffix + ' Year'),
        ('Date Registered', profile.created_at.strftime('%Y-%m-%d %H:%M')),
    ]
    return render(request, 'portal/profile.html', {

        'current': 'profile',
        'profile': profile,
        'is_own':  is_own,
        'fields':  fields,
    })


def contact_view(request):
    form = FeedbackForm(request.POST or None)
    success = False
    if request.method == 'POST' and form.is_valid():
        form.save()
        success = True
        form = FeedbackForm()   # reset
    return render(request, 'portal/contact.html', {
        'form': form, 'success': success, 'current': 'contact'
    })


def error404(request, exception=None):
    return render(request, 'portal/404.html', {
        'error': str(exception),
    })

def error500(request):
    return render(request, 'portal/500.html')





