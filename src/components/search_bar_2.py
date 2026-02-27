from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QIcon
from .circular_cursor import CustomCursor


class SearchOverlay(QWidget):
    """Overlay widget that appears when search button is clicked"""

    page_selected = Signal(str)

    def __init__(self, parent=None, pages=None, search_btn=None):
        super().__init__(parent)
        self.pages = pages if pages else []

        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.search_btn = search_btn

        CustomCursor(self, color="blue")

        # Main container
        container = QFrame(self)
        container.setStyleSheet(
            """
            QFrame {
                background-color: #222222;
                border: 1px solid #3C3C3C;
                border-radius: 6px;
            }
        """
        )

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search pages by name")
        self.search_input.setFixedHeight(26)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #474747;
                border-radius: 5px;
                background-color: #2A2A2A;
                color: #FFFFFF;
                font-size: 13px;
                padding-left: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0081CF;
            }
        """
        )
        self.search_input.textChanged.connect(self.filter_pages)
        self.search_input.installEventFilter(self)

        # results list
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(
            """

            QListWidget {
                background-color: #222222;
                color: #CCCCCC;
                border: none;
                border-radius: 10px;
                outline: none;
                padding-right: 5px;
                font-size: 11px;   
                margin: 0px; 
            }
                                        
            QListWidget::item {
                padding: 0px 10px;
            }
            
            QListWidget::item:selected {
                background-color: #04395E;
                color: #FFFFFF;
            }

            QListWidget::item:selected:hover {
                background-color: #04395E;
            }
            
            QListWidget::item:hover {
                background-color: #2A2A2A;
            }
        """
        )
        self.list_widget.setSpacing(1)
        self.list_widget.setMaximumHeight(320)
        self.list_widget.setMinimumHeight(120)

        self.list_widget.itemClicked.connect(
            lambda item: self.page_selected.emit(item.text())
        )

        # Scroll area for page buttons
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #2A2A2A;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #474747;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #0081CF;
            }
        """
        )
        scroll.setWidget(self.list_widget)

        # Layout for container
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(self.search_input)
        container_layout.addWidget(scroll)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setSpacing(4)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Populate pages
        self.populate_pages()

        # Set size
        self.setFixedSize(400, 500)

    def closeEvent(self, event):
        if self.search_btn:
            self.search_btn.show()
        super().closeEvent(event)

    def populate_pages(self):
        self.list_widget.clear()
        for page in self.pages:
            item = QListWidgetItem(page)
            self.list_widget.addItem(item)

    def filter_pages(self, text):
        text = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(text not in item.text().lower())

    def on_page_selected(self, page):
        """Emit signal and close overlay"""
        self.page_selected.emit(page)
        self.close()

    def showEvent(self, event):
        """Focus search input when overlay is shown"""
        super().showEvent(event)
        self.search_input.setFocus()
        self.search_input.clear()


class SearchBar(QWidget):
    page_selected = Signal(str)

    def __init__(self, parent=None, pages=None):
        super().__init__(parent)
        self.pages = pages if pages else []
        self.overlay = None

        # Search button
        self.search_btn = QPushButton("Command Center")
        self.search_btn.setFixedHeight(26)
        self.search_btn.setMinimumWidth(450)
        self.search_btn.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.search_btn.clicked.connect(self.on_search_btn_click)

        self.search_btn.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #757575;
                border-radius: 5px;
                background-color: #252525;
                color: #E0E0E0;
                font-size: 13px;
                padding-left: 15px;
                padding-right: 15px;
            }
            QPushButton:hover {
                background-color: #2A2A2A;
                border: 1px solid #757575;
            }
            QPushButton:pressed {
                background-color: #0081CF;
            }
        """
        )

        # Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.search_btn)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def on_search_btn_click(self):
        """Show the search overlay"""

        if self.search_btn.isVisible():
            self.search_btn.hide()

        if not self.overlay:
            self.overlay = SearchOverlay(
                self.window(), self.pages, search_btn=self.search_btn
            )
            self.overlay.search_input.setFocus()
            self.overlay.page_selected.connect(self.page_selected.emit)

        # Position the overlay
        button_rect = self.search_btn.rect()
        global_pos = self.search_btn.mapToGlobal(button_rect.topLeft())

        overlay_x = (
            global_pos.x() - (self.overlay.width() - self.search_btn.width()) // 2
        )
        overlay_y = (global_pos.y() - self.search_btn.height() // 2) + 12

        # overlay_x = global_pos.x() - self.overlay.width() // 2
        # overlay_y = global_pos.y() - self.overlay.height() // 2

        self.overlay.move(overlay_x, overlay_y)

        self.overlay.show()
        self.overlay.raise_()

    def set_pages(self, pages):
        """Update the list of pages"""
        self.pages = pages
        if self.overlay:
            self.overlay.pages = pages
            self.overlay.populate_pages()
