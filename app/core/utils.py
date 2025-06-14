import logging

logger = logging.getLogger("uvicorn.debug")


def qr(type, name, service, secret):
    return f"otpauth://{type}/{name}@{service}?secret={secret}"
