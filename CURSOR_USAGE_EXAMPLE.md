# Dynamic Circle Cursor Usage Guide

## Overview
The updated `CustomCursor` class now supports dynamic color selection for circle cursors. You can easily change cursor colors when hovering over buttons or other UI elements.

## Available Colors
Colors are configured in `src/config/config.py`:
- `black`
- `white`
- `green`
- `blue`
- `purple`
- `red`

## Usage Examples

### 1. Initialize with a Specific Color
```python
from src.components.circular_cursor import CustomCursor

# Apply black cursor to a widget on initialization
CustomCursor(my_button, color='black')

# Apply green cursor to a widget on initialization
CustomCursor(my_widget, color='green')
```

### 2. Change Cursor on Button Hover
```python
from PySide6.QtWidgets import QPushButton
from src.components.circular_cursor import CustomCursor

class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial cursor (optional)
        CustomCursor(self, color='blue')
    
    def enterEvent(self, event):
        # Change cursor to green when hovering
        CustomCursor.set_cursor(self, 'green')
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        # Change cursor back to blue when leaving
        CustomCursor.set_cursor(self, 'blue')
        super().leaveEvent(event)
```

### 3. Change Cursor on Button Click
```python
from PySide6.QtWidgets import QPushButton
from src.components.circular_cursor import CustomCursor

button = QPushButton("Change Cursor Color")

def on_button_clicked():
    CustomCursor.set_cursor(button, 'red')
    print("Cursor changed to red!")

button.clicked.connect(on_button_clicked)
```

### 4. Create a Cursor Color Selector
```python
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget
from src.components.circular_cursor import CustomCursor

class CursorColorSelector(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        # Get available colors from config
        colors = CustomCursor.get_available_colors()
        
        # Create a button for each color
        for color in colors:
            button = QPushButton(color.capitalize())
            button.clicked.connect(
                lambda checked, c=color: CustomCursor.set_cursor(self, c)
            )
            layout.addWidget(button)
        
        self.setLayout(layout)
```

### 5. Dynamic Cursor in Response to State
```python
from PySide6.QtWidgets import QMainWindow
from src.components.circular_cursor import CustomCursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_saving = False
        CustomCursor(self, 'black')
    
    def save_data(self):
        # Show red cursor during save
        CustomCursor.set_cursor(self, 'red')
        self.is_saving = True
        
        # ... save logic ...
        
        # Restore cursor when done
        CustomCursor.set_cursor(self, 'black')
        self.is_saving = False
```

## Key Methods

### `CustomCursor(parent_widget, color='black')`
Initialize the custom cursor on a widget.
- **parent_widget**: The widget to apply cursor to
- **color**: Color name (default: 'black')

### `CustomCursor.set_cursor(parent_widget, color='black')`
Change cursor for a widget to a specific color (class method).
- **parent_widget**: The widget to apply cursor to
- **color**: Color name (default: 'black')

### `CustomCursor.get_available_colors()`
Get list of available colors from config.
- **Returns**: List of color names

## Notes
- Invalid color names will default to 'black' with a warning message
- Cursor size is fixed at 18x18 pixels (can be modified in `set_cursor()` method)
- Colors must match the filenames in `src/resources/assets/circle_cursor/`
