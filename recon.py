import requests
import os
from colorama import Fore

def buscar_subdominios(dominio):
    print(f"\n{Fore.YELLOW}[*] ARGOS iniciando escaneo masivo en: {dominio}")
    
    # Buscamos el archivo wordlist.txt en la carpeta del proyecto
    ruta_wordlist = os.path.join(os.path.dirname(__file__), "wordlist.txt")
    
    if os.path.exists(ruta_wordlist):
        with open(ruta_wordlist, 'r') as f:
            subs = [line.strip() for line in f.readlines() if line.strip()]
        print(f"{Fore.CYAN}[+] Cargado diccionario local ({len(subs)} palabras)")
    else:
        print(f"{Fore.RED}[!] Error: No se encontró wordlist.txt. Usando lista básica.")
        subs = ['www', 'mail', 'admin', 'dev']

    encontrados = 0
    for s in subs:
        url = f"http://{s}.{dominio}"
        try:
            res = requests.get(url, timeout=1.5)
            if res.status_code == 200:
                print(f"{Fore.GREEN}[+] Activo: {url}")
                encontrados += 1
        except:
            pass
    print(f"\n{Fore.CYAN}[*] Escaneo finalizado. Se encontraron {encontrados} subdominios.")

def buscar_directorios(url_base):
    print(f"\n{Fore.YELLOW}[*] Buscando directorios sensibles...")
    rutas = ['admin', 'login', 'db', '.env', 'config', 'phpmyadmin', 'backup', 'robots.txt']
    for r in rutas:
        url = f"{url_base}/{r}"
        try:
            res = requests.get(url, timeout=1.5)
            if res.status_code == 200:
                print(f"{Fore.RED}[!] Encontrado: {url}")
        except:
            pass