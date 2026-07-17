import getpass
import os
import platform

from core.utils import error, fetch_json, prompt_int, read_local_version, run

try:
    username = os.getlogin()
except OSError:
    username = getpass.getuser()
if platform.system() != "Linux":
    print("\033[91m You can't do this here :)")
    raise SystemExit(1)
if os.geteuid() != 0:
    print(
        f"\n\033[91m Hey {username}! You need root permissions to do this :)")
    print("\n \033[00mrun sudo python3 main.py\n\n\n")
    raise SystemExit(1)
os.system("clear")
print("\033[91m[\033[00m*\033[91m] Checking tools version\n\033[00m")
database_url = "https://raw.githubusercontent.com/darkhunter141/Database/main/wifihunter_update_value.json"
version_name = fetch_json(database_url)
try:
    v_code = version_name["version"]
except (KeyError, TypeError):
    error("The update server response did not contain a version field.")
    raise SystemExit(1)

this_version = read_local_version("version")
if this_version is None:
    raise SystemExit(1)
if this_version != v_code:
    print("\033[91m[\033[00m*\033[91m] \033[93mUpdate available !\n\033[00m")
    print("\033[91m[\033[00m*\033[91m] \033[00mPlease run python3 updatetools.py\n\n\033[00m")
    raise SystemExit(0)


def main_option(no, name):
    print(f"\n\033[91m [\033[00m{no}\033[91m] \033[93m{name}")


from core.banner import banners
banners()
main_option(1, "Install Wireless-tools (Install First)")
main_option(2, "Wifi Spam")
main_option(3, "Start monitor mode")
main_option(4, "Stop monitor mode")
main_option(0, "Exit")
option = prompt_int("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
if option == 1:
    run("sudo python3 core/menu_install_tools.py",
        "install wireless-tools menu")
elif option == 2:
    run("sudo python3 core/spam_wifi.py", "wifi spam")
elif option == 3:
    banners()
    os.system('clear')
    print('\n\n\033[92m Your interfaces : \n\033[00m')
    run('bash core/interface_device.sh', "list interfaces")
    print('\n')
    print(
        "\033[91m[\033[00m*\033[91m] Type your wireless interface to start monitor mode\033[00m")
    print("\n")
    interface = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    command = "airmon-ng start {} && airmon-ng check kill".format(interface)
    run(command, "start monitor mode")
    print("\n\033[91m Back home (y/n) ")
    option = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    if option == "y":
        run('python3 main.py', "restart wifi-hunter")
    else:
        os.system('clear')
        print("\033[91m Wrong try again!")
        print('\033[00m run sudo main.py\n\n\n')
elif option == 4:
    banners()
    os.system('clear')
    print('\n\n\033[92m Your interfaces : \n\033[00m')
    run('bash core/interface_device.sh', "list interfaces")
    print('\n')
    print(
        "\033[91m[\033[00m*\033[91m] Type your wireless interface to stop monitor mode\033[00m")
    print("\n")
    interface = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    command = "airmon-ng stop {} && service network-manager restart && systemctl start NetworkManager".format(
        interface)
    run(command, "stop monitor mode")
    print("\n\033[91m Back home (y/n) ")
    option = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
    if option == "y":
        run('python3 main.py', "restart wifi-hunter")
    else:
        os.system('clear')
        print("\033[91m Wrong try again!")
        print('\033[00m run sudo main.py\n\n\n')

elif option == 0:
    os.system('clear')
    raise SystemExit(0)
else:
    os.system('clear')
    print("\033[91m Wrong try again!")
    print('\033[00m run sudo main.py\n\n\n')
    raise SystemExit(1)
