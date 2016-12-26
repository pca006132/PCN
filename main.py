import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QLabel, QLineEdit, QTextEdit, QCheckBox, QGridLayout, QComboBox, QToolTip
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import snbt
import style
import json

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def check_nbt(self):
        snbt.Tag.strict = self.use_strict.isChecked()
        try:
            tag = snbt.Tag.parse(str(self.nbt_edit.text()).strip())
            json_text = ''
            with open('test.json','r') as file:
                json_text = file.read()
            snbt.check_compound_items(snbt.load_json(json_text), tag,\
                str(self.base_list.currentText()))
            self.output.setText('No problem!')
        except snbt.NbtException as error:
            self.output.setText(error.message)
        except Exception as error:
            self.output.setText(str(error))

    def show_availables(self):
        try:
            with open('test.json','r') as file:
                json_text = file.read()
                tags = snbt.load_json(json_text)
            nbt = str(self.nbt_edit.text()).strip()
            self.output.setText(json.dumps(tags[str(self.base_list.currentText())], \
            sort_keys = True, indent = 4))
            if len(nbt) > 0:
                self.output.setText('Cannot find the requested NBT')
                outputs = []
                keys = list(tags[str(self.base_list.currentText())].keys())
                keys.sort()
                for key in keys:
                    if nbt in key.lower():
                        outputs.append('"%s": ' % key + json.dumps(\
                        tags[str(self.base_list.\
                        currentText())][key], sort_keys = True, indent = 4))
                if len(outputs) > 0:
                    self.output.setText(',\n'.join(outputs))

        except Exception as error:
            self.output.setText(str(error))

    def show_nbt_tree(self):
        try:
            tag = snbt.Tag.parse(str(self.nbt_edit.text()).strip())
            self.output.setText(tag.tree())
        except snbt.NbtException as error:
            self.output.setText(error.message)
        except Exception as error:
            self.output.setText(str(error))
    def initUI(self):
        QToolTip.setFont(QFont('Arial', 10))
        self.setWindowIcon(QIcon('image/icon.ico'))
        nbt_label = QLabel('NBT:')
        base_label = QLabel('Base tag:')

        self.nbt_edit = QLineEdit()

        json_text = ''
        keys = []
        try:
            with open('test.json','r') as file:
                json_text = file.read()
            keys = list(snbt.load_json(json_text).keys())
        except:
            exit()
        self.base_list = QComboBox()
        index = 0
        keys.sort()
        for key in keys:
            if key == '<entity>':
                index = len(self.base_list)
            self.base_list.addItem(key)
        self.base_list.setCurrentIndex(index)
        self.output = QTextEdit()
        self.use_strict = QCheckBox('Use Strict Mode?')
        self.use_strict.setToolTip("If true, it will check the type of the tags'+ \
            ' strictly.<br>For example, NoGravity:1 is not valid as 1 is int not byte.")
        self.output.setReadOnly(True)

        availables_btn = QPushButton('Show Tags')
        availables_btn.clicked.connect(self.show_availables)
        availables_btn.setToolTip('Show Nbt\'s type, and other data.<br>'+ \
            'Only shows children of the selected base tag.<br>'+ \
            'If NBT is empty, show all the children. Else, show all matched NBT')
        treebtn = QPushButton('Tree')
        treebtn.setToolTip('Pretty print the NBT.')
        treebtn.clicked.connect(self.show_nbt_tree)
        generate = QPushButton('Check nbt')
        generate.clicked.connect(self.check_nbt)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(nbt_label, 1, 0, 1, 1)
        grid.addWidget(self.nbt_edit, 1, 1, 1, 3)

        grid.addWidget(base_label, 2, 0, 1, 1)
        grid.addWidget(self.base_list, 2, 1, 1, 3)

        grid.addWidget(self.output, 3, 0, 4, 4)

        grid.addWidget(self.use_strict, 8, 0, 1, 1)
        grid.addWidget(availables_btn, 8, 1, 1, 1)
        grid.addWidget(treebtn, 8, 2, 1, 1)
        grid.addWidget(generate, 8, 3, 1, 1)

        self.setLayout(grid)

        self.setGeometry(400, 300, 600, 400)
        self.setWindowTitle('PCN')
        self.show()


if __name__ == '__main__':
    QApplication.addLibraryPath("./lib")

    app = QApplication(sys.argv)
    app.setStyleSheet(style.qss)
    ex = GUI()
    sys.exit(app.exec_())
