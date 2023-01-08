"""Format graph labels"""


def format_labels(to_format: list) -> dict:
    """Create label dict for graphs from list of names by replacing underscore with a space.

    :param: list to_format: List to create label dict from.
    :return: Labels.
    :rtype: dict.
    """
    return {label: label.replace("_", " ") for label in to_format}
