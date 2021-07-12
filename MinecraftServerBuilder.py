import pip
import os
import time

try:
    from pip._internal.utils.misc import get_installed_distributions
except ImportError:
    from pip import get_installed_distributions
installed = get_installed_distributions()
l = list()
for i in installed:
    l.append(i.key)

if "msb" not in l:
    print("Package MSB not installed, installing...")
    pip.main(['install', '--upgrade', 'msb'])
    print("Restart MSB")
    os.system("pause")
    exit()

import sys
import urllib.request
import urllib.error

import msb.server
import msb.versioncheck

if os.path.isfile("update.py"):
    os.remove("update.py")
if os.path.isfile("update_msb.py"):
    os.remove("update_msb.py")
argv = sys.argv

if len(argv) != 1:
    if argv[1] == "--testmode":
        print("test completed")
        os.system("pause")
        exit()
version = "0.2"
if not msb.server.check_connection("https://nomfodm.site"):
    print("connection with server failed")
    os.system("pause")
    exit()

if msb.versioncheck.isUpdates("https://nomfodm.site/msb/clientActualInfo.json", version):
    print("Found updates.")
    time.sleep(2)
    msb.server.download_url("https://nomfodm.site/msb/update.py", "update.py")
    os.startfile("update.py")
    exit()

if msb.versioncheck.isUpdatesMsb("https://nomfodm.site/msb/clientActualInfo.json"):
    print("Found updates for msb package.")
    time.sleep(2)
    msb.server.download_url("https://nomfodm.site/msb/update_msb.py", "update_msb.py")
    os.startfile("update_msb.py")
    exit()

os.system("cls")
print("Hello user! It is Minecraft Server Builder (MSB)")
print("Here you can create your own Minecraft server build.")
g = False
while True:
    inp = input("Do you want to continue? (yes or no): ").lower()
    if inp == "no":
        g = False
        break
    elif inp == "yes":
        g = True
        break

if not g:
    print("OK, bye user!")
    os.system("pause")
    exit()

os.system("cls")
server_version = input("Please, write MC server version here (e.g 1.17.1) from 1.11 to latest version of MC: ")
from tkinter import Tk
from tkinter.filedialog import askdirectory

os.system("cls")
ram = input("Please, enter how many gigabytes you want to give to server: ")
os.system("cls")
print("OK, now, choose the directory for the build.")
input("<press enter>")
Tk().withdraw()
directory = askdirectory()
os.system("cls")
print("Now, please wait...")

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
try:
    url = f"https://download.getbukkit.org/spigot/spigot-{server_version}.jar"
    msb.server.download_url(url, directory + "/core.jar")
except urllib.error.HTTPError:
    url = f"https://cdn.getbukkit.org/spigot/spigot-{server_version}.jar"
    msb.server.download_url(url, directory + "/core.jar")
msb.server.download_url("https://nomfodm.site/msb/eula.txt", directory + "/eula.txt")
with open(directory + "/start.bat", 'w') as file:
    file.write("@echo off" + '\n')
    file.write(f"java -Xmx{ram}G -Xms1G -jar core.jar nogui" + '\n')
    file.write("pause")
    file.close()

os.system("cls")
print("Finally, your build is done.")
print("To run it you need to start 'start.bat' file.")
input("<press enter>")
os.startfile(os.path.realpath(directory))
exit()
