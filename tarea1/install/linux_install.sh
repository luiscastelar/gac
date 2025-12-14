#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

open_terminal() {
    if command -v gnome-terminal >/dev/null 2>&1; then
        gnome-terminal -- bash -c "$1; exec bash"
    elif command -v konsole >/dev/null 2>&1; then
        konsole -e bash -c "$1; exec bash"
    elif command -v xterm >/dev/null 2>&1; then
        xterm -e bash -c "$1; exec bash"
    elif command -v open >/dev/null 2>&1; then
        # macOS
        open -a Terminal "$1"
    else
        echo "No se encontró un emulador de terminal"
        exit 1
    fi
}

open_terminal "$SCRIPT_DIR/install_internal.sh"
