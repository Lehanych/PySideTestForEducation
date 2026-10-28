from models.question import Question


positions = [1,2,3]
num_quests = [1,2]
questions = []
for position in positions:
    for num_quest in num_quests:
        questions.append(Question(
            position=position,
            title=f'Новый вопрос {num_quest}',
            question_str=f'Мой вопрос {num_quest} из категории {position}',
            answers=[f'Ответ 1 {num_quest}{position}', f'Ответ 2 {num_quest}{position}', f'Ответ 3 {num_quest}{position}', f'Ответ 4 {num_quest}{position}'],
            qtype='Неопределенный'
        )
        )