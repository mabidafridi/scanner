#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════╗"
echo "║     Installing PyScan Toolkit         ║"
echo "║     Red Team Port Scanner              ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found. Installing...${NC}"
    sudo apt install python3 python3-pip -y
fi

# Install dependencies
echo -e "${GREEN}[+] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt 2>/dev/null || echo "No dependencies"

# Make main script executable
echo -e "${GREEN}[+] Making scripts executable...${NC}"
chmod +x pyscan.py
chmod +x uninstall.sh

# Create symlink for system-wide use
echo -e "${GREEN}[+] Installing to /usr/local/bin...${NC}"
sudo ln -sf $(pwd)/pyscan.py /usr/local/bin/pyscan

# Create man page (optional)
echo -e "${GREEN}[+] Creating man page...${NC}"
sudo mkdir -p /usr/local/man/man1
sudo cat > /usr/local/man/man1/pyscan.1 << 'EOF'
.TH PYSCAN 1 "2024" "PyScan v1.0" "Red Team Tools"
.SH NAME
pyscan \- Professional Port Scanner
.SH SYNOPSIS
pyscan [target] [options]
.SH DESCRIPTION
PyScan is a fast, multi-threaded port scanner for red team operations.
.SH OPTIONS
\-p, \-\-ports    Port range (1-1000 or 22,80,443)
\-t, \-\-threads  Number of threads (default: 100)
\-o, \-\-output   Save results to file
\-\-timeout       Connection timeout (default: 1.0)
EOF

sudo mandb &>/dev/null

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════╗"
echo "║  ✅ Installation Complete!            ║"
echo "║                                       ║"
echo "║  Try: pyscan scanme.nmap.org -p 1-100 ║"
echo "║  Help: pyscan -h                      ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"