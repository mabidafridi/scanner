#!/usr/bin/env python3
import socket
import threading
import queue
import time
from datetime import datetime

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
    135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

class PortScanner:
    def __init__(self, target, ports, threads=100, timeout=1.0, grab_banner=True):
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.grab_banner = grab_banner
        self.open_ports = []
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        
        # Parse ports
        if "-" in ports:
            start, end = map(int, ports.split("-"))
            self.port_list = range(start, end + 1)
        else:
            self.port_list = [int(p) for p in ports.split(",")]
    
    def get_banner(self, ip, port):
        """Grab service banner"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((ip, port))
            s.send(b"HEAD / HTTP/1.1\r\n\r\n")
            banner = s.recv(256).decode('utf-8', errors='ignore').strip()
            s.close()
            return banner[:100] if banner else "No banner"
        except:
            return "No banner"
    
    def scan_port(self, ip, port):
        """Scan individual port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                banner = self.get_banner(ip, port) if self.grab_banner else "Skipped"
                
                with self.lock:
                    self.open_ports.append({
                        'port': port,
                        'service': service,
                        'banner': banner,
                        'state': 'open'
                    })
                    
                    # Live output
                    print(f"\033[92m[+] Port {port}\033[0m - \033[93m{service}\033[0m")
                    if banner and banner != "No banner":
                        print(f"    └─ \033[94m{banner[:80]}\033[0m")
            sock.close()
        except:
            pass
    
    def worker(self):
        """Thread worker"""
        while not self.queue.empty():
            try:
                port = self.queue.get_nowait()
            except queue.Empty:
                break
            
            self.scan_port(self.target, port)
            self.queue.task_done()
    
    def scan(self):
        """Main scan"""
        # Resolve hostname
        try:
            ip = socket.gethostbyname(self.target)
            print(f"[*] Target: {self.target} → {ip}\n")
            self.target = ip
        except:
            print(f"\033[91m[-] Cannot resolve {self.target}\033[0m")
            return []
        
        # Fill queue
        for port in self.port_list:
            self.queue.put(port)
        
        print(f"[*] Scanning {len(self.port_list)} ports with {self.threads} threads...\n")
        start_time = datetime.now()
        
        # Start threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        
        # Wait for completion
        self.queue.join()
        for t in threads:
            t.join()
        
        duration = (datetime.now() - start_time).total_seconds()
        print(f"\n\033[92m[+] Scan completed in {duration:.2f} seconds\033[0m")
        print(f"\033[92m[+] Found {len(self.open_ports)} open ports\033[0m")
        
        return self.open_ports
    
    def save_results(self, filename):
        """Save to file"""
        with open(filename, 'w') as f:
            f.write(f"PyScan Results - {self.target}\n")
            f.write(f"Scan time: {datetime.now()}\n")
            f.write(f"{'='*50}\n\n")
            for p in self.open_ports:
                f.write(f"{p['port']}\t{p['service']}\t{p['banner']}\n")
        print(f"\n[+] Results saved to {filename}")