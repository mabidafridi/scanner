#!/usr/bin/env python3
"""
Banner grabbing module for PyScan
"""

import socket

def grab_banner(ip, port, timeout=1.0):
    """
    Grab service banner from open port
    
    Args:
        ip: Target IP address
        port: Target port number
        timeout: Connection timeout in seconds
    
    Returns:
        Banner string or "No banner" if failed
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # Try common probes
        probes = [
            b"\r\n",  # Generic
            b"HEAD / HTTP/1.1\r\n\r\n",  # HTTP
            b"EHLO test\r\n",  # SMTP
            b"\x00",  # Generic
        ]
        
        for probe in probes:
            try:
                sock.send(probe)
                banner = sock.recv(256).decode('utf-8', errors='ignore').strip()
                if banner:
                    sock.close()
                    return banner[:100]  # First 100 chars
            except:
                continue
        
        sock.close()
        return "No banner"
    
    except:
        return "No banner"


def get_service_name(port):
    """
    Get common service name for a port
    
    Args:
        port: Port number
    
    Returns:
        Service name string
    """
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
        135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
        445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
    }
    return common_ports.get(port, "Unknown")