from tests.templates import template_quest

questions = template_quest.questions

def test_question_to_dict_and_back():
    one_quest = questions[0]
    question_dict = one_quest.to_dict()
    question2 = one_quest.from_dict(question_dict)
    assert question2 == one_quest

def test_question_placeholder():
    one_quest = questions[0]

    one_question_dict = one_quest.to_dict()

    assert one_quest.id == one_question_dict['id']
    assert one_quest.position == one_question_dict['position']
    assert one_quest.title == one_question_dict['title']
    assert one_quest.qtype == one_question_dict['qtype']
    assert one_quest.question_str == one_question_dict['question_str']
    assert one_quest.answers == one_question_dict['answers']