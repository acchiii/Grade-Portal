"""
Seed subjects on first run (mirrors db.php _seed_data).
Triggered via AppConfig.ready().
"""
from django.db.models.signals import post_migrate
from django.dispatch import receiver


SUBJECTS = [
    ('IT201', 'Data Structures & Algorithms',    3, 'BSIT'),
    ('IT101', 'Introduction to Computing',       3, 'BSIT'),
    ('ITNET1', 'Networking 1',       3, 'BSIT'),
    ('ITNET12', 'Networking 2',       3, 'BSIT'),
    ('IT301', 'Web Development',                 3, 'BSIT'),
    ('IT401', 'Database Management',             3, 'BSIT'),
    ('GE001', 'Purposive Communication',         3, 'GE'),
    ('GE002', 'Mathematics in the Modern World', 3, 'GE'),
    ('GE003', 'Understanding the Self',          3, 'GE'),
    ('PE001', 'Physical Education 1',            2, 'PE'),
    ('PE002', 'Physical Education 2',            2, 'PE'),
]


@receiver(post_migrate)
def seed_subjects(sender, **kwargs):
    if sender.name != 'portal':
        return
    from portal.models import Subject
    for code, title, units, dept in SUBJECTS:
        Subject.objects.get_or_create(
            code=code,
            defaults={'title': title, 'units': units, 'department': dept}
        )
