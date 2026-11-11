import os

from banner import banners
from utils import RED, info, menu_option, prompt, show_interfaces

banners()
show_interfaces()
print("\n\n")

menu_option(1, "Use Random SSIDS (slow)")
menu_option(2, "Use custom SSIDS")
menu_option(3, "Use default SSIDS")
menu_option(0, "Exit")
print(f"\n\n{RED} Choose an option : ")
option = int(prompt())
print("\n")
info("Type your wireless interface name : ")
option2 = prompt()
print("\n")
info("Turning on monitor mode")
os.system(f"macchanger -p {option2} >> /dev/null 2>&1")
os.system("sudo airmon-ng check kill")
os.system(f"sudo airmon-ng start {option2}")
info("Starting process...")
if option == 1:
    os.system(f"sudo mdk3 {option2} b -100 DH141")
elif option == 2:
    print(f"\n\n{RED} Type File Location  : ")
    filename = prompt()
    os.system(f"sudo mdk3 {option2} b -c 1 -f {filename}")
elif option == 3:
    os.system(f"sudo mdk3 {option2} b -c 1 -f core/ssid.txt")
else:
    exit()
