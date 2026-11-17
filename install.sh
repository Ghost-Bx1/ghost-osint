#!/usr/bin/env bash
# Ghost-OSINT Installer
# By Gh0st-Bx1 | github.com/Ghost-Bx1

G="\033[92m"; Y="\033[93m"; R="\033[91m"; C="\033[96m"
W="\033[97m"; D="\033[2m"; N="\033[1m"; X="\033[0m"
EQ="════════════════════════════════════════════════════════════════════"
HL="────────────────────────────────────────────────────────────────────"

banner() {
    echo -e "${G}╔${EQ}╗${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣇⠀⢿⣿⣿⡟⣿⣷⣄⠀⠙⢿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⢸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⢀⣾⣿⣿⢩⣿⠁⣾⣿⣿⡆⠀⢿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⢠⣿⣿⡟⣰⢿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣠⣴⣿⣧⠸⣿⣧⡐⠢⠉⠁⢀⣾⣿⣿⡇⣼⣿⢸⣿⣿⣿⣇⠀⢸${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣷⡀⠸⣿⣿⣧⠸⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⢃⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⠳⣘⣿⣿⣷⣶⣾⣿⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠀⢸${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⡇⠀⣿⣿⣿⡄⡿⢿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠋⢉⠉⡉⠛⠿⣿⠀⢸${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⡇⢀⣿⣿⣿⣧⢸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣾⣿⡄⠈⠀⠀⠀⠀ ⣾${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⡟⠀⣸⣿⣿⣿⣿⣜⡇⢿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠻⠇⠀⠰⠀⠀ ⣀⣾${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⠃⢠⣿⣿⠿⠿⠿⢿⣿⠸⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢣⢸⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⢰⠜⠋⠀⢀⡄⢰⣤⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠃⢻⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣆⠠⠀⡀⠀⠁⣿⣿⠟⠀⣽⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⢃⣿⣿⣿⡟⣸⣿⣿⣿⣿⡿⠋⢠⢃⣾⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣷⣶⠆⡄⠈⢉⣠⣴⣾⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠇⠛⢏⠉⠉⠁⠤⢊⣥⣾⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⢄⠀⢾⣿⣿⣿⣿⡇⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣶⣬⣭⣶⣾⣿⣿⠏⣼⣿⣿⣿⡇⣸⣿⣿⣿⠀⣰⣿⡁⢠⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣤⣀⡀⠀⠀⠉⠉⠁⢸⣿⣿⣿⢸⣿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⠇⣿⣿⣿⣿⡀⠹⢿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠛⠀⣼⣿⣿⣿⢸⣿⣿⢻⣿⣷⣌⠻⣿⣿⣿⣿⠟⣡⣾⣿⡟⣼⣿⣿⠀⣿⣿⣿⣿⣿⣶⣤⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⣴⣾⣿⣿⣿⡇⢸⣿⣿⣇⢻⣿⣿⣷⣦⣭⣭⣴⣾⣿⣿⣿⢡⣿⣿⣿⠀⣿⣿⣿⣿⣿⠿⠟⠃⡀⢸⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⡐⠠⢈⡉⠛⠛⠿⡇⢸⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⠀⣁⣤⡄⠀⣀⣒⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡌⠀⣦⠀⣼⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣄⡈⠛⠃⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢁⣤⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⠿⠿⣿⣿⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠈⣙⠛⠛⣛⣛⠛⠀⠻⢿⣿⣿⣿⣿⣿⣿⡃⢠⣤⠀⠀⣀⣉⣁⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣤⡀⢀⠈⢿⣿⣿⣿⣿⣷⣄⠁⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⢠⣿⣿⣿⣿⣿⠟⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⡿⢁⡄⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠘⣿⣿⣿⠁⠎⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡑⠈⠻⠇⠈⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}       ${G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿${X}       ${G}║${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}║${X}  ${G}${N}GHOST-OSINT INSTALLER${X}                                             ${G}║${X}"
    echo -e "${G}║${X}  ${C}v2.0.0  ${D}Extended OSINT Framework${X}                                  ${G}║${X}"
    echo -e "${G}║${X}  ${D}${HL:0:44}${X}                      ${G}║${X}"
    echo -e "${G}║${X}  ${W}By Gh0st-Bx1  ${D}│  github.com/Ghost-Bx1${X}                             ${G}║${X}"
    echo -e "${G}║${X}  ${D}${HL:0:44}${X}                      ${G}║${X}"
    echo -e "${G}║${X}                                                                    ${G}║${X}"
    echo -e "${G}╚${EQ}╝${X}"
    echo
}

info()  { echo -e "  ${C}[*]${X} $*"; }
ok()    { echo -e "  ${G}[+]${X} $*"; }
warn()  { echo -e "  ${Y}[~]${X} $*"; }
err()   { echo -e "  ${R}[!]${X} $*"; }
step()  { echo -e "\n${G}  >${X} ${W}$*${X}"; }

banner

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/opt/ghost-osint"
INSTALL_BIN="/usr/local/bin/ghost-osint"

if [[ $EUID -ne 0 ]]; then
    warn "Not running as root - installing to ~/.local"
    INSTALL_DIR="$HOME/.local/share/ghost-osint"
    INSTALL_BIN="$HOME/.local/bin/ghost-osint"
    mkdir -p "$HOME/.local/bin"
fi

step "Detecting system..."
PYTHON=$(command -v python3 || command -v python)
if [[ -z "$PYTHON" ]]; then
    err "Python 3 not found. Install python3 first."
    exit 1
fi
ok "Python: $($PYTHON --version 2>&1)"

step "Checking Python stdlib modules..."
for mod in socket urllib.request json re threading; do
    if $PYTHON -c "import $mod" 2>/dev/null; then
        ok "$mod available"
    else
        err "$mod not available (stdlib issue)"
    fi
done
info "ghost-osint uses Python stdlib only - no pip install needed"

step "Installing ghost-osint..."

mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/ghost-osint.py" "$INSTALL_DIR/ghost-osint.py"
chmod +x "$INSTALL_DIR/ghost-osint.py"
ok "Copied ghost-osint.py -> $INSTALL_DIR/"

[[ -f "$SCRIPT_DIR/README.md" ]] && cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"

mkdir -p "$(dirname "$INSTALL_BIN")"
cat > "$INSTALL_BIN" << WRAPPER
#!/usr/bin/env bash
exec python3 $INSTALL_DIR/ghost-osint.py "\$@"
WRAPPER
chmod +x "$INSTALL_BIN"
ok "Wrapper created: $INSTALL_BIN"

if [[ $EUID -ne 0 ]]; then
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        warn "Add to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

step "Verifying installation..."
echo
if "$PYTHON" "$INSTALL_DIR/ghost-osint.py" --no-banner --help &>/dev/null; then
    ok "ghost-osint.py runs correctly"
else
    warn "ghost-osint.py check returned non-zero (may be normal)"
fi

echo
echo -e "${G}  ╔══════════════════════════════════════╗${X}"
echo -e "${G}  ║${X}  ${G}${N}Installation complete!${X}              ${G}║${X}"
echo -e "${G}  ║${X}  ${D}Run:${X} ${W}ghost-osint --help${X}               ${G}║${X}"
echo -e "${G}  ║${X}  ${D}Or:${X}  ${W}ghost-osint --domain target.com${X}  ${G}║${X}"
echo -e "${G}  ╚══════════════════════════════════════╝${X}"
echo
