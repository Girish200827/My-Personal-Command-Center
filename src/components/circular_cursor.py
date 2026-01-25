from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QCursor, QPixmap
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.config import Config


class CustomCursor:
    # Mapping of color names to cursor filenames
    COLOR_MAPPING = {
        "black": "circle_cursor_Black_3.png",
        "white": "circle_cursor_White.png",
        "green": "circle_cursor_Green.png",
        "blue": "circle_cursor_Blue.png",
        "purple": "circle_cursor_Purple.png",
        "red": "circle_cursor_Red.png",
    }

    def __init__(self, parent_widget, color: str = "black"):
        """
        Initialize custom cursor with specified color.

        Args:
            parent_widget: The widget to apply the cursor to
            color: Color name from Config.ENABLE_CUSTOM_CURSOR list (default: 'black')
        """
        if hasattr(Config, "ENABLE_CUSTOM_CURSOR") and Config.ENABLE_CUSTOM_CURSOR:
            self.set_cursor(parent_widget, color)

    @classmethod
    def set_cursor(cls, parent_widget, color: str = "black"):
        """
        Set cursor for a widget with the specified color.

        Args:
            parent_widget: The widget to apply the cursor to
            color: Color name from Config.ENABLE_CUSTOM_CURSOR list
        """
        if (
            not hasattr(Config, "ENABLE_CUSTOM_CURSOR")
            or not Config.ENABLE_CUSTOM_CURSOR
        ):
            return

        # Validate color
        color = color.lower()
        if color not in cls.COLOR_MAPPING:
            print(f"Warning: Color '{color}' not found. Using 'black' instead.")
            color = "black"

        # Get the cursor filename for the color
        cursor_filename = cls.COLOR_MAPPING[color]

        # Build the full resource path
        resource_path = (
            Path(__file__).parent.parent
            / f"resources/assets/circle_cursor/{cursor_filename}"
        ).as_posix()

        # Load and apply cursor
        pixmap_circle_cursor = QPixmap(resource_path).scaled(18, 18)
        cursor = QCursor(pixmap_circle_cursor, -1, -1)
        parent_widget.setCursor(cursor)

    @staticmethod
    def get_available_colors():
        """
        Get list of available cursor colors from config.

        Returns:
            List of color names
        """
        if hasattr(Config, "ENABLE_CUSTOM_CURSOR"):
            return Config.ENABLE_CUSTOM_CURSOR
        return []
