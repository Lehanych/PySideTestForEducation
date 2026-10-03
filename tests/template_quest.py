from models.question import Quest


positions = [1,2,3]
num_quests = [1,2]
questions = []
for position in positions:
    for num_quest in num_quests:
        questions.append(Quest(
            position=position,
            title=f'Новый вопрос {num_quest}',
            question_html=f'Мой вопрос {num_quest} из категории {position}',
            answer_array_html=[f'Ответ 1 {num_quest}{position}', f'Ответ 2 {num_quest}{position}', f'Ответ 3 {num_quest}{position}', f'Ответ 4 {num_quest}{position}'],
            qtype='Неопределенный'
        )
        )