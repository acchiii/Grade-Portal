
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('grades/', views.grades_view, name='grades'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('teacher/', views.teacher_view, name='teacher'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('teacher/add-grade/', views.teacher_add_grade, name='teacher_add_grade'),
    path('teacher/create-section/', views.teacher_create_section, name='teacher_create_section'),
    # path('teacher/<str:section_name>/', views.section_view, name='section_view'),
    # path('teacher/<int:pk>/', views.section_view, name='teacher_section_view'),
    path('section/<int:section_id>/bulk-add-students/', views.bulk_add_students, name='bulk_add_students'),
    path('section/<int:section_id>/add-student/', views.add_student_to_section, name='add_student_to_section'),
    path('section/<str:section_name>/<str:subject_code>/<str:semester>/<str:school_yr>/', views.section_view,name='section_view'),
    path('ADMIN/add-teacher/', views.admin_add_teacher, name='admin_add_teacher'),
    path('ADMIN/teachers/', views.admin_teachers, name='admin_teachers'),
    path('ADMIN/subjects/', views.admin_subjects, name='admin_subjects'),
    path('ADMIN/add-subject/', views.admin_add_subject, name='admin_add_subject'),
    path('contact/', views.contact_view, name='contact'),
    path('portal-admin/', views.admin_login, name='admin_login'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]