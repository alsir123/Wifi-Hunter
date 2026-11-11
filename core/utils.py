"""Shared helpers for consistent error handling across Wifi-Hunter.

These helpers make failures visible instead of silently swallowing them:
shell commands report their exit status, network calls raise clear messages,
and user input is validated instead of crashing with a raw traceback.
"""
import shutil
import subprocess

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[00m"


def error(message):
    """Print an error message in a consistent style."""
    print(f"\n{RED}[!] {message}{RESET}")


def warn(message):
    """Print a warning message in a consistent style."""
    print(f"\n{YELLOW}[!] {message}{RESET}")


def run(command, description=None, check=False):
    """Run a shell command and surface its exit status.

    Returns the command's exit code. When the command fails (non-zero exit or
    the executable is missing) a clear message is printed instead of the error
    being silently swallowed. With ``check=True`` a non-zero exit aborts the
    program so failures propagate to the caller.
    """
    label = description or command
    try:
        completed = subprocess.run(command, shell=True)
    except OSError as exc:
        error(f"Could not run '{label}': {exc}")
        if check:
            raise SystemExit(1)
        return 1

    if completed.returncode != 0:
        warn(f"'{label}' exited with code {completed.returncode}")
        if check:
            raise SystemExit(completed.returncode)
    return completed.returncode


def require_command(name):
    """Return True if ``name`` is available on PATH, warning otherwise."""
    if shutil.which(name) is None:
        warn(f"Required command '{name}' was not found. Install it first "
             f"(menu option 1).")
        return False
    return True


def fetch_json(url, timeout=15):
    """Fetch and decode JSON, raising SystemExit with a clear message on error.

    Network problems, HTTP errors and malformed responses previously produced
    an unhandled traceback; here they are reported and propagated cleanly.
    """
    import requests

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        error(f"Failed to reach the update server: {exc}")
    except ValueError as exc:
        error(f"The update server returned an invalid response: {exc}")
    raise SystemExit(1)


def read_local_version(path="version"):
    """Read the integer version from ``path``.

    Returns None (after reporting the problem) if the file is missing or does
    not contain a valid integer, instead of crashing with a traceback.
    """
    try:
        with open(path) as version_file:
            return int(version_file.readline().strip())
    except FileNotFoundError:
        error(f"Version file '{path}' was not found.")
    except (ValueError, OSError) as exc:
        error(f"Could not read version from '{path}': {exc}")
    return None


def prompt_int(prompt, default=None):
    """Prompt for an integer, re-prompting instead of crashing on bad input.

    Returns ``default`` if the user aborts with EOF/Ctrl-C.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            warn("Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print()
            return default
