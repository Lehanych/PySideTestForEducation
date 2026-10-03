from dataclasses import dataclass

@dataclass
class Quest:
    position : int
    title : str
    question_html : str
    answer_array_html : list[str]
    qtype : str
    id: int = 0

    def to_dict(self):
        return {
            "position": self.position,
            "id": self.id,
            "title": self.title,
            "qtype": self.qtype,
            "question_html": self.question_html,
            "answer_array_html": self.answer_array_html
        }

    # переход обратно к экземпляру класса из словаря
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            position=data["position"],
            id=data["id"],
            title = data["title"],
            qtype = data["qtype"],
            question_html=data["question_html"],
            answer_array_html=data["answer_array_html"]
        )

