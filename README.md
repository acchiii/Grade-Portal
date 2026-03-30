# Capstone Project Guidelines

**Course Requirement: Full Stack Web Application Development using DJANGO**

## Project Overview
For this capstone project, students will develop a full-stack web application using the Django framework for the backend. The project must demonstrate the integration of frontend, backend, and database systems to create a fully functional web application.

The goal is to apply the knowledge and skills learned throughout the course to build a practical, useful, and deployable system.

## Group Requirements
- Each group must consist of 3–4 members only.
- Each member must actively contribute to the development and documentation of the system.

## System Requirements

### 1. Full Stack Implementation
The system must include:
- **Frontend** – User interface (HTML, CSS, JavaScript)
- **Backend** – Built using Django
- **Database** – Connected and used for storing and retrieving system data

All components must be fully integrated and functional. No using of templates.

### 2. Minimum System Functions
The system must have **five (5) or more features and functions**

#### Difference Between Functions and Features

**1. Functions**  
- Functions are the main operations of the system.
- They are the tasks that allow the system to work and process data.
- If the function is removed, the system cannot operate properly.

**Examples of Functions**:
- Create, Update, Delete Records (CRUD)
- Booking or Reservation Processing
- Order or Transaction Processing
- Report Generation
- User Management (Admin controls users)

**2. Features**
- Features are additional improvements that enhance usability or appearance of the system.
- They are not the main operation, but they make the system easier or more pleasant to use.
- If a feature is removed, the system will still function.

**Examples of Features**:
- Dark Mode
- Search Bar
- Email Notifications
- Profile Picture Upload
- Dashboard Charts or Graphs
- Sorting and Filtering Options

## System Interaction Requirement
Your system must have **active interaction** between the user and the system, such as:
- User input
- Data processing
- Database transactions
- System-generated outputs

Websites that only display content **without interaction will NOT be accepted**.

**Examples of REJECTED projects**:
- Scrolling informational websites
- Static article or blog pages
- Purely informational websites without system interaction

## Practical and Useful System
Your project must solve a **real-world problem** or provide a **useful service**.

**Examples of acceptable systems**:
- Inventory Management System
- Online Appointment Booking System
- **Student Record Management System**
- Event Reservation System
- Online Ordering System
- Task Management System

## Project Deliverables
1. **Working Web Application** - A fully functional full-stack web system developed using Django.
2. **System Documentation** - See formatting below.
3. **Final Presentation** - Live demo + technical explanation.

### Document Formatting
- **Font Style**: Times New Roman
- **Font Size**: Title 16pt Bold Centered, Chapters 14pt Bold, Subheadings 12pt Bold, Body 12pt
- **Spacing**: 1.5 or Double, Paragraph After 6pt
- **Alignment**: Justified

**❗❗ Important Reminders ❗❗**
- The system must be **fully functional**, not just a design prototype.
- The system must include **database operations**.
- The system must demonstrate **full-stack integration**.
- Projects that are static, purely informational, or lack user interaction will be **rejected**.

---

# GRADE PORTAL

**A Capstone Project Documentation**  
**Presented to**  
**College of Information Technology**  
**CEBU EASTERN COLLEGE INCORPORATED**

**Submitted in Fulfillment of the Requirements for the Course**  
**INTEGRATIVE PROGRAMMING AND TECHNOLOGIES**

**Submitted to:**  
**Gladymay S. Sadorra**

**Members:**

**Belarmino, Archie Q.**  
**Bilonoac, Rythner**  
**Dela Cruz, Rojen**  
**Noynay, Edison**  

**2025 – 2026**

## Introduction / Problem Statement

Traditional manual grade management in educational institutions faces several challenges:

1. **Time-Consuming Processes**: Teachers spend excessive time computing grades, calculating GWA, and updating records.
2. **Error-Prone Calculations**: Manual arithmetic leads to mistakes in averages and final remarks.
3. **Data Accessibility**: Students cannot easily view their grades; admins struggle with oversight.
4. **Scalability Issues**: Hard to manage large classes/sections across semesters/school years.
5. **Lack of Integration**: Separate systems for students/teachers/admins cause inconsistencies.

**GRADE PORTAL** solves these by providing a **full-stack Django web application** for:
- Students to register/view grades/GWA/standing.
- Teachers to manage classes/sections/students/grades.
- Admins to oversee users/subjects/teachers.

This **practical Student Record Management System** ensures real-time interaction, database transactions, and automated computations.

## System Features and Functions

### Core Functions (Essential Operations)
1. **User Authentication & Management** (CRUD): Student register/login, Teacher login (custom), Admin login/control.
2. **Teacher Class/Section Management** (CRUD): Create sections, bulk/single add students.
3. **Grade Processing** (CRUD): Input prelim/midterm/semi/final grades per student/section; auto-compute remarks (PASSED/FAILED/INC).
4. **Student Grade Viewing & Reporting**: View grades by semester, compute GWA, academic standing.
5. **Admin Management** (CRUD): Add teachers/subjects, view panels/feedback.
6. **School Year/Semester Management**: Dynamic current SY/Semester tracking.

### Enhancing Features
- Bulk student enrollment to sections.
- Semester filtering on grades.
- Auto GWA/standing calculation/color-coding.
- Contact feedback form.
- Responsive UI with dashboards.

## System Architecture

**Django MVT (Model-View-Template) Pattern**:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │◄──►│    Backend       │◄──►│   Database      │
│ (HTML/CSS/JS)   │    │ (Django Views)   │    │ (SQLite)        │
│ Templates:      │    │ URLs/Forms/Auth  │    │ Models: Student │
│ - base.html     │    │ Sessions         │    │ Teacher/Admin/  │
│ - grades.html   │    │                  │    │ Grade/Subject/  │
│ - teacher.html  │    └──────────────────┘    │ ClassSection    │
│ etc.            │                             └─────────────────┘
└─────────────────┘
```

- **Frontend**: Custom responsive templates (no frameworks).
- **Backend**: Custom views (17+), forms, signals; session-based auth.
- **Database**: Full integration with migrations/transactions.
- **Flow**: User input → View processing → Model/DB ops → Render template.

## Database Design

**Key Entities & Relations**:

| Model | Key Fields | Relations |
|-------|------------|-----------|
| **Student** | student_no (PK), name, email, course, year_level | Grades (1:M) |
| **Teacher** | teacher_id, name, email, subjects (M:M) | ClassSection (1:M) |
| **Admin** | admin_id, password | N/A |
| **Subject** | code (unique), title, units, dept | Grade (1:M), Teacher M:M |
| **ClassSection** | section_name, semester, school_yr | Teacher (M), Subject (M), Students (M:M), Grade (1:M) |
| **Grade** | prelim/midterm/semi/final, remarks, semester/yr | Student (M), Subject (M), ClassSection (M) |
| **SchoolYear/Semester** | sy/semester | Referenced in Grade/ClassSection |

**Unique Constraints**: No duplicate grades per student/subject/sem/yr. Migrations ensure integrity.

## Screenshots of the System
*(User to add images manually to `/screenshots/` folder)*

1. ![Login Page](screenshots/login.png)
2. ![Student Grades](screenshots/grades.png)
3. ![Teacher Dashboard](screenshots/teacher.png)
4. ![Admin Panel](screenshots/admin_panel.png)
5. ![Grade Entry](screenshots/section_view.png)
6. ![Section Management](screenshots/create_section.png)

## User Manual

### 1. Student
1. Register/Login at `/register` or `/login`.
2. View grades/GWA at `/grades/` (filter semester).
3. Profile at `/profile/`.
4. Contact feedback.

### 2. Teacher
1. Login at `/teacher-login/`.
2. Dashboard `/teacher/` – view sections/grades.
3. Create section `/teacher/create-section/`.
4. Add students (single/bulk).
5. Edit grades in section view.

### 3. Admin
1. Login at `/portal-admin/`.
2. Panel `/admin-panel/` – view students/feedback.
3. Add teacher `/ADMIN/add-teacher/`.
4. Manage subjects `/ADMIN/subjects/`.

**Run App**: `python manage.py migrate && python manage.py runserver`

**Fully functional with 6+ core functions, DB integration, user interaction.**
