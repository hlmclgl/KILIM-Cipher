from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QMenuBar, QMenu, QAction
from PyQt5.QtGui import QFont, QIcon
from help_dialog import HelpDialog
from encryption_manager import EncryptionManager


class EncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.encryption_manager = EncryptionManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Şifreleme Uygulaması")
        self.setGeometry(100, 100, 800, 600)
        self.createMenuBar()  
        self.setWindowIcon(QIcon('unlock.png'))  

        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #3C3C3C;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #5C5C5C;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """)

        layout = QVBoxLayout()

        input_label = QLabel("Mesaj Giriniz:")
        self.input_text = QTextEdit()

        output_label = QLabel("Şifrelenmiş Metin:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        button_layout = QHBoxLayout()
        encrypt_button = QPushButton("Şifrele")
        encrypt_button.clicked.connect(self.encrypt_message)
        decrypt_button = QPushButton("Çöz")
        decrypt_button.clicked.connect(self.decrypt_message)

        button_layout.addWidget(encrypt_button)
        button_layout.addWidget(decrypt_button)

        encrypt_button.setFixedSize(200, 34)
        encrypt_button.setStyleSheet("background-color: #4CAF50; color: black;")

        decrypt_button.setFixedSize(200, 34) 
        decrypt_button.setStyleSheet("background-color: #FF9800; color: black;") 

        layout.addWidget(input_label)
        layout.addWidget(self.input_text)
        layout.addLayout(button_layout)
        layout.addWidget(output_label)
        layout.addWidget(self.output_text)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.center()

    def createMenuBar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu('Yardım')

        help_action = QAction('Kullanıcı Kılavuzu', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def encrypt_message(self):
        plain_text = self.input_text.toPlainText().strip()
        if not plain_text:
            QMessageBox.warning(self, "Hata", "Lütfen şifrelenecek mesajı giriniz.")
            return
        try:
            cipher_text = self.encryption_manager.encrypt(plain_text)
            self.output_text.setPlainText(cipher_text)
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def decrypt_message(self):
        cipher_text = self.input_text.toPlainText().strip()
        if not cipher_text:
            QMessageBox.warning(self, "Hata", "Lütfen çözülecek mesajı giriniz.")
            return
        try:
            plain_text = self.encryption_manager.decrypt(cipher_text)
            self.output_text.setPlainText(plain_text)
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def center(self):
        screen = self.screen().geometry()
        window_geometry = self.frameGeometry()
        self.move(
            (screen.width() - window_geometry.width()) // 2,
            (screen.height() - window_geometry.height()) // 2
        )
