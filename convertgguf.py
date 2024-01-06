import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import subprocess
import os

class ConversionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.file_label = QLabel('File Path or URL:')
        self.file_edit = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.mode_label = QLabel('Conversion Mode:')
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(['cli', 'server', 'both'])
        self.convert_button = QPushButton('Convert')
        self.output_text = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combobox)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.output_text)

        self.browse_button.clicked.connect(self.browse_file)
        self.convert_button.clicked.connect(self.convert)

        self.setLayout(layout)
        self.setWindowTitle('Conversion App')

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select File', '', 'All Files (*);;GGUF Files (*.gguf)')
        if file_path:
            self.file_edit.setText(file_path)

    def convert(self):
        file_path = self.file_edit.text()
        mode = self.mode_combobox.currentText()

        try:
            self.output_text.clear()
            self.output_text.append(f"Converting {file_path} to llamafile with mode: {mode}\n")

            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'your_shell_script.sh')
            result = subprocess.run(['sh', script_path, file_path, mode], capture_output=True, text=True)

            self.output_text.append(result.stdout)
            if result.returncode != 0:
                self.output_text.append(f"Error: {result.stderr}")

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConversionApp()
    window.show()
    sys.exit(app.exec_())
