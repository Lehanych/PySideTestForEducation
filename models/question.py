from dataclasses import dataclass

@dataclass
class Question:
    position : int
    title : str
    question_str : str
    answers : list[str]
    qtype : str
    id: int = 0

    def to_dict(self):
        return {
            "position": self.position,
            "id": self.id,
            "title": self.title,
            "qtype": self.qtype,
            "question_str": self.question_str,
            "answers": self.answers
        }

    # переход обратно к экземпляру класса из словаря
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            position=data["position"],
            id=data["id"],
            title = data["title"],
            qtype = data["qtype"],
            question_str=data["question_str"],
            answers=data["answers"]
        )

