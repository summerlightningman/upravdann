from PyQt5 import QtWidgets, QtSql, QtGui, QtCore, QtPrintSupport
from PyQt5.QtWidgets import QMessageBox

import form


class MainWindow(QtWidgets.QMainWindow):
    facults, streams, sections, groups, cats = [], [], [], [], []
    group, value = str(), str()

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = form.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_2.show()

        self.ui.action.triggered.connect(self.about)
        self.ui.action_8.triggered.connect(self.info)

        self.ui.pushButton.clicked.connect(self.addPerson)
        self.ui.pushButton_2.clicked.connect(self.confirmSwap)
        self.ui.pushButton_3.clicked.connect(self.remove)
        self.ui.pushButton_4.clicked.connect(self.confirmSwap)
        self.ui.pushButton_5.clicked.connect(self.addPerson)
        self.ui.pushButton_6.clicked.connect(self.remove)
        self.ui.pushButton_7.clicked.connect(self.add)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_9.clicked.connect(self.deleteCath)
        self.ui.pushButton_10.clicked.connect(self.cathToList)
        self.ui.pushButton_11.clicked.connect(self.addTest)
        self.ui.pushButton_12.clicked.connect(self.deleteTest)
        self.ui.pushButton_13.clicked.connect(self.addMark)
        self.ui.pushButton_14.clicked.connect(self.deleteMark)
        self.ui.pushButton_15.clicked.connect(self.printMarks)
        self.ui.pushButton_16.clicked.connect(self.printGroups)

        self.ui.treeView.clicked.connect(self.editValue)
        self.ui.treeView.clicked.connect(self.students)
        self.ui.treeView.clicked.connect(self.tests)
        self.ui.listView.clicked.connect(self.editValue)
        self.ui.listView.clicked.connect(self.teachers)

        self.ui.tableView_2.clicked.connect(self.degree)
        self.ui.tableView.clicked.connect(self.marks)

        self.ui.groupBox_18.clicked.connect(self.tests)
        self.ui.spinBox.valueChanged.connect(self.tests)
        self.ui.comboBox_7.activated.connect(self.teacFromCath)
        self.ui.tabWidget.currentChanged.connect(self.viewTables)

    def resizeEvent(self, *args, **kwargs):
        self.ui.tableView.horizontalHeader().setDefaultSectionSize(self.ui.tabWidget.width() / 4)
        self.ui.tableView_2.horizontalHeader().setDefaultSectionSize(self.ui.tableView_2.width() / 3)
        self.ui.tableView_3.horizontalHeader().setDefaultSectionSize(self.ui.tab_8.width() / 4)
        self.ui.tableView_5.horizontalHeader().setDefaultSectionSize(self.ui.tableView_5.width() / 3)

    def viewTables(self):
        self.ui.tableView.horizontalHeader().setDefaultSectionSize(self.ui.tabWidget.width() / 4)
        self.ui.tableView_2.horizontalHeader().setDefaultSectionSize(self.ui.tableView_2.width() / 3)
        self.ui.tableView_3.horizontalHeader().setDefaultSectionSize(self.ui.tab_8.width() / 4)
        self.ui.tableView_5.horizontalHeader().setDefaultSectionSize(self.ui.tableView_5.width() / 3)

    def applyInDb(self):
        stud.database().commit()
        stud.submitAll()
        teac.database().commit()
        teac.submitAll()
        test.database().commit()
        test.submitAll()

    def about(self):
        QMessageBox.about(self, "О разработчике", """<h1>ИС "Деканат"</h1><table border='0' cellpadding='5'>
        <tr><td>Разработчик</td><td>Баранов Д.А.</td></tr><tr><td>Группа</td><td>ИТД-21</td></tr>
        <tr><td>Кафедра</td><td>Систем автоматизации проектных работ в информационных системах</td></tr><tr>
        <td>Преподаватели</td><td>Яскевич О.Г. и Иванов Д.В.</td></tr></table>
        <p align='center'>Для выполнения курсового проекта по дисциплине <u>Управление данными<u></p>""")

    def info(self):
        QMessageBox.information(self, 'Справка', """<h1>Справка об интерфейсе программы</h1>
        <p>Во вкладке "Студенты и проверочные работы" доступна большая часть работы: 
        Добавление, изменение и удаление факультетов, направлений, профилей подготовки, групп в дереве слева, 
        в том порядке, в котором они идут по мере раскрытия</p><p>Чтобы создать новый объект, нажмите кнопку "Добавить",
         после чего дважды по новому объекту с именем "Без имени", чтобы задать название (сокращённое)</p>
        <p>После выбора группы, при наличии в ней студентов, заполнится таблица справа, 
        находящаяся во вкладке студенты</p><p>При добавлении, также следует нажать дважды по полю из таблицы и записать 
        его значение. Вписывать следует все поля, кроме номера. Если значение вписано правильно, студент появится в базе
         данных, а также ему будет автоматически присвоен номер</p>
        """, QMessageBox.Ok, QMessageBox.Ok)

    def start(self):

        con.open()
        data.dataChanged.connect(self.editOrAdd)
        data.setColumnCount(2)
        sql.exec('SELECT short FROM cathedra')
        if sql.isActive():
            sql.first()
            while sql.isValid():
                self.cats.append(sql.value(0))
                sql.next()
        cath.setStringList(self.cats)
        cath.dataChanged.connect(self.editAddCath)
        self.ui.listView.setModel(cath)
        self.ui.comboBox_2.setModel(cath)
        sql.exec('SELECT name FROM degree')
        if sql.isActive():
            sql.first()
            while sql.isValid():
                self.ui.comboBox_3.addItem(sql.value(0))
                sql.next()

        sql.exec('SELECT short FROM faculity')
        if sql.isActive():
            sql.first()
            while sql.isValid():
                self.facults.append(QtGui.QStandardItem(sql.value(0)))
                sql.next()
        for row in self.facults:
            data.appendRow([row])
            sql.prepare(
                'SELECT short FROM stream WHERE faculity_id = '
                '(SELECT faculity_id FROM faculity WHERE short = ?)')
            sql.addBindValue(row.text())
            sql.exec_()
            if sql.isActive():
                sql.first()
                while sql.isValid():
                    self.streams.append(QtGui.QStandardItem(sql.value(0)))
                    row.appendRow(self.streams[-1])
                    sql.next()
        for row in self.streams:
            sql.prepare(
                'SELECT short FROM section WHERE stream_id = '
                '(SELECT stream_id FROM stream WHERE short = ?)')
            sql.addBindValue(row.text())
            sql.exec_()
            if sql.isActive():
                sql.first()
                while sql.isValid():
                    self.sections.append(QtGui.QStandardItem(sql.value(0)))
                    row.appendRow(self.sections[-1])
                    sql.next()
        for row in self.sections:
            sql.prepare(
                'SELECT name FROM class WHERE section_id = '
                '(SELECT section_id FROM section WHERE short = ?)')
            sql.addBindValue(row.text())
            sql.exec_()
            if sql.isActive():
                sql.first()
                while sql.isValid():
                    self.groups.append(QtGui.QStandardItem(sql.value(0)))
                    row.appendRow([QtGui.QStandardItem(''), self.groups[-1]])
                    sql.next()
        self.ui.treeView.setModel(data)
        self.ui.treeView.setColumnWidth(0, 200)

    def teachers(self):
        self.ui.label_5.setStyleSheet('color: black; font-size: 16px; background: white')
        self.ui.label_5.setText('Преподаватели кафедры  ' + self.value + '<hr>')
        self.ui.comboBox_2.setCurrentText(self.value)
        teac.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        con.open()
        sql.prepare('SELECT cathedra_id FROM cathedra WHERE short = ?')
        sql.addBindValue(self.value)
        sql.exec_()
        sql.first()
        teac.setTable('teacher')
        teac.setFilter('teacher.cathedra_id = ' + str(sql.value(0)))
        teac.select()

        teac.setHeaderData(3, QtCore.Qt.Horizontal, 'Фамилия')
        teac.setHeaderData(4, QtCore.Qt.Horizontal, 'Имя')
        teac.setHeaderData(5, QtCore.Qt.Horizontal, 'Отчество')
        self.ui.tableView_2.setModel(teac)
        self.ui.tableView_2.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tableView_2))
        for i in range(3):
            self.ui.tableView_2.hideColumn(i)

    def degree(self, index):
        sql.prepare('SELECT `name` FROM degree WHERE degree_id = ?')
        sql.addBindValue(teac.record(index.row()).field('degree_id').value())
        sql.exec_()
        sql.first()
        self.ui.comboBox_3.setCurrentText(sql.value(0))

    def students(self, index):
        self.ui.comboBox.clear()
        self.ui.label_4.setStyleSheet('color: black; font-size: 16px;')
        if index.column() == 1:
            if self.ui.treeView.currentIndex().column() == 1:
                self.ui.label_4.setText(
                    'Студенты группы ' + index.data()
                    + '<hr>')
            stud.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
            stud.setTable('student')
            sql.prepare('SELECT class_id FROM class WHERE `name` = ?')
            sql.addBindValue(index.data())
            sql.exec_()
            sql.first()
            self.group = str(sql.value(0))
            stud.setFilter('student.class_id = ' + self.group)
            stud.setSort(1, QtCore.Qt.AscendingOrder)
            stud.select()
            stud.setHeaderData(0, QtCore.Qt.Horizontal, 'Номер')
            stud.setHeaderData(1, QtCore.Qt.Horizontal, 'Фамилия')
            stud.setHeaderData(2, QtCore.Qt.Horizontal, 'Имя')
            stud.setHeaderData(3, QtCore.Qt.Horizontal, 'Отчество')
            sql.prepare('SELECT name FROM class WHERE section_id = (SELECT section_id FROM class WHERE `name` = ?)')
            sql.addBindValue(index.data())
            sql.exec_()
            if sql.isActive():
                sql.first()
                while sql.isValid():
                    self.ui.comboBox.addItem(sql.value(0))
                    sql.next()
            self.ui.comboBox.setCurrentText(index.data())
            self.ui.tableView.setModel(stud)
            self.ui.tableView.setItemDelegate(QtSql.QSqlRelationalDelegate(self.ui.tableView))
            self.ui.tableView.hideColumn(4)

    def teacFromCath(self):
        self.ui.comboBox_6.clear()
        if self.ui.comboBox_7.count() != 0:
            sql.prepare('SELECT s_name FROM teacher WHERE cathedra_id = '
                        '(SELECT cathedra_id FROM cathedra WHERE short = ?)')
            sql.addBindValue(self.ui.comboBox_7.currentText())
            sql.exec_()
            if sql.isActive():
                sql.first()
                while sql.isValid():
                    self.ui.comboBox_6.addItem(sql.value(0))
                    sql.next()

    def tests(self):
        self.ui.label_3.setStyleSheet('color: black; font-size: 16px;')
        if self.ui.treeView.currentIndex().column() == 1:
            self.ui.label_3.setText('Проведённые проверочные работы группы ' + self.ui.treeView.currentIndex().data()
                                    + '<hr>')
        self.ui.comboBox_5.clear()
        if self.ui.treeView.currentIndex().column() == 1:
            test.setEditStrategy(QtSql.QSqlRelationalTableModel.OnManualSubmit)
            test.setTable('test')
            filter = 'test.class_id = ' + self.group
            if self.ui.groupBox_18.isChecked() is True:
                filter += ' AND test.semester = ' + str(self.ui.spinBox.value())
            test.setFilter(filter)
            test.setRelation(4, QtSql.QSqlRelation('teacher', 'teacher_id', 's_name'))
            test.setRelation(2, QtSql.QSqlRelation('subject', 'subject_id', 'name'))
            test.setHeaderData(1, QtCore.Qt.Horizontal, 'Вид')
            test.setHeaderData(2, QtCore.Qt.Horizontal, 'Дисциплина')
            test.setHeaderData(4, QtCore.Qt.Horizontal, 'Фамилия преподавателя')
            test.setHeaderData(5, QtCore.Qt.Horizontal, 'Дата')
            test.select()
            self.ui.tableView_3.setModel(test)
            self.ui.tableView_3.horizontalHeader().setDefaultSectionSize(self.ui.tab_8.width() / 4)
            self.ui.tableView_3.hideColumn(0)
            self.ui.tableView_3.hideColumn(3)

            sql.exec('SELECT `name` FROM subject')
            sql.first()
            while sql.isValid():
                self.ui.comboBox_5.addItem(sql.value(0))
                sql.next()
            sql.exec('SELECT short FROM cathedra')
            sql.first()
            while sql.isValid():
                self.ui.comboBox_7.addItem(sql.value(0))
                sql.next()
            self.teacFromCath()

    def addTest(self):
        sql.prepare(
            'INSERT INTO test (`mode`, subject_id, class_id, teacher_id, `date`, semester) VALUES ('
            '?, '
            '(SELECT subject_id FROM `subject` WHERE `name` = ?), '
            '?, '
            '(SELECT teacher_id FROM teacher WHERE s_name = ? AND cathedra_id = '
            '(SELECT cathedra_id FROM cathedra WHERE short = ?)), '
            '?, ?)')
        sql.addBindValue(self.ui.comboBox_4.currentText())
        sql.addBindValue(self.ui.comboBox_5.currentText())
        sql.addBindValue(int(self.group))
        sql.addBindValue(self.ui.comboBox_6.currentText())
        sql.addBindValue(self.ui.comboBox_7.currentText())
        sql.addBindValue(str(self.ui.dateEdit.date().year()) + '-'
                         + str(self.ui.dateEdit.date().month()) + '-'
                         + str(self.ui.dateEdit.date().day()))
        sql.addBindValue(self.ui.spinBox.value())
        sql.exec_()
        con.commit()
        self.tests()

    def marks(self):
        self.ui.label_2.setStyleSheet('color: black; font-size: 16px;')
        self.ui.label_2.setText('Зачётные ведомости студента ' + self.ui.tableView.currentIndex().sibling(
            self.ui.tableView.currentIndex().row(), 1).data() + ' ' + self.ui.tableView.currentIndex().sibling(
            self.ui.tableView.currentIndex().row(), 2).data() + ' ' + self.ui.tableView.currentIndex().sibling(
            self.ui.tableView.currentIndex().row(), 3).data() + '<hr>')
        subj.setQuery(
            'SELECT s.name FROM test INNER JOIN subject s on test.subject_id = s.subject_id WHERE class_id = '
            '(SELECT class_id FROM student WHERE student_id = ' +
            str(self.ui.tableView.currentIndex().sibling(self.ui.tableView.currentIndex().row(), 0).data()) + ')')
        self.ui.comboBox_8.setModel(subj)
        self.ui.comboBox_8.setCurrentIndex(0)
        mark.setQuery('SELECT `name`, `mode`, mark, mark_id FROM mark m INNER JOIN test t on m.test_id = t.test_id '
                      'INNER JOIN subject s on t.subject_id = s.subject_id WHERE student_id = ' +
                      str(self.ui.tableView.currentIndex().sibling(self.ui.tableView.currentIndex().row(), 0).data()))
        mark.setHeaderData(0, QtCore.Qt.Horizontal, 'Дисциплина')
        mark.setHeaderData(1, QtCore.Qt.Horizontal, 'Вид проверочной работы')
        mark.setHeaderData(2, QtCore.Qt.Horizontal, 'Оценка')
        mark.setHeaderData(3, QtCore.Qt.Horizontal, 'ID')
        self.ui.tableView_5.horizontalHeader().setDefaultSectionSize(self.ui.tableView_5.width() / 3)
        self.ui.tableView_5.setModel(mark)

    def addMark(self):
        sql.prepare('INSERT INTO mark (student_id, test_id, mark) VALUES '
                    '(?, '
                    '(SELECT test_id FROM test WHERE subject_id = '
                    '(SELECT subject_id FROM subject WHERE `name` = ?) AND `mode` = ? AND class_id = '
                    '(SELECT class_id FROM student WHERE student_id = ?))'
                    ', ?)')
        sql.addBindValue(self.ui.tableView_4.selectedIndexes()[0].data())
        sql.addBindValue(self.ui.comboBox_8.currentText())
        sql.addBindValue(self.ui.comboBox_10.currentText())
        sql.addBindValue(self.ui.tableView_4.selectedIndexes()[0].data())
        sql.addBindValue(self.ui.comboBox_9.currentText())
        sql.exec_()
        con.commit()
        self.marks()

    def deleteMark(self):
        sql.prepare('DELETE FROM mark WHERE mark_id = ?')
        sql.addBindValue(self.ui.tableView_5.selectedIndexes()[3].data())
        sql.exec_()
        con.commit()
        self.marks()

    def deleteTest(self):
        sql.prepare('DELETE FROM test WHERE class_id = ? AND `mode` = ? AND subject_id = '
                    '(SELECT subject_id FROM subject WHERE name = ?)')
        sql.addBindValue(self.group)
        for index in self.ui.tableView_3.selectedIndexes():
            if len(sql.boundValues()) == 3:
                sql.clear()
                sql.prepare('DELETE FROM test WHERE class_id = ? AND `mode` = ? AND subject_id = '
                            '(SELECT subject_id FROM subject WHERE name = ?)')
                sql.addBindValue(self.group)
            else:
                sql.addBindValue(index.data())
        self.tests()

    def switchSemester(self):
        self.tests()

    def forAddTeacs(self):
        request = []
        sql.prepare('SELECT cathedra_id FROM cathedra WHERE short = ?')
        sql.addBindValue(self.ui.comboBox_2.currentText())
        sql.exec_()
        sql.first()
        request.append(sql.value(0))
        sql.prepare('SELECT degree_id FROM degree WHERE name = ?')
        sql.addBindValue(self.ui.comboBox_3.currentText())
        sql.exec_()
        sql.first()
        request.append(sql.value(0))
        return request

    def remove(self):
        if len(self.ui.tableView.selectedIndexes()) == 0 and len(self.ui.tableView_2.selectedIndexes()) == 0:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Нет выделенных записей для удаления')
        else:
            dia = QtWidgets.QMessageBox.warning(self, 'Подтверждение удаления',
                                                'Вы действительно желаете удалить данного ' + \
                                                ('студента?' if QtCore.QObject.sender(
                                                    self).objectName() == 'pushButton_3' else 'преподавателя?'),
                                                buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if dia == 16384:
                if QtCore.QObject.sender(self).objectName() == 'pushButton_3':
                    for index in self.ui.tableView.selectedIndexes():
                        stud.removeRow(index.row())
                        stud.submitAll()
                        stud.database().commit()
                        stud.select()
                else:
                    for index in self.ui.tableView_2.selectedIndexes():
                        teac.removeRow(index.row())
                        teac.submitAll()
                        teac.database().commit()
                        teac.select()

    def addPerson(self):
        if QtCore.QObject.sender(self).objectName() == 'pushButton':
            stud.insertRow(stud.rowCount())
            row = stud.record(stud.rowCount())
            row.setValue('class_id', self.group)
            stud.setRecord(stud.rowCount() - 1, row)
            stud.database().commit()
            stud.submitAll()
        else:
            teac.insertRow(teac.rowCount())
            row = teac.record(teac.rowCount())
            row.setValue('cathedra_id', self.forAddTeacs()[0])
            row.setValue('degree_id', self.forAddTeacs()[1])
            teac.setRecord(teac.rowCount() - 1, row)
            stud.database().commit()
            teac.submitAll()

    def add(self):
        if self.ui.treeView.currentIndex().data() is not None:
            if self.ui.treeView.currentIndex().parent().data() is not None:
                if self.ui.treeView.currentIndex().parent().parent().data() is not None:
                    for i in range(len(self.sections)):
                        if self.sections[i].text() == self.ui.treeView.currentIndex().data():
                            self.sections[i].appendRow([QtGui.QStandardItem(''), QtGui.QStandardItem('<Без имени>')])
                else:
                    for i in range(len(self.streams)):
                        if self.streams[i].text() == self.ui.treeView.currentIndex().data():
                            self.streams[i].appendRow([QtGui.QStandardItem('<Без имени>')])
            else:
                for i in range(len(self.facults)):
                    if self.facults[i].text() == self.ui.treeView.currentIndex().data():
                        self.facults[i].appendRow([QtGui.QStandardItem('<Без имени>')])
        else:
            data.appendRow(QtGui.QStandardItem('<Без имени>'))

    def confirmSwap(self):
        if QtCore.QObject.sender(self).objectName() == 'pushButton_2':
            if len(self.ui.tableView.selectedIndexes()) == 0:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Нет выделенных студентов для редактирования')
            else:
                for index in self.ui.tableView.selectedIndexes():
                    row = stud.record(index.row())
                    sql.prepare('SELECT class_id FROM class WHERE `name` = ?')
                    sql.addBindValue(self.ui.comboBox.currentText())
                    sql.exec_()
                    sql.first()
                    row.setValue('class_id', int(sql.value(0)))
                    stud.setRecord(index.row(), row)
            stud.database().commit()
            stud.submitAll()
            stud.select()
        else:
            if not self.ui.tableView_2.selectedIndexes():
                QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Нет выделенных преподавателей для редактирования')
            else:
                for index in self.ui.tableView_2.selectedIndexes():
                    row = teac.record(index.row())
                    row.setValue('cathedra_id', self.forAddTeacs()[0])
                    row.setValue('degree_id', self.forAddTeacs()[1])
                    teac.setRecord(index.row(), row)
            teac.database().commit()
            teac.submitAll()
            teac.select()

    def editOrAdd(self):
        sql, table, idx = QtSql.QSqlQuery(), str(), str()
        if self.ui.treeView.currentIndex().data() is not None:
            if self.ui.treeView.currentIndex().parent().data() is not None:
                if self.ui.treeView.currentIndex().parent().parent().data() is not None:
                    if self.ui.treeView.currentIndex().parent().parent().parent().data() is not None:
                        table = 'class'
                        sql.prepare('SELECT section_id FROM section WHERE short = ?')
                    else:
                        table = 'section'
                        sql.prepare('SELECT stream_id FROM stream WHERE short = ?')
                else:
                    table = 'stream'
                    sql.prepare('SELECT faculity_id FROM faculity WHERE short = ?')
            else:
                table = 'faculity'
        sql.addBindValue(self.ui.treeView.currentIndex().parent().data())
        sql.exec_()
        sql.first()
        idx = sql.value(0)
        if self.value == '<Без имени>':
            sql.prepare(
                'INSERT INTO ' + table + ' VALUES (NULL, ?, ' + ('NULL' if table == 'faculity' else '? , NULL') + ')')
            if table != 'faculity':
                sql.addBindValue(idx)
            sql.addBindValue(self.ui.treeView.currentIndex().data())
        else:
            sql.prepare('UPDATE ' + table + ' SET ' + ('short' if table != 'class' else 'name') + ' = ? WHERE ' + (
                'short' if table != 'class' else 'name') + ' = ?')
            sql.addBindValue(self.ui.treeView.currentIndex().data())
            sql.addBindValue(self.value)
        result = sql.exec_()
        if not result:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Ошибка изменения данных в базе данных')
        else:
            con.commit()

    def editValue(self, index):
        if index.data != '':
            self.value = index.data()

    def editAddCath(self):
        if self.value == '<Без имени>':
            sql.prepare('INSERT INTO cathedra (short) VALUES (?)')
            sql.addBindValue(self.ui.listView.currentIndex().data())
        else:
            sql.prepare('UPDATE cathedra SET short = ? WHERE short = ?')
            sql.addBindValue(self.ui.listView.currentIndex().data())
            sql.addBindValue(self.value)
        if sql.exec_() is False:
            QtWidgets.QMessageBox.critical(self, 'Ошибка ', 'Не удаётся выполнить операцию с кафедрами')
        else:
            con.commit()

    def cathToList(self):
        self.cats.append('<Без имени>')
        cath.setStringList(self.cats)

    def deleteCath(self):
        self.cats.pop(self.cats.index(self.value))
        cath.setStringList(self.cats)
        sql.prepare('DELETE FROM cathedra WHERE short = ?')
        sql.addBindValue(self.value)
        sql.exec_()
        con.commit()

    def delete(self):
        if self.ui.treeView.currentIndex().parent().data() is not None:
            if self.ui.treeView.currentIndex().parent().parent().data() is not None:
                if self.ui.treeView.currentIndex().parent().parent().parent().data() is not None:
                    table = 'class'
                    for i in range(len(self.sections)):
                        if self.sections[i].text() == self.ui.treeView.currentIndex().parent().data():
                            self.sections[i].removeRow(self.ui.treeView.currentIndex().row())
                else:
                    table = 'section'
                    for i in range(len(self.streams)):
                        if self.streams[i].text() == self.ui.treeView.currentIndex().parent().data():
                            self.streams[i].removeRow(self.ui.treeView.currentIndex().row())
            else:
                table = 'stream'
                for i in range(len(self.facults)):
                    if self.streams[i].text() == self.ui.treeView.currentIndex().parent().data():
                        self.facults[i].removeRow(self.ui.treeView.currentIndex().row())
        else:
            table = 'faculity'
            data.removeRow(self.ui.treeView.currentIndex().row())
        sql.prepare('DELETE FROM ' + table + ' WHERE ' + ('name' if table == 'class' else 'short') + ' = ?')
        sql.addBindValue(self.value)
        if sql.exec_() is False:
            QtWidgets.QMessageBox.critical(self, 'Ошибка удаления', 'Удаление прошло неудачно')
        else:
            con.commit()

    def printMarks(self):
        percent, marks, text, painter, student = str(), str(), QtGui.QTextDocument(), QtGui.QPainter(), \
                                                 dict.fromkeys(['группа', 'фамилия', 'имя', 'отчество'])
        sql.prepare('SELECT s.`name`, `mode`, mark, c.name, s_name, s2.name, t_name  FROM mark m '
                    'INNER JOIN test t on m.test_id = t.test_id '
                    'INNER JOIN subject s on t.subject_id = s.subject_id '
                    'INNER JOIN student s2 on m.student_id = s2.student_id '
                    'INNER JOIN class c on s2.class_id = c.class_id WHERE m.student_id = ?')
        sql.addBindValue(self.ui.tableView.currentIndex().sibling(self.ui.tableView.currentIndex().row(), 0).data())
        sql.exec_()
        if sql.isActive():
            sql.first()
            student = {'группа': sql.value(3), 'фамилия': sql.value(4), 'имя': sql.value(5), 'отчество': sql.value(6)}
            while sql.isValid():
                marks += '<p>' + sql.value(0) + ' (' + sql.value(1) + ') - ' + sql.value(2) + '</p>'
                sql.next()

        printer = QtPrintSupport.QPrinter()
        printer.setOutputFileName(student['фамилия'] + student['группа'] + '.pdf')
        printer.setPageLayout(QtGui.QPageLayout(QtGui.QPageSize(QtGui.QPageSize.A5), QtGui.QPageLayout.Portrait,
                                                QtCore.QMarginsF(1, 1, 1, 1), units=QtGui.QPageLayout.Inch))
        # printer.setPrinterName('Canon G1010 series')

        painter.begin(printer)
        text.setDefaultFont(QtGui.QFont('Times New Roman', 14))
        text.setDefaultStyleSheet('h2{text-align: center;}')

        if self.ui.checkBox.isChecked():
            sql.prepare(
                'SELECT ((SELECT count(*) FROM mark WHERE student_id = :s AND mark = "Отлично") * 5 + '
                '(SELECT count(*) FROM mark WHERE student_id = :s AND mark="Хорошо") * 4 + '
                '(SELECT count(*) FROM mark WHERE student_id = :s AND mark = "Удовлетворительно") * 3 + '
                '(SELECT count(*) FROM mark WHERE student_id = :s AND mark="Неудовлетворительно") * 2)'
                '/count(*) FROM mark WHERE student_id = :s')
            sql.bindValue(':s',
                          self.ui.tableView.currentIndex().sibling(self.ui.tableView.currentIndex().row(), 0).data())
            sql.exec_()
            sql.first()
            percent = str(sql.value(0))

        text.setHtml(
            "<h1 align='center'>Выписка</h1><h2>из зачётных ведомостей</h2><p>Студент группы: " + student['группа']
            + ' ' + student['фамилия'] + ' ' + student['имя'] + ' ' + student['отчество'] + '<hr>' +
            marks + '<hr>Средний балл: ' + percent)

        text.drawContents(painter, QtCore.QRectF(0, 0, 1000, 1000))
        painter.end()

        # dia = QtPrintSupport.QPrintDialog()
        # dia.setOptions(
        #     QtPrintSupport.QAbstractPrintDialog.PrintToFile | QtPrintSupport.QAbstractPrintDialog.PrintSelection)
        # dia.exec()

    def printGroups(self):
        percent, marks, text, percents = dict.fromkeys(
            ['Отлично', 'Хорошо', 'Удовлетворительно', 'Неудовлетворительно'],
            0.0), [], QtGui.QTextDocument(), str()
        sql.prepare('SELECT mark, c.name FROM mark '
                    'INNER JOIN test t on mark.test_id = t.test_id '
                    'INNER JOIN class c on t.class_id = c.class_id '
                    'WHERE t.class_id = ? AND mode = ? AND subject_id = '
                    '(SELECT subject_id FROM subject WHERE name = ?) AND semester = ?')
        sql.addBindValue(self.group)
        sql.addBindValue(self.ui.tableView_3.selectedIndexes()[0].data())
        sql.addBindValue(self.ui.tableView_3.selectedIndexes()[1].data())
        sql.addBindValue(self.ui.tableView_3.selectedIndexes()[4].data())
        sql.exec_()
        if sql.isActive():
            sql.first()
            group = sql.value(1)
            while sql.isValid():
                marks.append(sql.value(0))
                sql.next()
            for row in percent.keys():
                percents += '<p>' + row + ': ' + str((marks.count(row) / len(marks)) * 100) + '% </p>'

        text.setDefaultFont(QtGui.QFont('Times New Roman', 14))
        text.setHtml(
            "<h1 align='center'>Статистика успеваемости</h1><h2 align='center'>По группе " + group + "</h2><hr>"
            + percents)
        self.ui.label.setText(text.toHtml())

        printer, painter = QtPrintSupport.QPrinter(), QtGui.QPainter()
        printer.setOutputFileName(group + 'стастистика' + '.pdf')
        printer.setPageLayout(QtGui.QPageLayout(QtGui.QPageSize(QtGui.QPageSize.A5), QtGui.QPageLayout.Portrait,
                                                QtCore.QMarginsF(1, 1, 1, 1), units=QtGui.QPageLayout.Inch))

        # printer.setPrinterName('Canon G1010 series')

        painter.begin(printer)
        text.setDefaultFont(QtGui.QFont('Times New Roman', 14))
        text.setDefaultStyleSheet('h2{text-align: center;}')

        text.drawContents(painter, QtCore.QRectF(0, 0, 1000, 1000))
        painter.end()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    con = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    con.setHostName('localhost')
    con.setUserName('root')
    con.setPassword('')
    con.setDatabaseName('decanat')
    if not con.open():
        QtWidgets.QMessageBox.critical(None, 'Ошибка подключения', 'Не удаётся подключиться к базе данных')
    else:
        sql = QtSql.QSqlQuery()

        w = MainWindow()
        stud = QtSql.QSqlTableModel(parent=w)
        teac = QtSql.QSqlTableModel(parent=w)
        test = QtSql.QSqlRelationalTableModel(parent=w)
        mark = QtSql.QSqlQueryModel(parent=w)
        subj = QtSql.QSqlQueryModel(parent=w)
        data = QtGui.QStandardItemModel()
        cath = QtCore.QStringListModel()
        stud.dataChanged.connect(w.applyInDb)
        teac.dataChanged.connect(w.applyInDb)
        test.dataChanged.connect(w.applyInDb)

        w.start()
        w.show()
        sys.exit(app.exec_())
