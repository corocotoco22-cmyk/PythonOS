import asyncio
import getpass
import socket
import PyGUI
import time
import json
import os
from colorama import init, Fore
from nicegui import ui

init(autoreset=True)

version = "RS 1.0"
MyGIT = "https://github.com/corocotoco22-cmyk/PythonOS"

class WebTerminal:
    def __init__(self):
        self.user_input = None
        self.event = asyncio.Event()
    async def input_prompt(self, label_text: str) -> str:
        self.event.clear()
        ui.label(label_text)
        txt = ui.input().on('keydown.enter', self._submit)
        ui.button('Enviar', on_click=self._submit)
        
        await self.event.wait()
        val = self.user_input
        txt.value = ''
        return val

    def _submit(self):
        self.user_input = ui.context.client.content.value # Ajustar para pegar o valor correto do input atual
        self.event.set()

def clear():
    os.system('powershell -Command clear')

def obter_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

logins = {
    "admin": "admin123",
}

try:
    with open("logins.json", "r", encoding="utf-8") as logins_json:
        logins = json.load(logins_json)
except FileNotFoundError:
    with open("logins.json", "w", encoding="utf-8") as logins_json:
        json.dump(logins, logins_json)

while True:
    clear()
    print(Fore.YELLOW + rf"""
     ____        _   _                    ___  ____  
    |  _ \ _   _| |_| |__   ___  _ __    / _ \/ ___| 
    | |_) | | | | __| '_ \ / _ \| '_ \  | | | \___ \ 
    |  __/| |_| | |_| | | | (_) | | | | | |_| |___) |
    |_|    \__, |\__|_| |_|\___/|_| |_|  \___/|____/ 
           |___/                                     
    IP: {obter_ip_local()}
    Versão: {version}
    Link de Download/Atualização: {MyGIT}
    """)
    usuario = input("Nome de usuário: ")
    senha = getpass.getpass("Senha, por motivos bem próvaveis a senha não vai parecer: ")

    if logins.get(usuario) == senha:
        print(Fore.GREEN + "Entrando...")
        break
    else:    
        print(Fore.RED + "SENHA OU USUÁRIO INVÁLIDOS")
        continue
while True:
    resposta = input(
        r"""
         ____                 /\/|             
        / ___|  ___  ___ ___ |/\/   ___  ___ _ 
        \___ \ / _ \/ __/ __|/ _ \ / _ \/ __(_)
         ___) |  __/\__ \__ \ (_) |  __/\__ \_ 
        |____/ \___||___/___/\___/ \___||___(_)
        
        Rive
        Shell
        Shell, Rive:"""
    )
    if resposta == "Shell":
        break
    elif resposta == "Rive":
        print("Ops..., não há PyLand rodando")
    else:
        continue

print(r"""
    ███████╗███████╗██╗  ██╗
    ╚══███╔╝██╔════╝██║  ██║
      ███╔╝ ███████╗███████║
     ███╔╝  ╚════██║██╔══██║
    ███████╗███████║██║  ██║
    ╚══════╝╚══════╝╚═╝  ╚═╝
    Para ajuda digite "help"
    """)

try:
    while True:
        resposta = input("Kiko :> ")
        if resposta == "help":
            print("""
            help: ajuda
            exit: sai
            ^C: sai
            rive_ui: UI (tercero)
            """)
        elif resposta == "exit":
                print(Fore.RED + "Saindo...")
                time.sleep(2)
                exit()
        elif resposta == "rive_ui":
            print("Ops..., não há PyLand rodando")
        else:
            print(Fore.RED + f"Comando {resposta} não encontrado, para ajuda digite help")
except KeyboardInterrupt:
    print(Fore.RED + "\nSaindo..., só não toca Ctrl + C de novo")
    time.sleep(2)
    exit()