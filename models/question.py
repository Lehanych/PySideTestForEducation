class Quest:
    def __init__(self, id_category:int, id: int, title:str, question_html: str, answer_array: list[str], qtype: str):
        self.id = id
        self.type = qtype
        self.id_category = id_category
        self.question_html = question_html
        self.answer_array_html = answer_array
        self.title = title

    def to_dict(self):
        return {
            "id_category": self.id_category,
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "question_html": self.question_html,
            "answer_array_html": self.answer_array_html
        }

    # переход обратно к экземпляру класса из словаря
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_category=data["id_category"],
            id=data["id"],
            title = data["title"],
            qtype = data["type"],
            question_html=data["question_html"],
            answer_array=data["answer_array_html"]
        )