import nmap
from colorama import Fore

def escanear_vulnerabilidades(objetivo):
    nm = nmap.PortScanner()
    print(f"\n{Fore.YELLOW}[*] ARGOS analizando: {objetivo}...")
    
    nm.scan(objetivo, arguments='-sV --version-intensity 5')
    hallazgos = []
    versiones = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                servicio = nm[host][proto][port]['product']
                version = nm[host][proto][port]['version']
                
                info_completa = f"{servicio} {version}".strip()
                if not info_completa:
                    info_completa = "Desconocido"
                
                print(f"{Fore.GREEN}Puerto {port}: {Fore.WHITE}{info_completa}")
                hallazgos.append(f"Puerto {port}: {info_completa}")
                
                if servicio and servicio != "Desconocido":
                    v_limpia = version.split(' ')[0] if version else ""
                    versiones.append(f"{servicio} {v_limpia}".strip())
                    
    return hallazgos, versiones