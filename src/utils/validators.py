import re
from datetime import datetime
from typing import Tuple

def validate_task_title(title: str) -> Tuple[bool, str]:

    if not title or not title.strip():
        return False, 'Title cannot be empty'
    
    if len(title) > 200:
        return False, 'Title must be 200 characters or less'
    
    return True, ''

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_date(date_str: str) -> Tuple[bool, datetime]:
    try:
        dt = datetime.fromisoformat(date_str)
        return True, dt
    except ValueError:
        return False, None