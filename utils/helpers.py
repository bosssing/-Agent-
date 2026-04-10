import time
from functools import wraps
from typing import Dict, Any, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_response(success: bool, data: Any = None, message: str = "") -> Dict[str, Any]:
    return {
        "success": success,
        "data": data,
        "message": message
    }


def log_execution_time(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.2f} seconds: {str(e)}")
            raise
    return wrapper


def truncate_text(text: str, max_length: int = 1000) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
