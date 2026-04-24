#!/bin/bash

echo "[*] Removing PyScan..."

# Remove symlink
sudo rm -f /usr/local/bin/pyscan

# Remove man page
sudo rm -f /usr/local/man/man1/pyscan.1

echo "[+] PyScan uninstalled successfully!"