#!/usr/bin/env python3
"""
Inline utilities to avoid external dependencies.
"""


def printc(message: str, c: str = "blue", **kwargs):
    """Simple colored print with colorama fallback."""
    try:
        from colorama import Fore, Style, init
        init(autoreset=True)

        colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "black": Fore.BLACK,
        }

        color_code = colors.get(c, "")
        print(f"{color_code}{message}{Style.RESET_ALL}", **kwargs)
    except ImportError:
        # Fallback if colorama not available
        print(message, **kwargs)
