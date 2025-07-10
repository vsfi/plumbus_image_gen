import logging
import json
import os
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present, excluding system fields
        excluded_fields = {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename',
            'module', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated',
            'thread', 'threadName', 'processName', 'process', 'getMessage', 'exc_info',
            'exc_text', 'stack_info', 'taskName'
        }
        
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in excluded_fields:
                    log_entry[key] = value
        
        return json.dumps(log_entry, ensure_ascii=False)


class CustomFormatter(logging.Formatter):
    """Colored formatter for development"""
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "[%(asctime)s;%(levelname)s:%(name)s:%(lineno)d)] - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: green + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name):
    """Get logger with JSON or colored formatting based on environment"""
    logging.getLogger().handlers.clear()
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    
    # Use JSON formatting if LOG_FORMAT is set to json
    log_format = os.getenv("LOG_FORMAT", "text").lower()
    if log_format == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(CustomFormatter())

    log.addHandler(handler)
    return log


