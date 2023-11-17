from typing import List, Optional, Tuple, Union

import PySimpleGUI as sg

from src.button import GREY_BUTTON, OFF_IMAGE
from src.config import APPLICATION_WIDTH, DEFAULT_MODEL, MODELS, THEME


class BtnInfo:
    def __init__(self, state: bool = False) -> None:
        self.state: bool = state


def create_button(
    key: str,
    tooltip: str,
    text: str = "",
    image_data: str = None,
    subsample: int = 1,
    standard: bool = False,
) -> sg.Button:
    if not standard:
        theme_bg_color: str = sg.theme_background_color()
        color = (theme_bg_color, theme_bg_color)
    else:
        color = None

    return sg.Button(
        image_data=image_data,
        key=key,
        image_subsample=subsample,
        border_width=0,
        tooltip=tooltip,
        button_color=color,
        disabled_button_color=color,
        metadata=BtnInfo(),
        button_text=text,
    )


def create_text_area(
    text: str = "",
    size: Optional[Tuple[int, int]] = None,
    key: str = "",
    text_color: str = None,
) -> sg.Text:
    return sg.Text(
        text=text,
        size=size,
        key=key,
        background_color=sg.theme_background_color(),
        text_color=text_color,
        expand_x=True,
        expand_y=True,
    )


def name(name: str):
    spaces: int = 15 - len(name) - 2
    return sg.Text(
        name + " " * spaces,
    )


def create_frame(
    layout=[[]], title: str = "", key: str = "", border: int = 0
) -> sg.Frame:
    return sg.Frame(
        title=title,
        layout=layout,
        key=key,
        border_width=border,
        expand_x=True,
        expand_y=True,
    )


def create_column(layout, key: str = "") -> sg.Column:
    return sg.Column(
        layout=layout,
        key=key,
        expand_x=True,
        expand_y=True,
    )


def build_layout() -> (
    List[List[Union[sg.Text, sg.Button, sg.Frame, sg.Combo, sg.Input]]]
):
    # Create elements
    record_button: sg.Button = create_button(
        image_data=OFF_IMAGE,
        tooltip="Start/Stop Recording",
        key="-RECORD_BUTTON-",
    )
    analyze_button: sg.Button = create_button(
        image_data=GREY_BUTTON,
        text="Analyze",
        tooltip="Transcribe and Analyze",
        key="-ANALYZE_BUTTON-",
        subsample=2,
    )
    close_button: sg.Button = create_button(
        image_data=GREY_BUTTON,
        text="Close",
        tooltip="Exit the application",
        key="-CLOSE_BUTTON-",
        subsample=2,
    )

    transcribed_text: sg.Text = create_text_area(
        size=(APPLICATION_WIDTH, 3), key="-TRANSCRIBED_TEXT-", text_color="white"
    )
    quick_answer: sg.Text = create_text_area(
        size=(APPLICATION_WIDTH, 7), key="-QUICK_ANSWER-", text_color="white"
    )
    full_answer: sg.Text = create_text_area(
        size=(APPLICATION_WIDTH, 20), key="-FULL_ANSWER-", text_color="white"
    )

    instructions: sg.Text = create_text_area(
        size=(int(APPLICATION_WIDTH * 0.7), 2),
        key="-INSTRUCTIONS-",
        text="Press 'R' to start recording\nPress 'A' to transcribe the recording and provide answers",
    )

    model = sg.Combo(
        MODELS,
        default_value=DEFAULT_MODEL,
        readonly=True,
        k="-MODEL_COMBO-",
        s=28,
        tooltip="Select the model to use",
    )
    position = sg.Input(
        default_text="Python Developer",
        k="-POSITION_INPUT-",
        s=30,
        tooltip="Enter the position you are applying for",
        focus=False,
    )

    # Create frames
    top_frame = create_frame(
        layout=[
            [name("Model"), model],
            [name("Position"), position],
        ],
        key="-TOP_FRAME-",
    )
    instructions_frame = create_frame(
        title="",
        layout=[[instructions]],
        key="-INSTRUCTIONS_FRAME-",
    )
    buttons_frame = create_frame(
        layout=[[record_button], [analyze_button]],
        key="-BUTTONS_FRAME-",
    )
    question_frame = create_frame(
        title="Transcribed Question",
        layout=[[transcribed_text]],
        key="-QUESTION_FRAME-",
        border=1,
    )
    short_answer_frame = create_frame(
        title="Short Answer",
        layout=[[quick_answer]],
        key="-SHORT_ANSWER_FRAME-",
        border=1,
    )
    full_answer_frame = create_frame(
        title="Full Answer", layout=[[full_answer]], key="-FULL_ANSWER_FRAME-", border=1
    )
    close_button_frame = create_frame(
        title="",
        layout=[[close_button]],
        key="-CLOSE_BUTTON_FRAME-",
    )

    # Create columns
    col1 = create_column(
        layout=[[instructions_frame], [top_frame]],
        key="-COL1-",
    )

    col2 = create_column(
        layout=[[buttons_frame]],
        key="-COL2-",
    )

    col3 = create_column(
        layout=[[question_frame], [short_answer_frame], [full_answer_frame]],
        key="-COL3-",
    )

    col4 = create_column(
        layout=[[close_button_frame]],
        key="-COL4-",
    )

    layout = [[col1, col2], [col3], [col4]]

    return layout


def initialize_window() -> sg.Window:
    sg.theme(THEME)
    layout: List[
        List[Union[sg.Text, sg.Button, sg.Frame, sg.Combo, sg.Input]]
    ] = build_layout()

    return sg.Window(
        "Interview",
        layout,
        return_keyboard_events=True,
        use_default_focus=False,
        resizable=True,
    )
