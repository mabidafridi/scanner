#!/usr/bin/env python3

def print_banner():
    banner = r"""
     \           \      _|       _)      | _) 
    _ \         _ \    |     __|  |   _` |  | 
   ___ \       ___ \   __|  |     |  (   |  | 
 _/    _\ _) _/    _\ _|   _|    _| \__,_| _| 
                                              
    """
    # Clean up the raw string and apply colors
    for line in banner.strip().split('\n'):
        print(line)

def print_results(results):
    if not results:
        print("\n\033[91m[-] No open ports found\033[0m")
        return
    
    print(f"\n\033[93m{'='*60}\033[0m")
    print(f"\033[92mOpen Ports Summary:\033[0m")
    print(f"\033[93m{'PORT':<10} {'SERVICE':<15} {'BANNER'}\033[0m")
    print(f"\033[93m{'-'*50}\033[0m")
    
    for r in results:
        banner_short = r['banner'][:40] if r.get('banner') else "Unknown"
        print(f"{r['port']:<10} {r['service']:<15} {banner_short}")