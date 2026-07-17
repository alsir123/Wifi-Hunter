import os
import platform

from core.banner import banners
from core.utils import (
    RED,
    RESET,
    YELLOW,
    back_home,
    clear,
    get_local_version,
    get_remote_version,
    info,
    menu_option,
    prompt,
    show_interfaces,
    wrong_try_again,
)

username = os.getlogin()
if platform.system() == "Linux":
    pass
else:
    print(f"{RED} You can't do this here :)")
    exit()
if os.geteuid() == 0:
    pass
else:
    print(f"\n{RED} Hey {username}! You need root permissions to do this :)")
    print(f"\n {RESET}run sudo python3 main.py\n\n\n")
    exit()
clear()
info("Checking tools version\n")
v_code = get_remote_version()
this_version = get_local_version()
if this_version == v_code:
    pass
else:
    info("Update available !\n", YELLOW)
    info("Please run python3 updatetools.py\n\n", RESET)
    exit()


def monitor_mode(action, command_template):
    banners()
    clear()
    show_interfaces()
    print("\n")
    info(f"Type your wireless interface to {action} monitor mode")
    print("\n")
    interface = prompt()
    os.system(command_template.format(interface))
    back_home()


banners()
menu_option(1, "Install Wireless-tools (Install First)")
menu_option(2, "Wifi Spam")
menu_option(3, "Start monitor mode")
menu_option(4, "Stop monitor mode")
menu_option(0, "Exit")
option = int(prompt())
if option == 1:
    os.system("sudo python3 core/menu_install_tools.py")
elif option == 2:
    os.system("sudo python3 core/spam_wifi.py")
elif option == 3:
    monitor_mode("start", "airmon-ng start {} && airmon-ng check kill")
elif option == 4:
    monitor_mode(
        "stop",
        "airmon-ng stop {} && service network-manager restart"
        " && systemctl start NetworkManager",
    )
elif option == 0:
    wrong_try_again()
    exit()
else:
    wrong_try_again()
    exit()
