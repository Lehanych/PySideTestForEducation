import json
import os
from pathlib import Path

from models.question import Question


class QuestSaveLoadJSON:
    def __init__(self):
        self.dir_path = os.getcwd()

    def _load_json(self, full_path_file: str):
        if not full_path_file:
            print(f"Не указан путь")
            return {}
        if not os.path.isabs(full_path_file):
            full_path_file = os.path.join(self.dir_path, full_path_file)
        try:
            with open(full_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return {}

        path = Path(full_path_file).resolve()
        self.dir_path = path.parent
        return data

    def _save_json(self,data, path_file: str, name_file, test_title: str):
        if not name_file:
            name_file = test_title

        if not path_file or not os.path.isabs(path_file):
            path_file = os.path.join(self.dir_path, path_file)

        full_path_file = os.path.join(path_file, name_file) + '.json'

        try:
            with open(full_path_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print('Тест сохранен успешно')
            self.dir_path = path_file
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")


    def export_generated_test_json(self,
                                   generated_test: list[list[dict[str,str]]],
                                   path_file: str = '',
                                   name_file: str = '',
                                   title: str = 'Generated test',
                                   version: str = ''):
        """
        :param version: version of generated test
        :param name_file:
        :param path_file: you can just name file without define of path_file (it will placed in current directory)
        :param title: title of the test
        :param generated_test: it's generated test from test_generator.TestGenerator
        :return: saved test in JSON
        """
        data = {
            'version': version,
            'title': title,
            'generated_test': generated_test
        }
        self._save_json(data, path_file, name_file, name_file or title)


    def save_test_json(self,
                       questions:list[Question],
                       path_file: str = '',
                       name_file = '',
                       test_title = 'MyTest',
                       version = '0.1.a'):
        data = {
            'version': version,
            'title': test_title,
            'questions': [q.to_dict() for q in questions]
        }
        self._save_json(data, path_file, name_file, name_file or test_title)


    def load_test_json(self, full_path_file: str = ''):
        data = self._load_json(full_path_file)
        if data:
            questions = []
            for q_data in data.get('questions', []):
                question = Question.from_dict(q_data)
                questions.append(question)
        else:
            print("Не удалось загрузить тест")
            return False
        return questions

    def import_test_json(self, full_path_file: str = ''):
        data = self._load_json(full_path_file)
        if data:
            return data['generated_test']
        else:
            return False