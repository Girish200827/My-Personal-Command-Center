from pathlib import Path


class Config:
    APP_NAME = "My Personal Command Center"
    VERSION = "1.0.0"

    BASE_DIR = Path(__file__).parent.parent  # Go up to src/ directory

    PAGES = ["War Room", "Calendar", "Outmail", "Project", "Settings"]

    RESOURCES_DIR = BASE_DIR / "resources"
    STYLES_DIR = RESOURCES_DIR / "styles"
    ICONS_DIR = RESOURCES_DIR / "icons"
    BACKGROUND_DIR = RESOURCES_DIR / "assets/background"

    BACKGROUNDS = {
        "concrete_bg": BACKGROUND_DIR / "abstract_black_distressed_texture.png",
        "blackboard_bg": BACKGROUND_DIR / "blackboard_bg.png",
        "empty_jar_bg": BACKGROUND_DIR / "empty_jar_background.png",
        "ep_jar_bg": BACKGROUND_DIR / "ep-jar-trans-bg.png",
    }

    DATA_DIR = Path.home() / ".mypccapp"
    DATABASE_PATH = DATA_DIR / "tasks.db"

    DEFAULT_WINDOW_WIDTH = 1200
    DEFAULT_WINDOW_HEIGHT = 600
    MIN_WINDOW_WIDTH = 800
    MIN_WINDOW_HEIGHT = 600
    MAX_WINDOW_WIDTH = 32767
    MAX_WINDOW_HEIGHT = 32767

    USE_CUSTOM_TITLEBAR = True

    TITLEBAR_HEIGHT = 40
    AIM_BOX_HEIGHT = 60

    TASK_CATEGORIES = ["Big Rocks", "Pebbles", "Sand"]

    COLORS = {"primary": "#3498db", "secondary": "#2ecc71", "danger": "#e74c3c"}

    ENABLE_CUSTOM_CURSOR = ["black", "white", "green", "blue", "purple", "red"]
    CIRCLE_CURSOR_PATH = "src/resources/assets/circle_cursor"

    ENABLE_ANIMATION = True
    ENABLE_SOUND_EFFECTS = False
    DEBUG_MODE = False

    DB_CONNECTION_TIMEOUT = 30
    AUTO_SAVE_INTERVAL = 60

    MAX_TASK_TITLE_LENGTH = 200
    MAX_TASK_DESCRIPTION_LENGTH = 2000
    MAX_TASKS_PER_CATEGORY = 50

    SHORTCUTS = {"new_task": "Ctrl+N", "quit": "Ctrl+Q", "reset_window": "Ctrl+R"}

    @classmethod
    def ensure_directories(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_stylesheet_path(cls):
        return cls.STYLES_DIR / "main.qss"
