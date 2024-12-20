__version__ = "5.2.2"

from tkinter import Variable, StringVar, IntVar, DoubleVar, BooleanVar
from tkinter.constants import *
import tkinter.filedialog as filedialog

# import manager classes
from .windows.widgets.appearance_mode import AppearanceModeTracker
from .windows.widgets.scaling import ScalingTracker
from .windows.widgets.theme import ThemeManager

# import base widgets

# import widgets

# import windows

# import font classes

# import image classes

from .windows import ctk_tk

_ = Variable, StringVar, IntVar, DoubleVar, BooleanVar, CENTER, filedialog  # prevent IDE from removing unused imports


def set_appearance_mode(mode_string: str):
    """ possible values: light, dark, system """
    AppearanceModeTracker.set_appearance_mode(mode_string)


def get_appearance_mode() -> str:
    """ get current state of the appearance mode (light or dark) """
    if AppearanceModeTracker.appearance_mode == 0:
        return "Light"
    elif AppearanceModeTracker.appearance_mode == 1:
        return "Dark"


def set_default_color_theme(color_string: str):
    """ set color theme or load custom theme file by passing the path """
    ThemeManager.load_theme(color_string)


def set_widget_scaling(scaling_value: float):
    """ set scaling for the widget dimensions """
    ScalingTracker.set_widget_scaling(scaling_value)


def set_window_scaling(scaling_value: float):
    """ set scaling for window dimensions """
    ScalingTracker.set_window_scaling(scaling_value)


def deactivate_automatic_dpi_awareness():
    """ deactivate DPI awareness of current process (windll.shcore.SetProcessDpiAwareness(0)) """
    ScalingTracker.deactivate_automatic_dpi_awareness = True


def set_ctk_parent_class(ctk_parent_class):
    ctk_tk.CTK_PARENT_CLASS = ctk_parent_class
