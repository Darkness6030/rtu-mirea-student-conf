from models.conference import Conference
from validation import positive, text


class Section:
    def __init__(self, id: int, name: str, conference: Conference, capacity: int):
        if not isinstance(conference, Conference):
            raise ValueError("Секция должна ссылаться на конференцию")
        self.id = positive(id)
        self.name = text(name)
        self.conference = conference
        self.capacity = positive(capacity)

    def has_free_slot(self, submitted: int) -> bool:
        return 0 <= submitted < self.capacity

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "conference_id": self.conference.id,
            "capacity": self.capacity,
        }

    def __str__(self) -> str:
        return f"№{self.id} {self.name} · {self.conference.name} · лимит {self.capacity}"
