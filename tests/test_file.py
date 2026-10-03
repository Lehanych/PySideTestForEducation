from storage.question_storage import QuestStorage
from models.question import Quest
from file_storage.quest_file_repository import QuestSaveLoadJSON

from tests import template_quest

questions = template_quest.questions


storage = QuestStorage()
repository = QuestSaveLoadJSON()

def test_save_load_quest():
    for quest in questions:
        storage.add_quest(quest)

    questions_from_file = repository.load_quest_json(full_path_file="D:/Programming/PythonProject/PySideAutoTest/Test save or load json file 1.json")
    assert questions_from_file
    assert questions == questions_from_file

    storage.remove_question(3)

    repository.save_quest_json(questions=storage.questions, name_file='json with deleted question 3')

