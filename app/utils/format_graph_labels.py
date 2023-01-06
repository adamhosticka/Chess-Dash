"""Format graph labels"""


def format_labels(to_format: list) -> dict:
    return {label: label.replace("_", " ") for label in to_format}
