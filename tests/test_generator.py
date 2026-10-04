from models.question import Question
from services.generator_of_test import GeneratorTestCreator as Generator
import tests.templates.template_quest as template_quest
from repositories.quest_file_repository import QuestSaveLoadJSON

questions = template_quest.questions

test_generator = Generator()

file_save_loader = QuestSaveLoadJSON()
def test_create_random_quest():
    generated_test = test_generator.create_test_many_v_list(questions, n_var = 6)
    file_save_loader.export_generated_test_json(generated_test, name_file='tests\\test_data\\generated_test')

    generated_test_from_file = file_save_loader.export_generated_test_json(generated_test, name_file='tests\\test_data\\generated_test')

    assert generated_test_from_file == generated_test_from_file





