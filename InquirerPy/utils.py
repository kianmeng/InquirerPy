"""Module contains shared utility functions."""

import math
import os
import shutil
from typing import Dict, Optional, Tuple, Union

from InquirerPy.exceptions import InvalidArgument


def get_style() -> Dict[str, str]:
    """Get default style if style parameter is missing.

    Reads the ENV variable first before apply default one dark theme.

    :return: style dictionary ready to be consumed by `Style.from_dict`
    :rtype: Dict[str, str]
    """
    return {
        "questionmark": os.getenv("INQUIRERPY_STYLE_QUESTIONMARK", "#e5c07b"),
        "answer": os.getenv("INQUIRERPY_STYLE_ANSWER", "#61afef"),
        "input": os.getenv("INQUIRERPY_STYLE_INPUT", "#98c379"),
        "question": os.getenv("INQUIRERPY_STYLE_QUESTION", ""),
        "instruction": os.getenv("INQUIRERPY_STYLE_INSTRUCTION", ""),
        "pointer": os.getenv("INQUIRERPY_STYLE_POINTER", "#61afef"),
        "checkbox": os.getenv("INQUIRERPY_STYLE_CHECKBOX", "#98c379"),
        "separator": os.getenv("INQUIRERPY_STYLE_SEPARATOR", ""),
        "skipped": os.getenv("INQUIRERPY_STYLE_SKIPPED", "#5c6370"),
        "fuzzy_prompt": os.getenv("INQUIRERPY_STYLE_FUZZY_PROMPT", "#c678dd"),
        "fuzzy_info": os.getenv("INQUIRERPY_STYLE_FUZZY_INFO", "#98c379"),
        "fuzzy_marker": os.getenv("INQUIRERPY_STYLE_FUZZY_MARKER", "#e5c07b"),
        "fuzzy_border": os.getenv("INQUIRERPY_STYLE_FUZZY_BORDER", "#4b5263"),
        "fuzzy_match": os.getenv("INQUIRERPY_STYLE_FUZZY_MATCH", "#c678dd"),
    }


def calculate_height(
    height: Optional[Union[int, str]],
    max_height: Optional[Union[int, str]],
    offset: int = 1,
) -> Tuple[Optional[int], int]:
    """Calculate the height and max_height for the choice window.

    Allowed height values:
    * "60%" - percentage height in str
    * 20 - exact line height in int
    """
    try:
        _, term_lines = shutil.get_terminal_size()
        term_lines = term_lines
        if not height:
            dimmension_height = None
        else:
            if isinstance(height, str):
                height = height.replace("%", "")
                height = int(height)
                dimmension_height = math.floor(term_lines * (height / 100)) - offset
            else:
                dimmension_height = height

        if not max_height:
            dimmension_max_height = term_lines - offset
        else:
            if isinstance(max_height, str):
                max_height = max_height.replace("%", "")
                max_height = int(max_height)
                dimmension_max_height = (
                    math.floor(term_lines * (max_height / 100)) - offset
                )
            else:
                dimmension_max_height = max_height
        if dimmension_height and dimmension_height > dimmension_max_height:
            dimmension_height = dimmension_max_height
        if dimmension_height and dimmension_height < 0:
            dimmension_height = 1
        return dimmension_height, dimmension_max_height

    except ValueError:
        raise InvalidArgument(
            "prompt height needs to be either an int or str representing height percentage."
        )