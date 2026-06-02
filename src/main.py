"""Application entry point"""
import sys
from PyQt5.QtWidgets import QApplication
from src.window import OliverWindow


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Create main window
    window = OliverWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
