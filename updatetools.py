import os

from core.utils import error, fetch_json, read_local_version, run

os.system("clear")
database_url = "https://raw.githubusercontent.com/darkhunter141/Database/main/wifihunter_update_value.json"
version_name = fetch_json(database_url)
try:
    v_code = version_name["version"]
except (KeyError, TypeError):
    error("The update server response did not contain a version field.")
    raise SystemExit(1)

print("\033[91m[\033[00m*\033[91m] Checking tools version....\n\033[00m")

this_version = read_local_version("version")
if this_version is None:
    raise SystemExit(1)

if this_version == v_code:
    print("\033[91m[\033[00m*\033[91m] \033[92mAll files up to date !\n\033[00m")
    print("\033[91m[\033[00m*\033[91m] \033[00mrun python3 main.py\n\033[00m")
    raise SystemExit(0)

print("\033[91m[\033[00m*\033[91m] \033[95mDownloading files....\n\033[00m")

update_url = "https://github.com/ashrafiabir01/wifihunter_update_zip/raw/main/wifihunter_update.zip"
archive = "wifihunter_update.zip"

# Download first; only touch the existing installation once we know the new
# files are in hand, so a failed download can't leave a broken install.
if run(f"wget -O {archive} {update_url}", "download update") != 0:
    error("Download failed; your existing files were left untouched.")
    raise SystemExit(1)

for stale in ("main.py", "version"):
    try:
        os.remove(stale)
    except FileNotFoundError:
        pass
    except OSError as exc:
        error(f"Could not remove '{stale}': {exc}")
        raise SystemExit(1)
run("rm -rf core", "remove old core directory")

if run(f"unzip -o {archive}", "extract update") != 0:
    error("Extraction failed; the update is incomplete.")
    raise SystemExit(1)

run(f"rm -f {archive}", "clean up archive")
print("\n\033[91m[\033[00m*\033[91m] \033[95mUpdate Done\n\033[00m")
print("\033[91m[\033[00m*\033[91m] \033[00mrun python3 main.py\n\033[00m")
