from storage.question_storage import QuestStorage
import json

# load questions
file_q = 'test.json'

with open(file_q, 'r', encoding='utf-8') as f:
    data = json.load(f)

storage = QuestStorage()

def add_quest(storage):
    question =
    storage.questions = data['questions']
