import requests
from colorama import Fore

def auditoria_web(url):
    if not url.startswith('http'):
        url = f"http://{url}"
    
    hallazgos_web = []
    tecnologias = []
    
    print(f"\n{Fore.YELLOW}[*] ARGOS: Iniciando Auditoria de Tecnologías en {url}...")
    
    try:
        res = requests.get(url, timeout=10)
        contenido = res.text.lower()
        headers = res.headers

        # --- DETECCIÓN DE TECNOLOGÍAS ---
        if 'wp-content' in contenido: tecnologias.append("WordPress")
        if 'joomla' in contenido: tecnologias.append("Joomla")
        if 'moodle' in contenido: tecnologias.append("Moodle")
        if 'drupal' in contenido: tecnologias.append("Drupal")

        if 'php' in headers.get('X-Powered-By', '').lower() or '.php' in contenido: 
            tecnologias.append("PHP")
        
        server = headers.get('Server', 'No detectado')
        tecnologias.append(f"Servidor: {server}")

        print(f"{Fore.CYAN}[+] Tecnologias detectadas: {', '.join(tecnologias)}")
        hallazgos_web.append(f"Stack Tecnologico: {', '.join(tecnologias)}")

        # --- ANÁLISIS DE SEGURIDAD (CABECERAS) ---
        print(f"{Fore.WHITE}[*] Analizando cabeceras de seguridad...")
        
        # Diccionario de cabeceras a revisar
        seguridad = {
            'X-Frame-Options': 'Vulnerable a Clickjacking',
            'Content-Security-Policy': 'Falta politica CSP',
            'X-Content-Type-Options': 'Falta proteccion MIME',
            'Strict-Transport-Security': 'Falta HSTS (HTTPS forzado)'
        }

        for h, msg in seguridad.items():
            if h in headers:
                # Ahora imprimimos lo que SI está bien para que no parezca colgado
                print(f"{Fore.GREEN}[OK] {h} detectada.")
            else:
                print(f"{Fore.RED}[!] Falta {h}")
                hallazgos_web.append(f"Seguridad: {msg}")

        print(f"{Fore.YELLOW}[*] Auditoria web finalizada.")
        return hallazgos_web

    except Exception as e:
        print(f"{Fore.RED}[!] Error en auditoria: {e}")
        return ["Error de conexion"]