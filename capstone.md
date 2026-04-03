Capstone Project Guidelines

Course Requirement: Full Stack Web Application Development using DJANGO

Project Overview
For this capstone project, students will develop a full-stack web application using the Django framework for the backend. The project must demonstrate the integration of frontend, backend, and database systems to create a fully functional web application.

The goal is to apply the knowledge and skills learned throughout the course to build a practical, useful, and deployable system.

Group Requirements
-	Each group must consist of 3–4 members only.
-	Each member must actively contribute to the development and documentation of the system.

System Requirements

1. Full Stack Implementation
The system must include:
-	Frontend – User interface (HTML, CSS, JavaScript or frontend framework)
-	Backend – Built using Django
-	Database – Connected and used for storing and retrieving system data

All components must be fully integrated and functional. No using of templates.

2. Minimum System Functions
The system must have five (5) or more features and functions
Difference Between Functions and Features

1. Functions  
- Functions are the main operations of the system.
- They are the tasks that allow the system to work and process data.
- If the function is removed, the system cannot operate properly.

Examples of Functions:
-	Create, Update, Delete Records (CRUD)
-	Booking or Reservation Processing
-	Order or Transaction Processing
-	Report Generation
-	User Management (Admin controls users)

2. Features

Features are additional improvements that enhance usability or appearance of the system.
They are not the main operation, but they make the system easier or more pleasant to use.

If a feature is removed, the system will still function.

Examples of Features:
-	Dark Mode
-	Search Bar
-	Email Notifications
-	Profile Picture Upload
-	Dashboard Charts or Graphs
-	Sorting and Filtering Options

System Interaction Requirement

Your system must have active interaction between the user and the system, such as:
-	User input
-	Data processing
-	Database transactions
-	System-generated outputs

Websites that only display content without interaction will NOT be accepted.

Examples of REJECTED projects:
-	Scrolling informational websites
-	Static article or blog pages
-	Purely informational websites without system interaction

Practical and Useful System

Your project must solve a real-world problem or provide a useful service.

Examples of acceptable systems:
-	Inventory Management System
-	Online Appointment Booking System
-	Student Record Management System
-	Event Reservation System
-	Online Ordering System
-	Task Management System

Project Deliverables
1. Working Web Application - A fully functional full-stack web system developed using Django.
2. System Documentation
The documentation must include:

-	Project Title
-	Introduction / Problem Statement
-	System Features and Functions
-	System Architecture
-	Database Design
-	Screenshots of the System
-	User Manual

The document or the Manuscript of the system must be according to the manual.

-	Font Style
o	Microsoft Word standard: Times New Roman

-	Font Size
o	Title (Main Title): 16 pt – Bold, Centered
o	Chapter Titles: 14 pt – Bold
o	Subheadings: 12 pt – Bold
o	Body Text: 12 pt

-	Spacing
o	Line Spacing: 1.5 or Double Spacing 
o	Paragraph Spacing: Before 0 pt, After 6 pt

-	Alignment
o	Body Text: Justified

3. Final Presentation

Each group will present:

-	The problem your system solves
-	The system functions
-	System demonstration (live demo)
-	Technical explanation of frontend, backend, and database integration

❗❗ Important Reminders ❗❗

-	The system must be fully functional, not just a design prototype.
-	The system must include database operations.
-	The system must demonstrate full-stack integration.
-	Projects that are static, purely informational, or lack user interaction will be rejected.

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

[Member 1 Last Name, First Name]
[Member 2 Last Name, First Name] 
[Member 3 Last Name, First Name]
[Member 4 Last Name, First Name]

(all must be alphabetical)






2025 – 2026


Introduction / Problem Statement

**Problem Statement:**
Traditional student record and grading management in educational institutions like Cebu Eastern College (CEC) relies heavily on manual processes using spreadsheets and paper records. This leads to several challenges:

1. **Inefficient Data Management:** Difficulty in updating student information, courses, and grades across multiple documents.
2. **Error-Prone Grading:** Manual calculation of grades (prelim, midterm, semi-final, final) and GWA (General Weighted Average) prone to human errors.
3. **Limited Access:** Students cannot view their grades in real-time; teachers struggle with section management and student enrollment.
4. **Administrative Overhead:** Admins spend excessive time managing teachers, subjects, and sections without centralized control.
5. **Lack of Role-Based Access:** No secure differentiation between student, teacher, and admin functionalities.

**Proposed Solution:**
GRADE PORTAL is a comprehensive full-stack web application built with Django that digitizes student records, grading, and section management. It provides role-based access (Student, Teacher, Admin), real-time grade entry/viewing, automated GWA computation, and secure database transactions, solving real-world educational management problems at CEC.

The system ensures full user interaction through forms, authentication, CRUD operations, and dynamic views, fully integrating frontend (HTML/CSS/JS with Tailwind), backend (Django), and PostgreSQL-compatible database.

System Features and Functions

**Core Functions (6 Essential Operations):**

1. **Student Registration & Authentication (CRUD):** Self-registration with student_no as username, course/year selection, secure login/logout. Database stores student profiles.

2. **Admin User & Subject Management (CRUD):** Admins create/update/delete teachers (with subjects M2M) and subjects (code/title/units/dept). Centralized control.

3. **Teacher Section Creation & Management:** Teachers create sections (subject-specific, semester/SY), add/remove/bulk enroll students via M2M.

4. **Grade Entry & Processing:** Teachers input period grades (prelim/midterm/semi/final), auto-compute remarks (PASSED/FAILED/INC) based on final <=3.0.

5. **Student Grade Viewing & Reporting:** Students view grades by semester/SY, compute GWA with units weighting, standing assessment.

6. **Feedback & Contact System:** Users submit feedback forms stored in DB for admin review.

**Enhancing Features:**
- Semester/School Year filtering
- Bulk student operations
- Custom authentication (no Django templates used)
- Responsive Tailwind UI
- Session-based role security

All functions involve user input → DB processing → outputs, ensuring interaction.

System Architecture

**High-Level Architecture (Django MVT Pattern):**

```
Frontend (Browser)
  ↓ HTTP Requests (HTML Forms, AJAX)
Backend (Django)
  ├── Models (ORM → DB)
  ├── Views (Business Logic, Forms Validation)
  ├── Templates (HTML/CSS/JS - Tailwind)
  └── URLs (Routing)
  ↓ SQL Queries
Database (PostgreSQL/SQLite)
```

**Components:**
- **Frontend:** Custom HTML templates with Tailwind CSS/JS for responsive UI, forms, dynamic tables (no external frameworks beyond Tailwind).
- **Backend:** Django 5.0 with custom User models, session auth, role-based views (decorators/sessions).
- **Database:** Relational DB with 8+ tables, FK/M2M relations for integrity.
- **Integration:** ORM handles CRUD, forms validate input, views process data/transactions.
- **Deployment:** Gunicorn/WhiteNoise ready (requirements.txt).

Text ERD:
```
Student --(grades)--> Grade <--(subject)-- Subject
          ↑
ClassSection --(students M2M)--
          ↑
Teacher --(subjects M2M)--
Admin (auth)
```

Database Design

**Entities & Relationships:**

1. **Student** (PK: id, student_no(unique), name, email, course, year_level) - Custom auth user.
2. **Teacher** (PK: id, teacher_id(unique), name, password, subjects M2M).
3. **Admin** (PK: id, admin_id(unique), password).
4. **Subject** (PK: id, code(unique), title, units, department).
5. **ClassSection** (PK: id, FK teacher/subject, section_name, students M2M) unique_together=[teacher,subject,section_name,sem/SY].
6. **Grade** (PK: id, FK student/subject/section, grades(prelim..final), remarks) unique_together=[student,subject,sem,sy].
7. **Feedback** (name, email, message).
8. **SchoolYear/Semester** (global SY/sem tracking).

**Keys/Constraints:**
- Unique student_no/teacher_id/admin_id.
- Auto remarks on save.
- Cascade deletes protected.

Screenshots of the System

**1. Admin Panel - Dashboard**
![Admin Panel](screenshots/admin_panel.png)

**2. Teacher Dashboard - Sections & Grades**
![Teacher Dashboard](screenshots/teacher.png)

**3. Teacher Section View - Grade Entry**
![Section Grade Entry](screenshots/teacher_section_view.png)

**4. Student Grades - GWA Report**
![Student Grades](screenshots/grades.png)

**5. Student Registration**
![Registration](screenshots/register.png)

**6. Admin Add Teacher**
![Add Teacher](screenshots/admin_add_teacher.png)

User Manual

**1. Student Role:**
- Register: Fill form at /register → login with student_no/password.
- View Grades: Login → /grades (filter semester).
- Profile: /profile → view details.
- Contact: /contact → submit feedback.

**2. Teacher Role:**
- Login: /teacher_login (teacher_id/password).
- Dashboard: View sections/subjects.
- Create Section: /teacher_create_section → select subject/section_name.
- Manage Section: View/add/remove students, enter grades (periods → auto remarks).
- Bulk Add: Checkbox students → save.

**3. Admin Role:**
- Login: Index → admin_id/password.
- Panel: View students/feedback.
- Add Teacher: Form with subjects.
- Manage Subjects: List/add.

**Navigation:** Role-redirected post-login. Logout clears session.
**Running:** python manage.py runserver → localhost:8000

