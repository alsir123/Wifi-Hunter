"""Shared utilities for Wifi-Hunter.

This module centralises the code that was previously duplicated across
``main.py``, ``updatetools.py`` and the scripts in ``core/`` (ANSI colours,
the interactive prompt, menu rendering, status messages, interface listing,
version checking and the common navigation helpers).
"""

import os

import requests

# ANSI colour codes used throughout the project.
RED = "\033[91m"
RESET = "\033[00m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"

# Interactive prompt shown to the user.
PROMPT = f"\n\n{GREEN} ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > "

# Remote source used to check for updates.
DATABASE_URL = (
    "https://raw.githubusercontent.com/darkhunter141/Database/main/"
    "wifihunter_update_value.json"
)

# Path to the helper script that lists network interfaces.
INTERFACE_SCRIPT = "core/interface_device.sh"


def clear():
    """Clear the terminal."""
    os.system("clear")


def prompt():
    """Show the standard prompt and return the user's input."""
    return input(PROMPT)


def menu_option(no, name):
    """Print a single numbered menu entry."""
    print(f"\n{RED} [{RESET}{no}{RED}] {YELLOW}{name}")


def info(message, color=RED):
    """Print a ``[*]`` prefixed status message."""
    print(f"{RED}[{RESET}*{RED}] {color}{message}{RESET}")


def show_interfaces():
    """Display the machine's network interfaces."""
    print(f"\n\n{GREEN} Your interfaces : \n{RESET}")
    os.system(f"bash {INTERFACE_SCRIPT}")


def wrong_try_again():
    """Clear the screen and print the standard 'try again' message."""
    clear()
    print(f"{RED} Wrong try again!")
    print(f"{RESET} run sudo main.py\n\n\n")


def back_home():
    """Prompt to return to the main menu, restarting it on 'y'."""
    print(f"\n{RED} Back home (y/n) ")
    option = prompt()
    if option == "y":
        os.system("python3 main.py")
    else:
        wrong_try_again()


def get_remote_version():
    """Return the latest version code published in the remote database."""
    return requests.get(DATABASE_URL).json()["version"]


def get_local_version():
    """Return the version code stored in the local ``version`` file."""
    with open("version") as version_hunter:
        return int(version_hunter.readline())
