from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kullanıcı Kılavuzu")
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 20px;
                font-family: "Times New Roman";
            }
        """)
        layout = QVBoxLayout()
        help_text = """
        Şifreleme İçin :
        1. 'Mesaj Giriniz' kısmına şifrelenecek metni girin.
        2. 'Şifrele' butonuna tıklayarak metni şifreleyin.
        
        Şifre Çözme İçin:
        1. 'Mesaj Giriniz' kısmına çözülecek metni girin.
        2. 'Çöz' butonuna tıklayarak şifreli metni çözün.
        
        *Şifreleme ve çözme işlemleri 512 bitlik anahtarlarla yapılır.
        """
        help_label = QLabel(help_text, self)
        layout.addWidget(help_label)
        self.setLayout(layout)
