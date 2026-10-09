import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QListWidget, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtCore import QTimer, Qt

class ClipboardManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Clipboard Manager")
        self.resize(500, 400)
        
        self.clipboard = QApplication.clipboard()
        self.last_text = ""
        
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Search bar
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search clipboard history...")
        self.search_box.textChanged.connect(self.filter_history)
        layout.addWidget(self.search_box)

        # History List
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_selected)
        layout.addWidget(self.list_widget)

        # Status and Controls
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("Monitoring clipboard...")
        bottom_layout.addWidget(self.status_label)
        
        bottom_layout.addStretch()
        
        self.clear_btn = QPushButton("Clear History")
        self.clear_btn.clicked.connect(self.clear_history)
        bottom_layout.addWidget(self.clear_btn)
        
        layout.addLayout(bottom_layout)

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_clipboard)
        self.timer.start(500)

    def check_clipboard(self):
        current_text = self.clipboard.text()
        if current_text and current_text != self.last_text:
            self.last_text = current_text
            self.add_item(current_text)

    def add_item(self, text):
        # Avoid exact duplicates at the top
        items = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        if text in items:
            for i in range(self.list_widget.count()):
                if self.list_widget.item(i).text() == text:
                    self.list_widget.takeItem(i)
                    break
        self.list_widget.insertItem(0, text)
        self.status_label.setText(f"Captured at {QTimer.remainingTime(self.timer) if hasattr(self, 'timer') else ''}")

    def filter_history(self, query):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(query.lower() not in item.text().lower())

    def copy_selected(self, item):
        self.clipboard.setText(item.text())
        self.status_label.setText("Copied to clipboard!")

    def clear_history(self):
        self.list_widget.clear()
        self.last_text = ""
        self.status_label.setText("History cleared.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = ClipboardManager()
    manager.show()
    sys.exit(app.exec_()
)
