import os

from core.utils import (
    GREEN,
    MAGENTA,
    RED,
    RESET,
    clear,
    get_local_version,
    get_remote_version,
    info,
)

clear()
v_code = get_remote_version()
info("Checking tools version....\n")
this_version = get_local_version()
if this_version == v_code:
    info("All files up to date !\n", GREEN)
    info("run python3 main.py\n", RESET)
elif this_version != v_code:
    info("Downloading files....\n", MAGENTA)

    os.remove("main.py")
    os.remove("version")
    os.system("rm -rf core")
    os.system(
        "wget https://github.com/ashrafiabir01/wifihunter_update_zip/"
        "raw/main/wifihunter_update.zip"
    )
    os.system("unzip wifihunter_update.zip")
    os.system("rm -rf wifihunter_update.zip")
    info("\nUpdate Done\n")
    info("run python3 main.py\n", RESET)
else:
    info("Something wrong!\n", RED)
