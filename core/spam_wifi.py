import os

from banner import banners
from utils import error, prompt_int, require_command, run

banners()
print('\n\n\033[92m Your interfaces : \n\033[00m')
run('bash core/interface_device.sh', "list interfaces")
print("\n\n")


def main_option(no, name):
    print(f"\n\033[91m [\033[00m{no}\033[91m] \033[93m{name}")


main_option(1, "Use Random SSIDS (slow)")
main_option(2, "Use custom SSIDS")
main_option(3, "Use default SSIDS")
main_option(0, "Exit")
print("\n\n\033[91m Choose an option : ")
option = prompt_int("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ")
if option == 0 or option is None:
    raise SystemExit(0)
if option not in (1, 2, 3):
    error("Invalid option.")
    raise SystemExit(1)

print("\n\n\033[91m[\033[00m*\033[91m] Type your wireless interface name : \033[00m")
option2 = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ").strip()
if not option2:
    error("No interface name provided.")
    raise SystemExit(1)

for tool in ("airmon-ng", "mdk3"):
    if not require_command(tool):
        raise SystemExit(1)

print("\n\n\033[91m[\033[00m*\033[91m] Turning on monitor mode\033[00m")
run(f"macchanger -p {option2} >> /dev/null 2>&1", "reset MAC address")
run("sudo airmon-ng check kill", "kill interfering processes")
if run(f"sudo airmon-ng start {option2}", "start monitor mode") != 0:
    error(f"Could not start monitor mode on '{option2}'.")
    raise SystemExit(1)

print("\n\033[91m[\033[00m*\033[91m] Starting process...\033[00m")
if option == 1:
    run(f"sudo mdk3 {option2} b -100 DH141", "random SSID beacon spam")
elif option == 2:
    print("\n\n\033[91m Type File Location  : ")
    filename = input("\n\n\033[92m ͟w͟i͟f͟i͟-͟h͟u͟n͟t͟e͟r͟ > ").strip()
    if not os.path.isfile(filename):
        error(f"SSID file '{filename}' was not found.")
        raise SystemExit(1)
    run(f"sudo mdk3 {option2} b -c 1 -f {filename}", "custom SSID beacon spam")
elif option == 3:
    default_ssids = "core/ssid.txt"
    if not os.path.isfile(default_ssids):
        error(f"Default SSID file '{default_ssids}' was not found.")
        raise SystemExit(1)
    run(f"sudo mdk3 {option2} b -c 1 -f {default_ssids}",
        "default SSID beacon spam")
