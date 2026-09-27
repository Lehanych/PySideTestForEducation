from models.question import Quest
import json



def test_question_to_dict_and_back():
    file_q = 'test.json'

    with open(file_q, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(data)

    questions_list = data['questions']
    one_question_dict = questions_list[0]

    # question = Quest(1, 2, "title","", ["","","",""], "Неопределенный")
    question = Quest.from_dict(one_question_dict)
    question2_dict = question.to_dict()
    assert one_question_dict == question2_dict

def test_question_placeholder():
    file_q = 'test.json'

    with open(file_q, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(data)

    questions_list = data['questions']
    one_question_dict = questions_list[0]

    question = Quest.from_dict(one_question_dict)

    assert question.id == one_question_dict['id']
    assert question.id_category == one_question_dict['id_category']
    assert question.title == one_question_dict['title']
    assert question.type == one_question_dict['type']
    assert question.question_html == one_question_dict['question_html']
    assert question.answer_array_html == one_question_dict['answer_array_html']