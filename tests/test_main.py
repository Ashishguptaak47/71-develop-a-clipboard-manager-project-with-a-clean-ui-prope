import sys
import unittest
from PyQt5.QtWidgets import QApplication
from main import ClipboardManager

app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()

class TestClipboardManager(unittest.TestCase):
    def setUp(self):
        self.manager = ClipboardManager()

    def tearDown(self):
        self.manager.close()

    def test_initial_state(self):
        self.assertEqual(self.manager.list_widget.count(), 0)
        self.assertEqual(self.manager.search_box.text(), "")

    def test_add_item(self):
        self.manager.add_item("Test Clip 1")
        self.assertEqual(self.manager.list_widget.count(), 1)
        self.assertEqual(self.manager.list_widget.item(0).text(), "Test Clip 1")

    def test_duplicate_item_moves_to_top(self):
        self.manager.add_item("Clip A")
        self.manager.add_item("Clip B")
        self.manager.add_item("Clip A")
        self.assertEqual(self.manager.list_widget.count(), 2)
        self.assertEqual(self.manager.list_widget.item(0).text(), "Clip A")
        self.assertEqual(self.manager.list_widget.item(1).text(), "Clip B")

if __name__ == "__main__":
    unittest.main()
