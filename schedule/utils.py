from schedule.Schedule_models import A_CourseSection


def create_default_section():
    default_section = A_CourseSection()
    default_section.professor = None  # {"id": 0, "name": ""}
    default_section.capacity = 0
    default_section.save()
    return default_section


