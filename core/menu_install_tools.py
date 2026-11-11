from banner import banners
from utils import run, warn


def option(option_name, option_no):
    custom_option = f"\n\033[91m [\033[00m{option_no}\033[91m] \033[93m{option_name}"
    print(custom_option)


def menu():
    print("\n\n\033[91m Choose an option : ")
    option('Wifte', 1)
    option('Aircrack-ng', 2)
    option('Reaver', 3)
    option('Pixiewps', 4)
    option('Wireshark', 5)
    option('Wash', 6)
    option("Macchanger", 7)
    option("Cowpatty", 8)
    option("Bully", 9)
    option("Mdk3", 10)


TOOLS = [
    ("pixiewps", "pixiewps"),
    ("reaver", "reaver"),
    ("wifite", "wifite"),
    ("aircrack-ng", "aircrack-ng"),
    ("wireshark", "wireshark"),
    ("macchanger", "macchanger"),
    ("cowpatty", "cowpatty"),
    ("bully", "bully"),
    ("mdk3", "mdk3"),
    ("net-tools", "net-tools"),
]


def choice_intall_tools():
    choice = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    print()
    if choice != "y":
        run("clear")
        print("\033[91m Wrong try again!")
        print('\033[00m run sudo main.py\n\n\n')
        return

    print("\033[91m[\033[00m*\033[91m] apt update...\033[00m")
    if run("sudo apt-get update", "apt-get update") != 0:
        warn("Package list update failed; installations below may fail too.")

    failed = []
    for label, package in TOOLS:
        print(f"\033[91m[\033[00m*\033[91m] Installing {label}...\033[00m")
        if run(f"sudo apt-get install -y {package}", f"install {label}") != 0:
            failed.append(label)

    if failed:
        warn("The following tools failed to install: " + ", ".join(failed))
    else:
        print("\n\n Done")

    print("\n\033[91m Back home (y/n) ")
    choice = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    if choice == "y":
        run('python3 main.py', "restart wifi-hunter")
    else:
        print("\033[91m Wrong try again!")
        print('\033[00m run sudo main.py\n\n\n')


banners()
menu()
print("\n\033[91m[\033[00m*\033[91m]\033[91m Install all tools (y/n) ")
choice_intall_tools()
