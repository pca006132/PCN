import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QLabel, QLineEdit, QTextEdit, QCheckBox, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import snbt

class GUI(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def check_nbt(self):
        snbt.Tag.strict = self.use_strict.isChecked()
        try:
            tag = snbt.Tag.parse(str(self.nbt_edit.text()))
            json_text = ''
            with open('test.json','r') as file:
                json_text = file.read()
            snbt.check_compound_items(snbt.load_json(json_text), tag,\
                str(self.base_edit.text()))
            self.output.setText('No problem!')
        except snbt.NbtException as error:
            self.output.setText(error.message)

    def initUI(self):
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowIcon(QIcon('image/icon.ico'))
        nbt_label = QLabel('NBT:')
        base_label = QLabel('Base tag:')

        self.nbt_edit = QLineEdit()
        self.base_edit = QLineEdit('<entity>')
        self.output = QTextEdit()
        self.use_strict = QCheckBox('Use Strict Mode?')
        self.output.setReadOnly(True)
        generate = QPushButton('Check nbt')
        generate.clicked.connect(self.check_nbt)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(nbt_label, 1, 0, 1, 1)
        grid.addWidget(self.nbt_edit, 1, 1, 1, 3)

        grid.addWidget(base_label, 2, 0, 1, 1)
        grid.addWidget(self.base_edit, 2, 1, 1, 3)

        grid.addWidget(self.output, 3, 0, 4, 4)

        grid.addWidget(self.use_strict, 8, 0, 1, 2)
        grid.addWidget(generate, 8, 2, 1, 2)

        self.setLayout(grid)

        self.setGeometry(400, 300, 600, 400)
        self.setWindowTitle('NBT checker')
        self.show()


if __name__ == '__main__':
    QApplication.addLibraryPath("./")
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
