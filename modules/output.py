#!/usr/bin/env python3

def print_banner():
    banner = """
\033[91m    ____       __                 \033[0m
\033[91m   / __/___ _/ /____  __________\033[0m
\033[91m  / _/ / _ `/ __/ _ \/ __/ __/ \033[0m
\033[91m /___/ \_,_/\__/\___/_/ /_/    \033[0m
\033[91m                                \033[0m
\033[93m    Professional Port Scanner   \033[0m
\033[93m    Red Team Edition v1.0       \033[0m
\033[90m    Owner Abid Afridi\033[0m
    """
    print(banner)

def print_results(results):
    if not results:
        print("\n\033[91m[-] No open ports found\033[0m")
        return
    
    print(f"\n\033[93m{'='*60}\033[0m")
    print(f"\033[92mOpen Ports Summary:\033[0m")
    print(f"\033[93m{'PORT':<10} {'SERVICE':<15} {'BANNER'}\033[0m")
    print(f"\033[93m{'-'*50}\033[0m")
    
    for r in results:
        banner_short = r['banner'][:40] if r['banner'] else "Unknown"
        print(f"{r['port']:<10} {r['service']:<15} {banner_short}")