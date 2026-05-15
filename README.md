# ARGOS-SCAN v1.0 🛡️

**ARGOS-SCAN** es una herramienta de automatización para auditorías de seguridad y pentesting, diseñada para centralizar las fases críticas de reconocimiento, escaneo de vulnerabilidades y análisis de exploits en una única interfaz de consola.

Desarrollado originalmente como proyecto.

El script sigue una metodología de pentesting estructurada en 5 fases:

1.  **Reconocimiento (OSINT):** Enumeración de subdominios y búsqueda de directorios sensibles (`robots.txt`, etc.).
2.  **Escaneo de Red:** Identificación de puertos abiertos y detección de versiones de servicios mediante Nmap.
3.  **Auditoría Web:** Análisis de stack tecnológico y verificación de seguridad en cabeceras HTTP (HSTS, CSP, etc.).
4.  **Búsqueda de Exploits:** Integración con la base de datos de `Exploit-DB` a través de `Searchsploit` para identificar vectores de ataque basados en versiones de software detectadas.
5.  **Generación de Reportes:** Creación automática de un informe técnico detallado en formato `.txt` con hallazgos y sugerencias de remediación.

## 🛠️ Requisitos e Instalación

### Requisitos Previos
Es necesario tener instaladas las siguientes herramientas en tu sistema (preferentemente Parrot Security OS o Kali Linux):
* **Python 3.x**
* **Nmap**
* **Exploit-DB (Searchsploit)**

### Instalación
1. Clona el repositorio:

   git clone https://github.com/Ezequiel1889/argos_scan.git
   cd argos_scan

   pip3 install -r requirements.txt

💻 Uso
Para iniciar la herramienta, simplemente ejecuta el archivo principal:

python3 main.py

📝 Ejemplo de Reporte
La herramienta genera un archivo llamado informe_auditoria.txt que incluye:

Resumen de la fase de auditoría.

Estado del objetivo (Limpio/Vulnerable).

Detalle de exploits sugeridos para los servicios detectados.

Desarrollado por: Ezequiel Flammini
Año: 2026
