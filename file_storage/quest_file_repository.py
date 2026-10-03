import json
import os
from pathlib import Path

from models.question import Quest


class QuestSaveLoadJSON:
    def __init__(self):
        self.dir_path = os.getcwd()

    def save_quest_json(self, questions:list[Quest], path_file: str = '', name_file = '', test_title = 'MyTest', version = '0.1.a', ):
        data = {
            'version': version,
            'title': test_title,
            'questions': [q.to_dict() for q in questions]
        }
        if not name_file:
            name_file = test_title
        if not path_file:
            path_file = self.dir_path

        full_path_file = os.path.join(path_file, name_file) + '.json'

        try:
            with open(full_path_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print('Тест сохранен успешно')
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
        self.dir_path = path_file


    def load_quest_json(self, full_path_file: str = '', name_file = ''):
        try:
            with open(full_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return False
        questions = []
        for q_data in data.get('questions', []):
            question = Quest.from_dict(q_data)
            questions.append(question)
        path = Path(full_path_file).resolve()
        self.dir_path = path.parent
        return questions