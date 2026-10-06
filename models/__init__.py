"""Предметная модель ПР3; обычные Python-классы, не Django ORM."""

from models.conference import Conference
from models.section import Section
from models.student import Student
from models.talk import Talk

__all__ = ["Conference", "Section", "Student", "Talk"]
