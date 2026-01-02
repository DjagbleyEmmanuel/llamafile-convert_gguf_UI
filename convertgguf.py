import sys
import subprocess
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QComboBox, QTextEdit, 
                             QFileDialog, QMessageBox, QProgressBar, QHBoxLayout, 
                             QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette, QBrush

class ConversionWorker(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, gguf_path, base_llamafile, zipalign_path, destination):
        super().__init__()
        self.gguf_path = gguf_path
        self.base_llamafile = base_llamafile
        self.zipalign_path = zipalign_path
        self.destination = destination

    def run(self):
        try:
            self.log.emit(f"🚀 Starting conversion process...")
            
            # 1. Copy base llamafile to destination
            self.log.emit(f"📂 Copying base llamafile to {self.destination}...")
            shutil.copy2(self.base_llamafile, self.destination)
            self.progress.emit(30)

            # 2. Run zipalign
            # Command structure: zipalign -j0 <destination> <gguf> <args_file_if_any>
            # Note: We are embedding the GGUF into the llamafile
            self.log.emit(f"⚙️ Running zipalign to embed GGUF...")
            cmd = [self.zipalign_path, "-j0", self.destination, self.gguf_path]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.log.emit(f"  [zipalign] {line.strip()}")
            
            process.wait()
            if process.returncode != 0:
                self.finished.emit(False, f"zipalign failed with exit code {process.returncode}")
                return

            self.progress.emit(80)

            # 3. Make executable
            self.log.emit(f"🔓 Setting executable permissions...")
            os.chmod(self.destination, 0o755)
            
            self.progress.emit(100)
            self.log.emit(f"✅ Conversion successful! Saved to: {self.destination}")
            self.finished.emit(True, "Success")
        except Exception as e:
            self.finished.emit(False, str(e))

class LlamafileForge(QWidget):
    def __init__(self):
        super().__init__()
        self.app_version = "2.0.0"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Llamafile Forge')
        self.setMinimumSize(700, 600)
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # Glass Panel
        self.panel = QFrame()
        self.panel.setObjectName("glassPanel")
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(25, 25, 25, 25)
        self.panel_layout.setSpacing(15)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 10)
        self.panel.setGraphicsEffect(shadow)

        # Title
        self.title_label = QLabel("LLAMAFILE FORGE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #00FFC8; letter-spacing: 2px;")
        self.panel_layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle = QLabel("The Ultimate GGUF to Llamafile Tool")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("color: #AAAAAA; font-size: 14px; margin-bottom: 10px;")
        self.panel_layout.addWidget(self.subtitle)

        # Inputs
        self.gguf_input = self.create_input_pair("GGUF Model File:", "Browse GGUF", self.browse_gguf)
        self.base_input = self.create_input_pair("Base Llamafile:", "Browse Base", self.browse_base)
        self.zipalign_input = self.create_input_pair("Zipalign Binary:", "Browse Zip", self.browse_zipalign)
        self.dest_input = self.create_input_pair("Save Output As:", "Save Path", self.browse_dest)

        # Convert Button
        self.convert_button = QPushButton("BRING TO LIFE")
        self.convert_button.setObjectName("convertButton")
        self.convert_button.setFixedHeight(50)
        self.convert_button.clicked.connect(self.start_conversion)
        self.panel_layout.addWidget(self.convert_button)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.panel_layout.addWidget(self.progress_bar)

        # Output Log
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setPlaceholderText("Ready for conversion...")
        self.output_log.setObjectName("logArea")
        self.panel_layout.addWidget(self.output_log)

        # Footer Actions
        footer_layout = QHBoxLayout()
        self.about_btn = QPushButton("About")
        self.about_btn.setFixedWidth(100)
        self.about_btn.clicked.connect(self.show_about)
        footer_layout.addStretch()
        footer_layout.addWidget(self.about_btn)
        self.panel_layout.addLayout(footer_layout)

        self.main_layout.addWidget(self.panel)

        self.apply_styles()

    def create_input_pair(self, label_text, btn_text, slot):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #E0E0E0; font-weight: bold;")
        
        row = QHBoxLayout()
        edit = QLineEdit()
        edit.setPlaceholderText(f"Path to {label_text.lower()[:-1]}...")
        btn = QPushButton(btn_text)
        btn.setFixedWidth(120)
        btn.clicked.connect(slot)
        
        row.addWidget(edit)
        row.addWidget(btn)
        
        layout.addWidget(label)
        layout.addLayout(row)
        self.panel_layout.addLayout(layout)
        return edit

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0F111A;
            }
            #glassPanel {
                background-color: rgba(30, 34, 50, 200);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
            QLineEdit {
                background-color: rgba(0, 0, 0, 100);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border: 1px solid #00FFC8;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            #convertButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00FFC8, stop:1 #0088FF);
                color: #000;
                border: none;
                font-size: 16px;
                letter-spacing: 1px;
            }
            #convertButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #22FFD4, stop:1 #2299FF);
            }
            #logArea {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 8px;
                color: #A0FF90;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #00FFC8;
                border-radius: 4px;
            }
        """)

    def browse_gguf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select GGUF", "", "GGUF Files (*.gguf)")
        if path: self.gguf_input.setText(path)

    def browse_base(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Base Llamafile", "", "All Files (*)")
        if path: self.base_input.setText(path)

    def browse_zipalign(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Zipalign", "", "All Files (*)")
        if path: self.zipalign_input.setText(path)

    def browse_dest(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Llamafile", "", "Llamafile (*.llamafile)")
        if path: self.dest_input.setText(path)

    def start_conversion(self):
        gguf = self.gguf_input.text()
        base = self.base_input.text()
        zip_path = self.zipalign_input.text()
        dest = self.dest_input.text()

        if not all([gguf, base, zip_path, dest]):
            QMessageBox.warning(self, "Missing Fields", "Please populate all paths before proceeding.")
            return

        self.convert_button.setEnabled(False)
        self.output_log.clear()
        self.progress_bar.setValue(0)

        self.worker = ConversionWorker(gguf, base, zip_path, dest)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.log.connect(self.output_log.append)
        self.worker.finished.connect(self.conversion_done)
        self.worker.start()

    def conversion_done(self, success, message):
        self.convert_button.setEnabled(True)
        if success:
            QMessageBox.information(self, "Done", "Llamafile generated successfully!")
        else:
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{message}")

    def show_about(self):
        QMessageBox.about(self, "About Llamafile Forge", 
                         f"<h2>Llamafile Forge v{self.app_version}</h2>"
                         "<p>A professional utility for creating self-contained Llamafiles from GGUF models.</p>"
                         "<p><b>Created by Djagbley Emmanuel (Priderock)</b></p>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LlamafileForge()
    window.show()
    sys.exit(app.exec_())
