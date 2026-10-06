from validation import positive, text


class Student:
    def __init__(self, id: int, name: str, group: str):
        self.id = positive(id)
        self.name = text(name)
        self.group = text(group)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "group": self.group}

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(data["id"], data["name"], data["group"])

    def __str__(self) -> str:
        return f"№{self.id} {self.name} · {self.group}"
