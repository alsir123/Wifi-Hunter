import requests, os

DATABASE_URL = "https://raw.githubusercontent.com/darkhunter141/Database/main/wifihunter_update_value.json"


def get_remote_version(url=DATABASE_URL):
    version_name = requests.get(url).json()
    return version_name["version"]


def read_local_version(path="version"):
    with open(path) as version_hunter:
        return int(version_hunter.readline())


if __name__ == "__main__":
    os.system("clear")
    v_code = get_remote_version()
    print("\033[91m[\033[00m*\033[91m] Checking tools version....\n\033[00m")
    this_version = read_local_version()
    if this_version == v_code:
        print("\033[91m[\033[00m*\033[91m] \033[92mAll files up to date !\n\033[00m")
        print("\033[91m[\033[00m*\033[91m] \033[00mrun python3 main.py\n\033[00m")
    elif this_version != v_code:
        print("\033[91m[\033[00m*\033[91m] \033[95mDownloading files....\n\033[00m")

        os.remove("main.py")
        os.remove("version")
        os.system("rm -rf core")
        os.system("wget https://github.com/ashrafiabir01/wifihunter_update_zip/raw/main/wifihunter_update.zip")
        os.system("unzip wifihunter_update.zip")
        os.system("rm -rf wifihunter_update.zip")
        print("\n\033[91m[\033[00m*\033[91m] \033[95mUpdate Done\n\033[00m")
        print("\033[91m[\033[00m*\033[91m] \033[00mrun python3 main.py\n\033[00m")
    else:
        print("\033[91m[\033[00m*\033[91m] \033[91mSomething wrong!\n\033[00m")
