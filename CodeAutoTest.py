from __future__ import annotations
import json
import sys
import os
# from jinja2 import Template
import random
from html.parser import HTMLParser


from PySide6 import QtGui, QtGui
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import \
    QMainWindow, \
    QApplication, \
    QFileDialog, \
    QTextEdit, \
    QWidget, \
    QSizePolicy, \
    QSplitter, QTabWidget, \
    QPushButton, QToolButton, \
    QMenu, QTreeWidgetItem, QTreeWidget, \
    QGridLayout, QStatusBar, QToolBar, \
    QAbstractItemView

from models.question import Quest

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setup mainWindow
        self.setObjectName("MainWindow")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(880, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
        self.setToolTip("")
        self.setWhatsThis("")
        # Main widget in QMainWindow
        self.centralwidget = QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        # setup grid on QWidget
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        # Add PushButton
        self.PushBAddQuest = QPushButton(self.centralwidget)
        self.PushBAddQuest.setObjectName("PushButtAddQuest")
        self.gridLayout.addWidget(self.PushBAddQuest, 0, 0, 1, 1)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.PushBDeleteQuest = QPushButton(self.centralwidget)
        self.PushBDeleteQuest.setObjectName("PushBDeleteQuest")
        self.gridLayout.addWidget(self.PushBDeleteQuest, 0, 1, 1, 1)
        # setup list of Quest
        # создаём пустое хранилище для вопросов и ответов
        self.QStorage = QuestStorage()
        self.listViewContent = QTreeQA(self.QStorage, parent = self.centralwidget)
        self.listViewContent.setHeaderHidden(True)
        self.listViewContent.setSizePolicy(sizePolicy)
        self.listViewContent.setObjectName("listViewContent")
        self.gridLayout.addWidget(self.listViewContent, 2, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # setup a menu
        self.file_menu = self.menuBar().addMenu("File")
        # save test as
        self.action_savetest_json = QAction(self)
        self.action_savetest_json.triggered.connect(self.save_test_json)
        self.action_savetest_json.setObjectName("Save as JSON")
        self.save_as = self.file_menu.addMenu("Save as...")
        self.save_as.addAction(self.action_savetest_json)
        self.action_savetest_html = QAction()
        self.action_savetest_html.setObjectName("Save as HTML")
        self.action_savetest_html.triggered.connect(self.save_test_html)
        self.save_as.addAction(self.action_savetest_html)
        #
        self.actionImageQuest = QAction(self)
        self.actionImageQuest.setObjectName("actionImageQuest")
        self.actionTextAnswer = QAction(self)
        self.actionTextAnswer.setObjectName("actionTextAnswer")
        self.actionImageAnswer = QAction(self)
        self.actionImageAnswer.setObjectName("actionImageAnswer")
        # self.toolBar.addAction(self.action_SaveTest)
        # self.toolBar.addAction(self.actionImageQuest)
        # self.toolBar.addSeparator()
        # self.toolBar.addAction(self.actionTextAnswer)
        # self.toolBar.addAction(self.actionImageAnswer)
        self.retranslateUi()
        # Create workspace as vertical splitter
        self.SplitterWorkSpace = QSplitter(Qt.Vertical)
        # Create workspace for questions
        self.WorkSpaceQuest = TextEdit()
        self.WorkSpaceQuest.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred))
        self.WorkSpaceQuest.setMinimumHeight(100)
        # Create workspace for answers
        self.WorkSpaceAnswer = AnswerArea()
        self.WorkSpaceAnswer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.SplitterWorkSpace.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
        # set up splitters
        self.SplitterWorkSpace.setStretchFactor(0,1)
        self.SplitterWorkSpace.setStretchFactor(1,1)
        self.SplitterWorkSpace.addWidget(self.WorkSpaceQuest)
        self.SplitterWorkSpace.addWidget(self.WorkSpaceAnswer)
        self.SplitterWorkSpace.setChildrenCollapsible(False)
        # Add workspace to grid
        self.gridLayout.addWidget(self.SplitterWorkSpace, 0, 2, 3, 1)
        # Add buttons for create categories
        self.QAddBCategorie = QPushButton(self)
        self.QAddBCategorie.setText("Добавить категорию")
        self.gridLayout.addWidget(self.QAddBCategorie, 1, 0, 1, 1)
        # add buttons for delete categories
        self.PushBDeleteCategorie = QPushButton(self)
        self.PushBDeleteCategorie.setText("Удалить категорию")
        self.gridLayout.addWidget(self.PushBDeleteCategorie, 1, 1, 1, 1)
        # выбор первоначального размера сплиттера
        self.SplitterWorkSpace.setSizes([100, 400])
        # назначение кнопок для категорий
        self.QAddBCategorie.clicked.connect(self.add_category)
        self.PushBDeleteCategorie.clicked.connect(self.delete_category)
        # назначение кнопок для вопросов
        self.PushBAddQuest.clicked.connect(self.add_question)
        self.PushBDeleteQuest.clicked.connect(self.delete_question)
        # изначально отключаем кнопки удаления
        self.PushBDeleteQuest.setEnabled(False)
        self.PushBDeleteCategorie.setEnabled(False)
        # изначально отключаем кнопку создание вопроса без категорий
        self.PushBAddQuest.setEnabled(False)
        # set_up choice of question
        self.listViewContent.currentItemChanged.connect(self.item_changed)
        # when titla of tree was change

    def save_test_json(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить JSON", "", "JSON файлы (*.json)"
        )
        if filePath:
            self.QStorage.save_to_file(filePath)

    # Task: проработать вывод html теста, рассмотреть возможность интерактивного выполнения
    def save_test_html(self):
        n_var = 3
        data = self.QStorage.create_test_many_v_list(n_var=n_var)
        quest_n_answer_html_one_blocks = ""
        for i_var in range(n_var):
            title_var = f"Вариант {i_var}"
            # form inner 1 var
            inner_block_quest_answers = ""
            for i_category in range(len(data[i_var])):
                block_answers = ""
                for i_answ in range(len(data[i_var][i_category]["answer"])):
                    html_parser = QTextEditExtractor()
                    html_parser.feed(data[i_var][i_category]["answer"][i_answ])
                    parser_answer = html_parser.get_body()
                    block_answer = f"""
                    <div class = one-answer>
                        {parser_answer}
                    </div>
                    """
                    block_answers += block_answer
                inner_block_quest_answer = f"""
                    <div class = "block-quest">
                        {data[i_var][i_category]["question"]}
                    </div>
                    <div class = "block-answer">
                        {block_answers}
                    </div>
                """
                inner_block_quest_answers += inner_block_quest_answer

            quest_n_answer_html_one_block = f"""
                <div class = title_var>
                    {title_var}
                </div>
                <div class = "block-quest-answer"
                    {inner_block_quest_answers}    
                    </div>
                </div>
            """
            quest_n_answer_html_one_blocks += quest_n_answer_html_one_block

        html_test = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            
            @media print {{
                body {{
                    margin: 0;
                    padding: 15px;
                }}
                .question {{
                    page-break-inside: avoid;
                }}
                .answers {{
                    page-break-inside: avoid;
                }}
                button {{
                    display: none
                }}
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }}
            .question {{
            margin-bottom: 25px;
            padding: 10px;
            border-left: 3px solid #007bff;
            }}
            
            .question-text {{
            font-weight: bold;
            margin-bottom: 10px;
            }}
            
            .answers {{
            margin-left: 20px;
            }}
            
            .answer {{
            margin: 5px 0;
            }}
            
            button {{
            margin-top: 20px;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            }}
        </style>
        </head>
        
        <body>
            <div class="header">
                <h1>{{ test_data.title }}</h1>
                <p><strong>Ученик:</strong> {{ test_data.student }}</p>
                <p><strong>Дата:</strong> {{ test_data.date }}</p>
            </div>
            <div class="test">
                {quest_n_answer_html_one_blocks}
            </div>
        <body>
        """
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить HTML", "", "HTML файлы (*.html)"
        )
        if filePath:
            with open(filePath, 'w', encoding='utf-8') as file:
                file.write(html_test)
        return html_test

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.file_menu.setTitle(_translate("File","Файл"))
        self.setWindowTitle(_translate("MainWindow", "Test"))
        self.PushBAddQuest.setText(_translate("MainWindow", "Добавить вопрос"))
        self.PushBDeleteQuest.setText(_translate("MainWindow", "Удалить вопрос"))
        self.action_savetest_html.setText(_translate("Save as HTML", "Сохранить как HTML"))
        self.action_savetest_json.setText(_translate("Save as JSON", "Сохранить как JSON"))
        self.actionImageQuest.setText(_translate("MainWindow", "Добавить картинку ответа"))
        self.actionTextAnswer.setText(_translate("MainWindow", "Добавить текст ответа"))
        self.actionImageAnswer.setText(_translate("MainWindow", "Добавить картинку ответа"))
        self.actionImageAnswer.setToolTip(_translate("MainWindow", "Добавить картинку ответа"))

    # when change in content of questions
    def item_changed(self, item, prev_item):
        tree = self.listViewContent
        if item and -1 == tree.indexOfTopLevelItem(item):
            # включаем кнопку удаления вопроса
            self.PushBDeleteQuest.setEnabled(True)
            self.PushBDeleteCategorie.setEnabled(False)
            # включаем кнопку добавления вопроса при нажатии на вопрос
            self.PushBAddQuest.setEnabled(True)
            # Выгрузка вопроса и ответа в QTextEdit при нажатии
        # для категории
        if item and -1 != tree.indexOfTopLevelItem(item):
            # включаем кнопку удаления категории
            self.PushBDeleteQuest.setEnabled(False)
            self.PushBDeleteCategorie.setEnabled(True)
            # включаем кнопку добавления вопроса при нажатии на категорию
            self.PushBAddQuest.setEnabled(True)
            # отключаем рабочие поля
            self.WorkSpaceAnswer.setEnabled(False)
            self.WorkSpaceQuest.setEnabled(False)

        # Подключаем textedit'ы
        if item and -1 == tree.indexOfTopLevelItem(item):
            self.WorkSpaceAnswer.setEnabled(True)
            self.WorkSpaceQuest.setEnabled(True)
        if prev_item:
                if -1 == tree.indexOfTopLevelItem(prev_item):
                    # load current data to QStorage
                    prev_quest = self.QStorage.get_question(prev_item.id_q)
                    prev_quest.question_html = self.WorkSpaceQuest.toHtml()
                    prev_quest.answer_array_html = []
                    for tab in self.WorkSpaceAnswer.tabs:
                        prev_quest.answer_array_html.append(tab.toHtml())

        # load data from QStorage to WorkAreas
        if item and -1 == tree.indexOfTopLevelItem(item):
            self.WorkSpaceQuest.clear()
            cur_quest = self.QStorage.get_question(item.id_q)
            self.WorkSpaceQuest.insertHtml(cur_quest.question_html)
            while self.WorkSpaceAnswer.count() > 0:
                self.WorkSpaceAnswer.delete_tab(0)
            for answer in cur_quest.answer_array_html:
                tab = self.WorkSpaceAnswer.add_new_tab()
                tab.insertHtml(answer)


    # добавление категории
    def add_category(self):
        tree = self.listViewContent
        tree.add_category_toTree()
        # buttons on for delete category and add quest
        if not self.PushBDeleteCategorie.isEnabled():
            self.PushBDeleteCategorie.setEnabled(True)
        if not self.PushBAddQuest.isEnabled():
            self.PushBAddQuest.setEnabled(True)

    def delete_category(self):
        # текущая ветка
        tree = self.listViewContent
        # выбор текущей категории + обновление id
        tree.remove_category_FromTreeNStorage()
        if tree.topLevelItemCount() == 0:
            self.PushBDeleteCategorie.setEnabled(False)
            self.PushBAddQuest.setEnabled(False)
        if tree.currentItem():
            self.item_changed(tree.currentItem(), None)

    # добавление вопроса в категорию
    def add_question(self):
        tree = self.listViewContent
        tree.add_quest_toTree_and_QStorage()
        if not self.PushBDeleteQuest.isEnabled():
            self.PushBDeleteQuest.setEnabled(True)


    def delete_question(self):
        tree = self.listViewContent
        child_count = tree.currentItem().parent().childCount() - 1
        tree.remove_quest_fromTree_and_QStorage()
        # выключаем кнопку удаления, если удалять нечего
        if child_count == 0:
            self.PushBDeleteQuest.setEnabled(False)
            self.PushBAddQuest.setEnabled(False)

class QTextEditExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_body = False
        self.body_content = []
        self.body_tag_found = False

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
            self.body_tag_found = True
            attrs_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs) if attrs else ''
            self.body_content.append(f'<body{attrs_str}')
        elif self.in_body:
            attrs_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs) if attrs else ''
            self.body_content.append(f'<{tag}{attrs_str}>')
        self.current_tag = tag

    def handle_endtag(self, tag):
        if tag == 'body':
            self.body_content.append('</body>')
            self.in_body = False
        elif self.in_body:
            self.body_content.append(f'</{tag}>')

    def handle_data(self, data):
        if self.in_body:
            self.body_content.append(data)

    def handle_startendtag(self, tag, attrs):
        if self.in_body:
            attrs_str = ' ' + ' '.join(f'{k}="{v}"' for k, v in attrs) if attrs else ''
            self.body_content.append(f'<{tag}{attrs_str} />')

    def get_body(self):
        return ''.join(self.body_content)


# класс для формирования вопроса + ответы


class QuestStorage:
    def __init__(self):
        self.questions: list[Quest] = []
        self.current_path = None

    def add_quest(self, title: str = "Новый вопрос", id_category = 0) -> Quest:
        new_id = len(self.questions)
        question = Quest(id_category, new_id, title,"", ["","","",""], "Неопределенный")
        self.questions.append(question)
        return question

    def remove_question(self,index: int):
        if 0 <= index < len(self.questions):
            self.questions.pop(index)
            # update id in QTree!
            for i, q in enumerate(self.questions):
                q.id = i
            return True
        return False

    def get_question(self,index: int):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None

    def get_all_questions(self):
        return self.questions.copy()

    def get_all_questions_from_category(self):
        pass

    def sort_questions_by_category(self):
        pass

    def create_test_one_v(self):
        pass

    def create_test_many_v_list(self, n_var=1) -> list[list[dict[str,str]]]:
        list_quest: list[list[Quest]] = []
        for quest in self.questions:
            id_category = quest.id_category
            if id_category != 0:
                while len(list_quest) <= id_category:
                    list_quest.append([])
                list_quest[id_category].append(quest)
        # category with no name
        list_quest[0] = []
        for i_category in range(1,len(list_quest)):
                random.shuffle(list_quest[i_category])
        test = []
        for i_var in range(n_var):
            quest_one_var = []
            for i_category in range(1,len(list_quest)):
                quest_html = list_quest[i_category][i_var % len(list_quest[i_category])].question_html
                answer_html = list_quest[i_category][i_var % len(list_quest[i_category])].answer_array_html
                random.shuffle(answer_html)
                one_quest = {"question" : quest_html, "answer" : answer_html}
                quest_one_var.append(one_quest)
            test.append(quest_one_var)
        return test

    def save_to_file(self,file_path: str):
        data = {
            'version': '0.1.a',
            'title' : 'MyTest',
            'questions': [q.to_dict() for q in self.questions]
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.current_path = file_path

    def load_from_file(self, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.questions.clear()
        for q_data in data.get('questions',[]):
            question = Quest.from_dict(q_data)
            self.questions.append(question)
        self.current_path = file_path

class QTreeQA(QTreeWidget):
    def __init__(self, StorageQ:QuestStorage, parent=None):
        super().__init__(parent)
        # setup DragAndDrop
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setDropIndicatorShown(True)
        self.setSortingEnabled(False)
        self.id_quest_next = 1
        self.id_category_next = 1
        self.StorageQ = StorageQ
        # enable editing of items
        self.setEditTriggers(QAbstractItemView.DoubleClicked |
                             QAbstractItemView.EditKeyPressed)

    def dropEvent(self, event):
        target = self.itemAt(event.pos())
        dragged_items = self.selectedItems()
        parent_begin = dragged_items[0].parent()
        if not self.isDropAllowed(dragged_items, target):
            event.ignore()
            return
        super().dropEvent(event)
        # обновление id
        if dragged_items[0].parent() is None:
            self.update_id_categorynName()
        else:
            self.update_idAndName_quest(dragged_items[0].parent())
            self.update_idAndName_quest(parent_begin)



    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)
        target = self.itemAt(event.pos())
        dragged_items = self.selectedItems()
        if not self.isDropAllowed(dragged_items, target):
            event.ignore()

    def isDropAllowed(self, dragged_items, target):

        # убираем вставку в пустое место
        if target is None:
            return False
        # запрет самого в себя
        if target in dragged_items:
            return False

        drag_position = self.dropIndicatorPosition()
        # setup drag for category
        if dragged_items[0].parent() is None:
            # позволяем категориям вставляться в пустое место
            if target is None:
                return True
            if drag_position == QAbstractItemView.OnItem:
                return False
            # запрещаем вставлять в потомков
            for dragged in dragged_items:
                if self.isChildOf(target, dragged):
                    return False
            return True

        # setup drag for question
        if dragged_items[0].parent():
            # запрещаем вставлять в объекты одного уровня
            for dragged in dragged_items:
                if self.isSameLevel(target, dragged) and drag_position == QAbstractItemView.OnItem:
                    return False
            # запрещаем вставлять в корень
            if target.parent() is None and not drag_position == QAbstractItemView.OnItem:
                return False
        return True

    def isChildOf(self, possible_child, possible_parent):
        parent = possible_child.parent()
        if parent is not None:
            if parent == possible_parent:
                return True
        return False

    def isSameLevel(self, dragged, target):
        if target.parent() and dragged.parent():
            return True
        return False

    def add_category_toTree(self):
        id_category_next = self.id_category_next
        item = QTreeItem(tree=None, id_q=id_category_next)
        self.addTopLevelItem(item)
        self.id_category_next += 1
        # переименовываем по номерам
        item.setText(0, f"Категория {id_category_next}")
        self.clearSelection()
        self.setCurrentItem(item)
        item.setSelected(True)
        return item

    def remove_category_FromTreeNStorage(self):
        current = self.currentItem()
        # moving children in general category
        if current.childCount():
            if self.topLevelItem(0).id_q != 0:
                item_gen_category = QTreeItem(tree=None, id_q=0)
                self.insertTopLevelItem(0, item_gen_category)
                item_gen_category.setText(0, "Без категории")
            else:
                item_gen_category = self.topLevelItem(0)

            children = current.takeChildren()

            for child in children:
                if current.text(0) != "Без категории":
                    item_gen_category.addChild(child)
                    self.update_idAndName_quest(item_gen_category)
                else:
                    self.StorageQ.remove_question(child.question.id)
            for i_cat in range(self.topLevelItemCount()):
                self.update_idAndName_quest(self.topLevelItem(i_cat))

        # удаление категории и детей вместе с ней
        self.takeTopLevelItem(self.indexOfTopLevelItem(current))

        if self.currentItem():
            # выбрать следующий элемент
            self.currentItem().setSelected(True)
            # обновление id и имена
            self.update_id_categorynName()

    def add_quest_toTree_and_QStorage(self):
        curItem = self.currentItem()
        item = QTreeItem(tree=None,id_q=0)
        # need block because question is 0
        self.blockSignals(True)
        # checkup of selection category or item inside
        if curItem.parent() is None:
            # добавляем вопрос также в QStorage и кидаем ссылку в item
            curItem.addChild(item)
        else:
            curItem.parent().addChild(item)
        self.blockSignals(False)
        id_category = item.parent().id_q
        quest = self.StorageQ.add_quest(id_category=id_category)
        item.id_q = quest.id
        item.question = quest
        # раскрытие после добавления
        curItem.setExpanded(True)
        n_quest = item.parent().childCount()
        # переименовываем по номерам
        item.setText(0, f"Вопрос {n_quest}")

        # выбираем только что добавленный вопрос
        self.clearSelection()
        self.setCurrentItem(item)
        item.setSelected(True)
        return item

    def remove_quest_fromTree_and_QStorage(self):
        item = self.currentItem()
        self.StorageQ.remove_question(item.id_q)
        item.parent().takeChild(item.parent().indexOfChild(item))
        item = self.currentItem()
        if item:
            # выбрать следующий элемент и обновить id
            self.currentItem().setSelected(True)
            self.update_idAndName_quest(item.parent())


    def update_idAndName_quest(self, parent: QTreeItem):
        child_count = parent.childCount()

        # update name in category
        for i_item in range(child_count):
            if not parent.child(i_item).title_is_modified:
                parent.child(i_item).setText(0, f"Вопрос {i_item+1}")
            parent.child(i_item).id_q = parent.child(i_item).question.id
            parent.child(i_item).question.id_category = parent.id_q


    def update_id_categorynName(self):
        if self.topLevelItem(0):
            NzeroCategory = self.topLevelItem(0).id_q
        else:
            return
        for i in range(self.topLevelItemCount()):
            if self.topLevelItem(i).id_q == 0:
                continue
            self.topLevelItem(i).id_q = i + NzeroCategory
            if not self.topLevelItem(i).title_is_modified:
                id_top_level = self.topLevelItem(i).id_q
                self.topLevelItem(i).setText(0, f"Категория {id_top_level}")
        self.id_category_next = self.topLevelItemCount()


# Class of element of tree with id
class QTreeItem(QTreeWidgetItem):
    def __init__(self, tree, id_q):
        super().__init__(tree)
        self.id_q = id_q
        self.question = 0
        self.title_is_modified = False
        # enable editing of items
        self.setFlags(self.flags() | Qt.ItemIsEditable)


class AnswerArea(QTabWidget):
    def __init__(self):
        super().__init__()
        # Сначала выключены пока не добавлены вопросы
        self.setEnabled(False)
        # добавление кнопки плюс
        self.tabButton = QToolButton(self)
        self.tabButton.setText('+')
        # Делаем так, чтобы всё закрывалось
        self.setTabsClosable(True)
        self.setCornerWidget(self.tabButton)
        # ячейка для новых окон для ответов
        self.tabs = [TextEdit(),TextEdit(),TextEdit(),TextEdit()]
        tab_index = 1
        # Создание стандартных вкладок для ответов
        for tab in self.tabs:
            tab.setEnabled(True)
            self.addTab(tab, str(tab_index)+'-й ответ')
            tab_index += 1

        self.tabButton.clicked.connect(self.add_new_tab)
        self.tabCloseRequested.connect(self.delete_tab)

    def add_new_tab(self):
        new_widget = TextEdit()
        tab_index = self.insertTab(self.count(),new_widget, f"{len(self.tabs)+1}-й ответ")
        new_widget.setEnabled(True)
        self.tabs.append(new_widget)
        self.setCurrentIndex(tab_index)
        return new_widget

    def delete_tab(self,tab_index):
        widget_to_remove = self.widget(tab_index)
        self.removeTab(tab_index)
        if widget_to_remove in self.tabs:
            self.tabs.remove(widget_to_remove)
        for tab_i in range(len(self.tabs)):
            self.setTabText(tab_i, str(tab_i+1)+'-й ответ')
            tab_i += 1
        return widget_to_remove



class TextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

        #Изначально выключим
        self.setEnabled(False)
        # Настройки
        self.setMinimumWidth(200)
        self.setAcceptRichText(True)
        self.setAcceptDrops(True)

        # Включаем бары
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Добавляем контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        insert_image_action = menu.addAction("Вставить изображение")
        insert_image_action.triggered.connect(self.insert_image)
        save_content = menu.addAction("Сохранить")
        menu.exec_(self.mapToGlobal(pos))

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            cursor = self.textCursor()
            cursor.insertImage(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    '''
    MainWindow
    '''

    window.show()
    sys.exit(app.exec())
