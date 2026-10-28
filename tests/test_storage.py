from storage.question_storage import QuestStorage

from tests.templates import template_quest

questions = template_quest.questions

storage = QuestStorage()

def test_add_quest():
    storage.add_empty_quest()
    for quest in questions:
        storage.add_quest(quest)

def test_remove_quest():
    deleted_quest = storage.get_quest_by_id(3)
    storage.remove_question(3)

    assert deleted_quest in questions
    assert deleted_quest not in storage.questions
