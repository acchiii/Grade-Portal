
GRADE PORTAL
Student Record & Grading Management System


A Capstone Project Documentation
Presented to
College of Information Technology
CEBU EASTERN COLLEGE INCORPORATED




Submitted in Fulfillment of the Requirements for the Course
INTEGRATIVE PROGRAMMING AND TECHNOLOGIES




Submitted to:
Gladymay S. Sadorra






Members:


(all must be alphabetical)






2025 – 2026


Introduction / Problem Statement

Problem Statement:
Traditional student record and grading management in educational institutions like Cebu Eastern College (CEC) relies heavily on manual processes using spreadsheets and paper records. This leads to several challenges:

1. Inefficient Data Management: Difficulty in updating student information, courses, and grades across multiple documents.
2. ErrorProne Grading: Manual calculation of grades (prelim, midterm, semifinal, final) and GWA (General Weighted Average) prone to human errors.
3. Limited Access: Students cannot view their grades in realtime; teachers struggle with section management and student enrollment.
4. Administrative Overhead: Admins spend excessive time managing teachers, subjects, and sections without centralized control.
5. Lack of RoleBased Access: No secure differentiation between student, teacher, and admin functionalities.

Proposed Solution:
GRADE PORTAL is a comprehensive fullstack web application built with Django that digitizes student records, grading, and section management. It provides rolebased access (Student, Teacher, Admin), realtime grade entry/viewing, automated GWA computation, and secure database transactions, solving realworld educational management problems at CEC.

The system ensures full user interaction through forms, authentication, CRUD operations, and dynamic views, fully integrating frontend (HTML/CSS/JS with Tailwind), backend (Django), and PostgreSQLcompatible database.

System Features and Functions

Core Functions (6 Essential Operations):

1. Student Registration & Authentication (CRUD): Selfregistration with student_no as username, course/year selection, secure login/logout. Database stores student profiles.

2. Admin User & Subject Management (CRUD): Admins create/update/delete teachers (with subjects M2M) and subjects (code/title/units/dept). Centralized control.

3. Teacher Section Creation & Management: Teachers create sections (subjectspecific, semester/SY), add/remove/bulk enroll students via M2M.

4. Grade Entry & Processing: Teachers input period grades (prelim/midterm/semi/final), autocompute remarks (PASSED/FAILED/INC) based on final <=3.0.

5. Student Grade Viewing & Reporting: Students view grades by semester/SY, compute GWA with units weighting, standing assessment.

6. Feedback & Contact System: Users submit feedback forms stored in DB for admin review.

Enhancing Features:
 Semester/School Year filtering
 Bulk student operations
 Custom authentication (no Django templates used)
 Responsive Tailwind UI
 Sessionbased role security

All functions involve user input → DB processing → outputs, ensuring interaction.

System Architecture

HighLevel Architecture (Django MVT Pattern):


Frontend (Browser)
  ↓ HTTP Requests (HTML Forms, AJAX)
Backend (Django)
  ├── Models (ORM → DB)
  ├── Views (Business Logic, Forms Validation)
  ├── Templates (HTML/CSS/JS  Tailwind)
  └── URLs (Routing)
  ↓ SQL Queries
Database (PostgreSQL/SQLite)


Components:
 Frontend: Custom HTML templates with Tailwind CSS/JS for responsive UI, forms, dynamic tables (no external frameworks beyond Tailwind).
 Backend: Django 5.0 with custom User models, session auth, rolebased views (decorators/sessions).
 Database: Relational DB with 8+ tables, FK/M2M relations for integrity.
 Integration: ORM handles CRUD, forms validate input, views process data/transactions.
 Deployment: Gunicorn/WhiteNoise ready (requirements.txt).

Text ERD:

Student (grades)> Grade <(subject) Subject
          ↑
ClassSection (students M2M)
          ↑
Teacher (subjects M2M)
Admin (auth)


Database Design

Entities & Relationships:

1. Student (PK: id, student_no(unique), name, email, course, year_level)  Custom auth user.
2. Teacher (PK: id, teacher_id(unique), name, password, subjects M2M).
3. Admin (PK: id, admin_id(unique), password).
4. Subject (PK: id, code(unique), title, units, department).
5. ClassSection (PK: id, FK teacher/subject, section_name, students M2M) unique_together=[teacher,subject,section_name,sem/SY].
6. Grade (PK: id, FK student/subject/section, grades(prelim..final), remarks) unique_together=[student,subject,sem,sy].
7. Feedback (name, email, message).
8. SchoolYear/Semester (global SY/sem tracking).

Keys/Constraints:
 Unique student_no/teacher_id/admin_id.
 Auto remarks on save.
 Cascade deletes protected.

Screenshots of the System

1. Admin Panel  Dashboard
![Admin Panel](screenshots/admin_panel.png)

2. Teacher Dashboard  Sections & Grades
![Teacher Dashboard](screenshots/teacher.png)

3. Teacher Section View  Grade Entry
![Section Grade Entry](screenshots/teacher_section_view.png)

4. Student Grades  GWA Report
![Student Grades](screenshots/grades.png)

5. Student Registration
![Registration](screenshots/register.png)

6. Admin Add Teacher
![Add Teacher](screenshots/admin_add_teacher.png)

User Manual

1. Student Role:
 Register: Fill form at /register → login with student_no/password.
 View Grades: Login → /grades (filter semester).
 Profile: /profile → view details.
 Contact: /contact → submit feedback.

2. Teacher Role:
 Login: /teacher_login (teacher_id/password).
 Dashboard: View sections/subjects.
 Create Section: /teacher_create_section → select subject/section_name.
 Manage Section: View/add/remove students, enter grades (periods → auto remarks).
 Bulk Add: Checkbox students → save.

3. Admin Role:
 Login: Index → admin_id/password.
 Panel: View students/feedback.
 Add Teacher: Form with subjects.
 Manage Subjects: List/add.



