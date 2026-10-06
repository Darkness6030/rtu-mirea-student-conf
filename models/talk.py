from models.section import Section
from models.student import Student
from validation import positive, text


class Talk:
    def __init__(
        self,
        id: int,
        title: str,
        abstract: str,
        student: Student,
        section: Section,
        is_cancelled: bool = False,
    ):
        if not isinstance(student, Student) or not isinstance(section, Section):
            raise ValueError("Доклад должен ссылаться на студента и секцию")
        if type(is_cancelled) is not bool:
            raise ValueError("Статус должен иметь тип bool")
        self.id = positive(id)
        self.title = text(title)
        self.abstract = text(abstract)
        self.student = student
        self.section = section
        self._is_cancelled = is_cancelled

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

    @property
    def status(self) -> str:
        return "Отменён" if self.is_cancelled else "Подан"

    def cancel(self) -> None:
        self._is_cancelled = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "abstract": self.abstract,
            "student_id": self.student.id,
            "section_id": self.section.id,
            "is_cancelled": self.is_cancelled,
        }

    def __str__(self) -> str:
        return f"№{self.id} {self.title} · {self.student.name} · {self.status}"
