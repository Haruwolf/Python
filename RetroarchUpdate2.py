import urllib.request
import os, ctypes, sys
import time
import pyperclip
import re
import getpass
from bs4 import BeautifulSoup
import requests
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

def sanityCheck():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def userVersionCheck():
    retroarchPath = f"C:\\Users\\{userName}\\AppData\\Roaming\\RetroArch\\retroarch.exe"
    dataArquivo = os.path.getctime(retroarchPath)
    print("O dia da sua versão é %s" %time.strftime("%d/%m/%Y", time.localtime((dataArquivo))))

def retroVersionCheck():
    htmlPage = requests.get("https://www.retroarch.com/?page=platforms").content
    extractPage = BeautifulSoup(htmlPage, 'html.parser')
    pattern = re.compile("The current stable version is: \d\.\d\.\d")
    version = extractPage.find("p", text = pattern)
    versionPattern = re.compile("\d\.\d\.\d")
    actualVersion = versionPattern.search(str(version))
    print("A versão atual disponível na página de downloads do Retroarch é a %s" %actualVersion.group(0))
    versionPage = requests.get("http://buildbot.libretro.com/stable/").content
    versionExtractPage = BeautifulSoup(versionPage, 'html.parser')
    searchversionDate = versionExtractPage.find_all("td")
    dates = str(searchversionDate)
    patternSearch = re.compile(f"({actualVersion.group(0)})\<\/a><\/td>, \<td class=\"fb-d\">((\d\d\d\d)-(\d\d)-(\d\d))") 
    takeDate = patternSearch.search(dates)
    retroVersion = str(takeDate.group(1))
    versionDay, versionMonth, versionYear = takeDate.group(5), takeDate.group(4), takeDate.group(3)
    print (f"A versão {retroVersion} é da data {versionDay}/{versionMonth}/{versionYear}")
    proceedCheck(retroVersion)

def proceedCheck(retroVersion):
    print ("Aperte ENTER para prosseguir")
    input()
    if (os.path.isfile(f"C:\\Users\\{userName}\\Downloads\\Outros\\retroarch.exe")):
        print("O setup já existe")
        print("Deletando setup antigo")
        os.remove(f"C:\\Users\\{userName}\\Downloads\\Outros\\retroarch.exe")
    else:
        print("O setup não existe")

    downloadAndInstall(retroVersion)
    
def downloadAndInstall(retroVersion):
        installPath = f"C:\\Users\\{userName}\\AppData\\Roaming\\RetroArch"
        pyperclip.copy(installPath)
        url = f"https://buildbot.libretro.com/stable/{retroVersion}/windows/x86_64/RetroArch-Win64-setup.exe"
        download = f"C:\\Users\\{userName}\\Downloads\\Outros\\retroarch.exe"
        print ("Baixando a versão mais recente")
        print ("Por favor aguarde")
        print ("...")
        urllib.request.urlretrieve(url,download)
        print ("Download completo, começando a instalação")
        inst = Application(backend="uia").start(download)
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("^v")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
        send_keys("{ENTER}")
   

def close():
    print ("Pressione ENTER para sair do programa")
    input()
    sys.exit(0)

userName = getpass.getuser()
sanityCheck()

if sanityCheck():
    print("Modo administrador detectado, prosseguindo com o updater")
else:
    print("Não será possível prosseguir a instalação, execute o programa em modo administrador")
    close()

userVersionCheck()
retroVersionCheck()
close()

