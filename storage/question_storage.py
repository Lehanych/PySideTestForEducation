from models.question import Quest

class QuestStorage:
    def __init__(self):
        self.questions: list[Quest] = []
        self.current_path = None
        self.id = 1

    def add_quest2(self, question: Quest):
        question.id = self.id
        self.questions.append(question)
        self.id += 1
        return Quest

    def add_empty_quest(self, title: str = "Новый вопрос", test_position = 0):
        question = Quest(test_position, self.id, title, "", ["", "", "", ""], "Неопределенный")
        self.id += 1
        self.questions.append(question)
        return Quest

    def get_quest_by_id(self, id_quest: int):
        for quest in self.questions:
            if quest.id == id_quest:
                return quest
        return None

    def remove_question(self,id_quest: int):
        for quest in self.questions:
            if quest.id == id_quest:
                self.questions.remove(quest)
                return True
        return False

    def get_question(self,index: int):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def get_all_questions(self):
        return self.questions.copy()

    def get_all_questions_from_category(self):
        pass

    def sort_questions_by_category(self):
        pass

    def create_test_one_v(self):
        pass