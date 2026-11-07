import logging
import os

logger = logging.getLogger("provider")


def primary_provider(question):
    mode = os.getenv("PRIMARY_MODE", "ok")

    if mode == "error":
        raise ConnectionError("Primary unavailable")

    if mode == "timeout":
        raise TimeoutError("Primary timed out")

    return f"Primary answer for: {question}"


def secondary_provider(question):
    return f"Fallback answer for: {question}"


def generate_answer(question):
    try:
        return {"answer": primary_provider(question), "provider": "primary"}

    except (ConnectionError, TimeoutError) as error:
        logger.warning("fallback_used: %s", type(error).__name__)

        return {"answer": secondary_provider(question), "provider": "secondary"}
