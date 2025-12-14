#!/bin/sh
# ============================================
# Lanzador de la aplicación Python (Linux/macOS)
# ============================================

# Cambiar al directorio del script
cd "$(dirname "$0")" || exit 1

# Comprobar Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 no está instalado"
    exit 1
fi

# Ejecutar la aplicación
python3 html2graphml.py
exit 0