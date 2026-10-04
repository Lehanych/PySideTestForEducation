from models.question import Question
import random


class GeneratorTestCreator:
    def __init__(self):
        pass
    def create_test_many_v_list(self,questions: list[Question], n_var=1) -> list[list[dict[str,str]]]:
        """
        :param questions:
        :param n_var:
        :return: list of var: list of questions in var: dict(qtype,question_str, answers)
        """

        list_quest: list[list[Question]] = []
        for quest in questions:
            position = quest.position
            if position != 0:
                while len(list_quest) <= position:
                    list_quest.append([])
                list_quest[position].append(quest)
        # category with no name
        list_quest[0] = []
        for i_pos in range(1,len(list_quest)):
                random.shuffle(list_quest[i_pos])
        shuffled_questions = []
        for i_var in range(n_var):
            quest_one_var = []
            for i_pos in range(1,len(list_quest)):
                one_question = list_quest[i_pos][i_var % len(list_quest[i_pos])]

                qtype = one_question.qtype
                question_str = one_question.question_str
                answers = one_question.answers

                random.shuffle(answers)

                one_quest = {'qtype': qtype,"question" : question_str, "answer" : answers}
                quest_one_var.append(one_quest)

            shuffled_questions.append(quest_one_var)
        return shuffled_questions