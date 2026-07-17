import os

from banner import banners
from utils import RED, back_home, info, menu_option, prompt, wrong_try_again


def menu():
    print(f"\n\n{RED} Choose an option : ")
    menu_option(1, "Wifte")
    menu_option(2, "Aircrack-ng")
    menu_option(3, "Reaver")
    menu_option(4, "Pixiewps")
    menu_option(5, "Wireshark")
    menu_option(6, "Wash")
    menu_option(7, "Macchanger")
    menu_option(8, "Cowpatty")
    menu_option(9, "Bully")
    menu_option(10, "Mdk3")


def choice_intall_tools():
    option = prompt()
    print()
    if option == "y":
        info("apt update...")
        os.system("sudo apt-get update")
        info("Installing pixiewps...")
        os.system("sudo apt-get install -y pixiewps")
        info("Installing reaver...")
        os.system("sudo apt install reaver -y")
        info("Installing wifite...")
        os.system("sudo apt install wifite -y")
        info("Installing aircrack-ng...")
        os.system("sudo apt install aircrack-ng -y")
        info("Installing wireshark...")
        os.system("sudo apt install wireshark -y")
        info("Installing macchanger...")
        os.system("sudo apt install macchanger")
        info("Installing cowpatty...")
        os.system("sudo apt-get install cowpatty")
        info("Installing bully...")
        os.system("sudo apt-get install bully")
        info("Installing mdk3..")
        os.system("sudo apt-get install mdk3")
        os.system("sudo apt install net-tools")
        print("\n\n Done")
        back_home()
    else:
        wrong_try_again()


banners()
menu()
info(" Install all tools (y/n) ", RED)
choice_intall_tools()
