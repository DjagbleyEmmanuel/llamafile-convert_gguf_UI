import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTextEdit, QFileDialog, QMessageBox, QScrollArea
from PyQt5.QtCore import Qt
import subprocess
import os

class ConversionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('GGUF to LLAMAFILE Converter')

        self.file_label = QLabel('GGUF File Path or URL:')
        self.file_edit = QLineEdit()
        self.browse_button = QPushButton('Browse')
        self.browse_button.setObjectName('browseButton')
        
        self.zipalign_label = QLabel('Zipalign File Path:')
        self.zipalign_edit = QLineEdit()
        self.zipalign_browse_button = QPushButton('Browse')
        self.zipalign_browse_button.setObjectName('browseButton')
        
        self.mode_label = QLabel('Conversion Mode:')
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItems(['cli', 'server', 'both'])
        
        self.convert_button = QPushButton('Convert')
        self.convert_button.setObjectName('convertButton')
        self.output_text = QTextEdit()

        self.about_button = QPushButton('About')
        self.about_button.setObjectName('aboutButton')
        self.about_text = QTextEdit()
        self.about_text.setReadOnly(True)
        self.about_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.about_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.about_text.setMaximumHeight(200)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.browse_button)
        
        layout.addWidget(self.zipalign_label)
        layout.addWidget(self.zipalign_edit)
        layout.addWidget(self.zipalign_browse_button)
        
        layout.addWidget(self.mode_label)
        layout.addWidget(self.mode_combobox)
        
        layout.addWidget(self.convert_button)
        layout.addWidget(self.output_text)

        layout.addWidget(self.about_button)
        layout.addWidget(self.about_text)

        self.browse_button.clicked.connect(self.browse_gguf_file)
        self.zipalign_browse_button.clicked.connect(self.browse_zipalign_file)
        self.convert_button.clicked.connect(self.convert)
        self.about_button.clicked.connect(self.show_about)

        self.setLayout(layout)

        # Apply custom style sheet
        self.setStyleSheet('''
            QWidget {
                background-color: #262626;
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background-color: #393939;
                border: 2px solid #62B800;
                border-radius: 5px;
                padding: 5px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #62B800;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QPushButton#convertButton {
                background-color: #32CD32;
            }
            QPushButton#aboutButton {
                background-color: #008CBA;
            }
        ''')

        # Set app version
        self.app_version = "1.0.0"

    def browse_gguf_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select GGUF File', '', 'All Files (*);;GGUF Files (*.gguf)')
        if file_path:
            self.file_edit.setText(file_path)

    def browse_zipalign_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Zipalign File', '', 'Executable Files (*.exe);;All Files (*)')
        if file_path:
            self.zipalign_edit.setText(file_path)

    def convert(self):
        gguf_file_path = self.file_edit.text()
        zipalign_file_path = self.zipalign_edit.text()
        mode = self.mode_combobox.currentText()

        try:
            self.output_text.clear()
            self.output_text.append(f"Converting {gguf_file_path} to llamafile with mode: {mode}\n")

            # Replace this with your conversion logic
            # For example:
            # subprocess.run(['your_conversion_command', gguf_file_path, zipalign_file_path, mode], capture_output=True, text=True)
            # Or any other conversion logic you have
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")

    def show_about(self):
        about_text = f"""
        GGUF to LLAMAFILE Converter

        Version: {self.app_version}

        This application allows you to convert GGUF files to LLAMAFILE format.
        Created by Priderock.
        """
        self.about_text.setText(about_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConversionApp()
    window.show()
    sys.exit(app.exec_())
