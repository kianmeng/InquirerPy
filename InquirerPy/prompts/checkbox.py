"""Module contains checkbox prompt."""

from typing import Any, Callable, Dict, List, Literal, Tuple, Union

from prompt_toolkit.validation import Validator

from InquirerPy.base import BaseComplexPrompt, InquirerPyUIControl
from InquirerPy.enum import (
    INQUIRERPY_EMPTY_HEX_SEQUENCE,
    INQUIRERPY_FILL_HEX_SEQUENCE,
    INQUIRERPY_POINTER_SEQUENCE,
)
from InquirerPy.separator import Separator


class InquirerPyCheckboxControl(InquirerPyUIControl):
    """A UIControl class intended to be used by `prompt_toolkit` window.

    Used to dynamically update the content and indicate the current user selection

    :param choices: a list of choices to display
    :type choices: List[Union[Any, Dict[str, Any]]]
    :param default: default value for selection
    :type default: Any
    :param pointer: the pointer to display, indicating current line, default is unicode ">"
    :type pointer: str
    :param enabled_symbol: the qmark to indicate selected choices
    :type enabled_symbol: str
    :param disabled_symbol: the qmark to indicate not selected choices
    :type disabled_symbol: str
    """

    def __init__(
        self,
        choices: List[Union[Any, Dict[str, Any]]],
        default: Any = None,
        pointer: str = INQUIRERPY_POINTER_SEQUENCE,
        enabled_symbol: str = INQUIRERPY_FILL_HEX_SEQUENCE,
        disabled_symbol: str = INQUIRERPY_EMPTY_HEX_SEQUENCE,
    ) -> None:
        """Initialise required attributes and call base class."""
        self.pointer = "%s " % pointer
        self.enabled_symbol = enabled_symbol
        self.disabled_symbol = disabled_symbol
        super().__init__(choices, default)

        for raw_choice, choice in zip(choices, self.choices):
            if isinstance(raw_choice, dict):
                choice["enabled"] = raw_choice.get("enabled", False)
            else:
                choice["enabled"] = False

    def _get_hover_text(self, choice) -> List[Tuple[str, str]]:
        display_choices = []
        display_choices.append(("class:pointer", self.pointer))
        if not isinstance(choice["value"], Separator):
            display_choices.append(
                (
                    "class:checkbox",
                    "%s " % self.enabled_symbol
                    if choice["enabled"]
                    else "%s " % self.disabled_symbol,
                )
            )
        display_choices.append(("[SetCursorPosition]", ""))
        display_choices.append(("class:pointer", choice["name"]))
        return display_choices

    def _get_normal_text(self, choice) -> List[Tuple[str, str]]:
        display_choices = []
        display_choices.append(("", len(self.pointer) * " "))
        if not isinstance(choice["value"], Separator):
            display_choices.append(
                (
                    "class:checkbox",
                    "%s " % self.enabled_symbol
                    if choice["enabled"]
                    else "%s " % self.disabled_symbol,
                )
            )
            display_choices.append(("", choice["name"]))
        else:
            display_choices.append(("class:separator", choice["name"]))
        return display_choices


class CheckboxPrompt(BaseComplexPrompt):
    """A wrapper class around `prompt_toolkit` Application to create a checkbox prompt.

    :param message: message to display
    :type message: str
    :param choices: list of choices to display
    :type choices: List[Union[Any, Dict[str, Any]]]
    :param default: default value
    :type default: Any
    :param style: a dictionary of style
    :type style: Dict[str, str]
    :param editing_mode: editing_mode of the prompt
    :type editing_mode: Literal["emacs", "default", "vim"]
    :param qmark: question qmark to display
    :type qmark: str
    :param pointer: the pointer qmark to display
    :type pointer: str
    :param enabled_symbol: qmark indicating enabled box
    :type enabled_symbol: str
    :param disabled_symbol: qmark indicating not selected qmark
    :type disabled_symbol: str
    :param instruction: instruction to display after the message
    :type instruction: str
    :param height: preferred height of the choice window
    :type height: Union[str, int]
    :param max_height: max height choice window should reach
    :type max_height: Union[str, int]
    :param validate: a callable or Validator instance to validate user selection
    :type validate: Union[Callable[[str], bool], Validator]
    :param invalid_message: message to display when input is invalid
    :type invalid_message: str
    """

    def __init__(
        self,
        message: str,
        choices: List[Union[Any, Dict[str, Any]]],
        default: Any = None,
        style: Dict[str, str] = {},
        editing_mode: Literal["emacs", "default", "vim"] = "default",
        qmark: str = "?",
        pointer: str = INQUIRERPY_POINTER_SEQUENCE,
        enabled_symbol: str = INQUIRERPY_FILL_HEX_SEQUENCE,
        disabled_symbol: str = INQUIRERPY_EMPTY_HEX_SEQUENCE,
        instruction: str = "",
        transformer: Callable = None,
        height: Union[int, str] = None,
        max_height: Union[int, str] = None,
        validate: Union[Callable[[str], bool], Validator] = None,
        invalid_message: str = "Invalid input",
    ) -> None:
        """Initialise the content_control and create Application."""
        self.content_control = InquirerPyCheckboxControl(
            choices, default, pointer, enabled_symbol, disabled_symbol
        )
        super().__init__(
            message=message,
            style=style,
            editing_mode=editing_mode,
            qmark=qmark,
            instruction=instruction,
            transformer=transformer,
            height=height,
            max_height=max_height,
            validate=validate,
            invalid_message=invalid_message,
            multiselect=True,
        )

    def _handle_enter(self, event) -> None:
        """Override this method to force empty array result.

        When user does not select anything, exit with empty list.
        """
        self.status["answered"] = True
        self.status["result"] = self.result_name
        event.app.exit(result=self.result_value)
