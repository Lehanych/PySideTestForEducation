from storage.question_storage import QuestStorage
from repositories.quest_file_repository import QuestSaveLoadJSON

from tests.templates import template_quest

questions = template_quest.questions


storage = QuestStorage()
repository = QuestSaveLoadJSON()

def test_save_load_quest():
    for quest in questions:
        storage.add_quest(quest)

    repository.save_test_json(questions=storage.questions, name_file='tests\\test_data\\Test save or load json file 1')
    questions_from_file = repository.load_test_json(full_path_file="tests\\test_data\\Test save or load json file 1.json")

    assert questions_from_file
    assert questions == questions_from_file

    storage.remove_question(3)

    repository.save_test_json(questions=storage.questions, name_file='json with deleted question 3')
    repository.load_test_json(full_path_file="json with deleted question 3")
    assert questions_from_file
    assert questions == questions_from_file

