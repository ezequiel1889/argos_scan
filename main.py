import os
import sys
import subprocess
import getpass
from colorama import Fore, Back, Style, init

try:
    from recon import buscar_subdominios, buscar_directorios
    from scanner import escanear_vulnerabilidades
    from web_audit import auditoria_web
except ImportError as e:
    print(f"\n{Fore.RED}[!] Error: Faltan archivos del proyecto ({e})")
    sys.exit()

init(autoreset=True)
usuario_sistema = getpass.getuser()
memoria_auditoria = []
servicios_global = [] 

def mostrar_banner():
    banner = f"""{Fore.CYAN}
    █████╗ ██████╗  ██████╗  ██████╗ ███████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗██╔════╝     ██╔════╝██╔════╝██╔══██╗████╗  ██║
    ███████║██████╔╝██║  ███╗██║   ██║███████╗     ███████╗██║     ███████║██╔██╗ ██║
    ██╔══██║██╔══██╗██║   ██║██║   ██║╚════██║     ╚════██║██║     ██╔══██║██║╚██╗██║
    ██║  ██║██║  ██║╚██████╔╝╚██████╔╝███████║     ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    {Fore.YELLOW}
          [+] Pentesting Methodology Tool | v1.0
          [+] Desarrollado por: Ezequiel Flammini
    """
    print(banner)

def generar_reporte_completo():
    print(f"\n{Fore.BLACK}{Back.WHITE}          RESUMEN DE AUDITORÍA (CONSOLA)          ")
    if not memoria_auditoria:
        print(f"{Fore.RED}\n[!] Sin datos registrados."); return

    try:
        with open("informe_auditoria.txt", "w") as f:
            f.write("*"*85 + "\n")
            f.write("   REPORTE TÉCNICO DETALLADO DE VULNERABILIDADES - ARGOS SCAN\n")
            f.write(f"   Responsable: Ezequiel Flammini | Auditor: {usuario_sistema}\n")
            f.write("*" * 85 + "\n\n")

            for entrada in memoria_auditoria:
                es_vuln = len(entrada['detalle'].strip()) > 30
                status_txt = "VULNERABLE" if es_vuln else "LIMPIO"
                status_color = Fore.RED + status_txt if es_vuln else Fore.GREEN + status_txt
                
                # --- RESUMEN EN CONSOLA ---
                print(f"{Fore.CYAN}Fase: {entrada['fase']:<20} | Objetivo: {entrada['target']:<30} | Estado: {status_color}")

                # --- DETALLE EN ARCHIVO TXT ---
                f.write(f"\n[+] FASE: {entrada['fase']}\n")
                f.write(f"[*] OBJETIVO: {entrada['target']}\n")
                
                if es_vuln:
                    f.write("-" * 40 + "\n")
                    f.write(f"ESTADO: {status_txt}\n")
                    if "EXPLOITS" in entrada['fase']:
                        f.write("\n" + "!"*25 + " COMANDOS DE BUSQUEDA SUGERIDOS " + "!"*25 + "\n")
                        for s in servicios_global:
                            v_recom = " ".join(s.split()[:2])
                            f.write(f" ==> searchsploit {v_recom}\n")
                        f.write("!"*82 + "\n")
                    f.write(f"\nHALLAZGOS TÉCNICOS:\n{entrada['detalle']}\n")
                else:
                    f.write("ESTADO: SEGURO\n")
                f.write("=" * 85 + "\n")

        print(f"\n{Fore.YELLOW}[i] Detalle técnico guardado en 'informe_auditoria.txt'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    os.system('clear')
    mostrar_banner()
    
    while True:
        print(f"\n{Fore.WHITE}--- MENÚ DE OPERACIONES ---")
        print(f"{Fore.GREEN}[1]{Fore.WHITE} Fase 1: Reconocimiento (Subdominios y Directorios)")
        print(f"{Fore.GREEN}[2]{Fore.WHITE} Fase 2: Escaneo de Red (Nmap - Puertos y Versiones)")
        print(f"{Fore.GREEN}[3]{Fore.WHITE} Fase 3: Auditoría Web (Stack Tecnológico y Cabeceras)")
        print(f"{Fore.GREEN}[4]{Fore.WHITE} Fase 4: Búsqueda de Exploits (Searchsploit)")
        print(f"{Fore.GREEN}[5]{Fore.WHITE} Fase 5: Informe Final (Consola y Archivo TXT)")
        print(f"{Fore.RED}[0]{Fore.WHITE} Salir")

        opc = input(f"\n{Fore.CYAN}ARGOS-SCAN > {Fore.WHITE}")

        if opc == '1':
            t = input("Dominio: "); buscar_subdominios(t); buscar_directorios(f"http://{t}")
            memoria_auditoria.append({"fase": "RECONOCIMIENTO", "target": t, "detalle": "Análisis de subdominios y directorios finalizado."})
        
        elif opc == '2':
            t = input("IP: "); h, v = escanear_vulnerabilidades(t)
            servicios_global = v
            memoria_auditoria.append({"fase": "ESCANEO RED", "target": t, "detalle": "\n".join(h)})
        
        elif opc == '3':
            t = input("URL: "); h_web = auditoria_web(t)
            memoria_auditoria.append({"fase": "AUDITORÍA WEB", "target": t, "detalle": "\n".join(h_web)})
        
        elif opc == '4':
            if not servicios_global:
                print(f"{Fore.RED}[!] Error: Realizá la Fase [2] primero."); continue
            
            detalle_exp = ""
            print(f"\n{Fore.YELLOW}[*] Buscando vulnerabilidades críticas...")
            for srv in servicios_global:
                srv_corto = " ".join(srv.split()[:2])
                res = subprocess.getoutput(f"searchsploit {srv_corto}")
                
                if "No Results" in res:
                    solo_nombre = srv.split(' ')[0]
                    res = subprocess.getoutput(f"searchsploit {solo_nombre} | head -n 12")
                
                if "No Results" not in res:
                    print(f"{Fore.RED}[VULNERABLE] {srv_corto}")
                    detalle_exp += f"\n--- REPORTE DE EXPLOITS PARA: {srv} ---\n{res}\n"
                else:
                    print(f"{Fore.GREEN}[LIMPIO] {srv_corto}")
            
            memoria_auditoria.append({"fase": "ANÁLISIS EXPLOITS", "target": "Servicios Red", "detalle": detalle_exp if detalle_exp else "Sin hallazgos."})

        elif opc == '5': generar_reporte_completo()
        elif opc == '0': sys.exit()

        while True:
            resp = input(f"\n{Fore.CYAN}¿Seguir escaneando? (si/no): ").strip().lower()
            if resp == 'si': break
            elif resp == 'no': 
                print(f"\n{Fore.MAGENTA}Auditoria Finalizada, buen trabajo {usuario_sistema}"); sys.exit()