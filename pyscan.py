#!/usr/bin/env python3
"""
PyScan - Professional Port Scanner
Usage: pyscan <target> [options]
"""

import sys
import os
import argparse

# Add modules path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.scanner import PortScanner
from modules.output import print_banner, print_results

def main():
    parser = argparse.ArgumentParser(
        description="PyScan - Fast Port Scanner for Red Teams",
        epilog="Example: pyscan 192.168.1.1 -p 1-1000"
    )
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (1-1000 or 22,80,443)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads (default: 100)")
    parser.add_argument("-o", "--output", help="Save results to file")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout")
    parser.add_argument("--no-banner", action="store_true", help="Disable banner grabbing")
    
    args = parser.parse_args()
    
    print_banner()
    
    scanner = PortScanner(
        target=args.target,
        ports=args.ports,
        threads=args.threads,
        timeout=args.timeout,
        grab_banner=not args.no_banner
    )
    
    results = scanner.scan()
    print_results(results)
    
    if args.output:
        scanner.save_results(args.output)

if __name__ == "__main__":
    main()