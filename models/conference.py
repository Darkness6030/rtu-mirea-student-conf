from datetime import date

from validation import iso_date, positive, text


class Conference:
    def __init__(self, id: int, name: str, event_date: date, deadline: date, location: str):
        self.id = positive(id)
        self.name = text(name)
        self.event_date = event_date
        self.deadline = deadline
        self.location = text(location)
        if not isinstance(event_date, date) or not isinstance(deadline, date):
            raise ValueError("Даты конференции должны иметь тип date")
        if deadline > event_date:
            raise ValueError("Срок подачи позже конференции")

    def is_open(self, today: date | None = None) -> bool:
        return (today or date.today()) <= self.deadline

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "event_date": self.event_date.isoformat(),
            "deadline": self.deadline.isoformat(),
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conference":
        return cls(
            data["id"],
            data["name"],
            iso_date(data["event_date"]),
            iso_date(data["deadline"]),
            data["location"],
        )

    def __str__(self) -> str:
        return f"№{self.id} {self.name} · {self.event_date} · приём до {self.deadline}"
