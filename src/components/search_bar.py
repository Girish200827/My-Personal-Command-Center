from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QKeyEvent
from config.config import Config
from services.database import Database


class SearchBar(QWidget):
    page_selected = Signal(str)

    def __init__(self, parent=None, pages=None):
        super().__init__(parent)

        self.pages = pages if pages else []

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("CURRENT ROOM NAME")

        self.search_input.setMinimumWidth(400)
        self.search_input.setFixedHeight(40)

        self.search_input.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.search_input.textChanged.connect(self.on_text_changed)
        self.search_input.installEventFilter(self)

        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #474747;
                border-radius: 30px;
                background-color: #252525;
                color: #474747;
                font-size: 14px;          
                }
            QLineEdit:focus {
                border: 2px solid #0081CF;
            }
            QLineEdit:hover {
                background-color: #5B5B5B;
                border: 2px solid #2A2A2A;
            }
            QLineEdit:focus:hover {
                border: 2px solid #0081CF;
                background-color: #2A2A2A;
            }
        """
        )

        self.dropdown = QListWidget(self)
        self.dropdown.setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
        )
        self.dropdown.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.dropdown.setStyleSheet(
            """
            QListWidget {
                border: 2px solid #0081CF;
                border-radius: 10px;
                background-color: #2A2A2A;
                color: #FFFFFF;
                font-size: 14px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #5B5B5B;
            }
            QListWidget::item:selected {
                background-color: #0081CF;
            }
        """
        )

        self.dropdown.setFixedHeight(400)
        self.dropdown.setMinimumHeight(150)
        self.dropdown.setMaximumHeight(250)
        self.dropdown.itemClicked.connect(self.on_item_selected)
        self.dropdown.hide()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.search_input)
        self.main_layout.addWidget(self.dropdown)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.center_placeholder()

    def center_placeholder(self):
        """Center the placeholder text"""
        # This is a workaround - we'll use alignment
        self.search_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def eventFilter(self, obj, event):
        """Filter events to handle Escape and Enter keys"""
        if obj == self.search_input:
            if event.type() == QEvent.Type.FocusIn:
                self.search_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.show_dropdown()
                return False
            elif event.type() == QEvent.Type.FocusOut:
                if not self.search_input.text():
                    self.search_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
                return False
            elif event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Escape or event.key() == Qt.Key.Key_Return:
                    self.search_input.clearFocus()
                    self.hide_dropdown()
                    return True
                elif event.key() == Qt.Key.Key_Down:
                    if self.dropdown.isVisible() and self.dropdown.count() > 0:
                        self.dropdown.setFocus()
                        self.dropdown.setCurrentRow(0)
                    return True
        return super().eventFilter(obj, event)

    def on_text_changed(self, text):
        """Handle text changes and filter dropdown"""
        self.filter_dropdown(text)

    def show_dropdown(self):
        """Show the dropdown with all pages"""
        self.populate_dropdown(self.pages)
        if self.dropdown.count() > 0:
            pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())
            pos.setY(pos.y() + 5)
            self.dropdown.move(pos)
            self.dropdown.show()
            self.dropdown.raise_()

    def hide_dropdown(self):
        """Hide the dropdown"""
        self.dropdown.hide()

    def populate_dropdown(self, items):
        """Populate dropdown with items"""
        self.dropdown.clear()
        for item in items:
            self.dropdown.addItem(item)

        if self.dropdown.count() > 0:
            item_height = self.dropdown.sizeHintForRow(0)
            total_height = min(item_height * self.dropdown.count() + 15, 250)
            self.dropdown.setFixedHeight(total_height)

    def filter_dropdown(self, text):
        """Filter dropdown items based on search text"""
        if not text:
            self.populate_dropdown(self.pages)
        else:
            filtered_pages = [
                page for page in self.pages if text.lower() in page.lower()
            ]
            self.populate_dropdown(filtered_pages)

        if self.dropdown.count() > 0 and self.search_input.hasFocus():
            pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())
            pos.setY(pos.y() + 5)
            self.dropdown.move(pos)
            self.dropdown.show()
        else:
            self.dropdown.hide()

    def on_item_selected(self, item):
        selected_text = item.text()
        self.search_input.setText(selected_text)
        self.hide_dropdown()
        self.search_input.clearFocus()
        self.page_selected.emit(selected_text)

    def set_pages(self, pages):
        """Update the list of available pages"""
        self.pages = pages

    def hideEvent(self, event):
        self.hide_dropdown()
        super().hideEvent(event)
