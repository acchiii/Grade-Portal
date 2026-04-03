# Add Delete Section Feature to Teacher Dashboard

## Plan:
**Information Gathered:**
- `portal/templates/portal/teacher.html`: Lists sections as links to view, + button to create.
- No delete functionality currently.
- `portal/static/portal/images/delete.png` exists.
- Models: ClassSection has FK teacher, M2M students, on_delete=CASCADE safe for delete.
- Need new view/URL/form for delete section by ID.

**Plan:**
1. **Add `delete_section` view** in portal/views.py: check teacher owns section, section.students.all().clear() or cascade, delete section, message success, redirect teacher dashboard.
2. **Add URL** in portal/urls.py: path('teacher/section/<int:section_id>/delete/', views.delete_section, name='delete_section').
3. **Edit `portal/templates/portal/teacher.html`**: Add 🗑️ delete button/image next to each section card, with confirm POST form or JS.
4. Use delete.png icon.

**Dependent Files:**
- portal/views.py (new view)
- portal/urls.py (new URL)
- portal/templates/portal/teacher.html (add delete buttons)

**Followup:**
- Test: Teacher dashboard → delete section → "Section deleted successfully", gone from list.
- Runserver reload.

Confirm before implement?

