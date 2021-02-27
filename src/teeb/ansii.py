# -*- coding: utf-8 -*-
from enum import Enum


class ANSIIColor(Enum):
    """ANSII text color codes
    see: https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    BLACK = "30"
    DARK_RED = "31"
    DARK_GREEN = "32"
    RED = "33"
    DARK_BLUE = "34"
    PURPLE = "35"
    BLUE = "36"
    GRAY = "37"
    BRIGHT_BLACK = "1;30"
    BRIGHT_RED = "1;31"
    BRIGHT_GREEN = "1;32"
    BRIGHT_YELLOW = "1;33"
    BRIGHT_BLUE = "1;34"
    BRIGHT_PURPLE = "1;35"
    BRIGHT_CYAN = "1;36"
    BRIGHT_GRAY = "1;37"


class ANSIIStyle:
    """Generate ANSII text style & color escape start & end codes
    see: https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    start = ""
    end = ""

    def __init__(
        self,
        *,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        strikethrough: bool = False,
        color: ANSIIColor = None,
    ):
        tmp = []
        if bold:
            tmp.append("1")
        if italic:
            tmp.append("3")
        if underline:
            tmp.append("4")
        if strikethrough:
            tmp.append("9")
        if color:
            tmp.append(color.value)
        if tmp:
            self.start = f"\033[{';'.join(tmp)}m"
            self.end = "\033[0m"
