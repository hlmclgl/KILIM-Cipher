
import sys
from PyQt5.QtWidgets import QApplication
from app_ui import EncryptionApp 
import secrets 

MASTER_HMAC_KEY = secrets.token_bytes(32)


def main():
    app = QApplication(sys.argv)
    
    window = EncryptionApp(MASTER_HMAC_KEY) 
    
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()