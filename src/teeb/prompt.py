# -*- coding: utf-8 -*-
from teeb.ansii import (
    ANSIIColor,
    ANSIIStyle,
)


def prompt(question: str, options: list) -> str:
    """Print colorful prompt.

    returns: a lower case decision option key.
    """
    default_options = {
        "d": {"name": "Delete", "style": ANSIIStyle(bold=True, color=ANSIIColor.RED)},
        "n": {
            "name": "No",
            "style": ANSIIStyle(bold=True, color=ANSIIColor.BRIGHT_BLUE),
        },
        "p": {
            "name": "Process",
            "style": ANSIIStyle(bold=True, color=ANSIIColor.BRIGHT_RED),
        },
        "q": {"name": "Quit", "style": ANSIIStyle(bold=True, color=ANSIIColor.GRAY)},
        "s": {
            "name": "Skip",
            "style": ANSIIStyle(bold=True, color=ANSIIColor.BRIGHT_YELLOW),
        },
        "y": {
            "name": "Yes",
            "style": ANSIIStyle(bold=True, color=ANSIIColor.BRIGHT_GREEN),
        },
        "0": {
            "name": "Zero",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_CYAN),
        },
        "1": {
            "name": "One",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_PURPLE),
        },
        "2": {
            "name": "Two",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_RED),
        },
        "3": {
            "name": "Three",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_YELLOW),
        },
        "4": {
            "name": "Four",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_GREEN),
        },
        "5": {
            "name": "Five",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_GRAY),
        },
        "6": {
            "name": "Six",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_BLUE),
        },
        "7": {
            "name": "Seven",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_BLACK),
        },
        "8": {
            "name": "Eight",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_CYAN),
        },
        "9": {
            "name": "Nine",
            "style": ANSIIStyle(bold=True, italic=True, color=ANSIIColor.BRIGHT_PURPLE),
        },
    }
    assert options, "Empty prompt options list. Please provide at least one!"

    result = None
    matching_options = {
        option: default_options[option]
        for option in options
        if option in default_options
    }
    formatted_options = " / ".join(
        f"{props['style'].start}{key} ({props['name']}){props['style'].end}"
        for key, props in matching_options.items()
    )
    while result not in matching_options:
        result = input(f"{question} {formatted_options}: ").lower()

    return result
