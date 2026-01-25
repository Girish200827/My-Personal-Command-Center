import uuid
from datetime import datetime


def generate_task_id() -> str:
    return f"task_{uuid.uuid4().hex[:12]}"


def generate_timestamp_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = uuid.uuid4().hex[:6]
    return f"{timestamp}_{random_part}"
