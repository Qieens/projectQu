import requests
import time
import sys



print("========================================")
print("   🚀 Script made by @qieen")
print("   💬 Auto Poster Discord v1.0")
print("========================================\n")

def exit_with_message(msg):
    print(f"\n❌ {msg}")
    input("Klik ENTER untuk keluar...")
    sys.exit()
    
# ========== INPUT DARI PENGGUNA ==========
token_user = input("🔑 Masukkan Token Anda: ").strip()
channel_file = 'idchannel.txt'
message_file = 'message.txt'

try:
    delaykirim = int(input("⏳ Jeda antar pengulangan (detik): ").strip())
    totalkirim = int(input("🔁 Jumlah pengulangan kirim: ").strip())
except ValueError:
    exit_with_message("Input angka tidak valid!")

# ========== CEK VALIDITAS TOKEN ==========
check_token = requests.get(
    "https://discord.com/api/v10/users/@me",
    headers={'Authorization': token_user}
)

if check_token.status_code != 200:
    exit_with_message("Token user tidak valid!")

# ========== BACA FILE PESAN ==========
ada_error = False

try:
    with open(message_file, 'r', encoding='utf-8') as mf:
        message = mf.read().strip()
except FileNotFoundError:
    print(f"❌ File '{message_file}' tidak ditemukan!")
    ada_error = True
else:
    if not message:
        print("❌ File 'message.txt' kosong! Harap isi dengan pesan yang ingin dikirim.")
        ada_error = True

# ========== BACA FILE CHANNEL ==========
try:
    with open(channel_file, 'r') as file:
        id_channel = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print(f"❌ File '{channel_file}' tidak ditemukan!")
    ada_error = True
else:
    if not id_channel:
        print("❌ File 'idchannel.txt' kosong! Harap isi dengan minimal 1 ID channel.")
        ada_error = True

# ========== KELUAR JIKA ADA ERROR ==========
if ada_error:
    input("Klik ENTER untuk keluar...")
    sys.exit()

# ========== SIAPKAN HEADER REQUEST ==========
headers = {
    'Authorization': token_user
}

# ========== MULAI PENGIRIMAN ==========
print("Script made by @qieen")
for i in range(totalkirim):
    print(f"\n🌀 Loop ke-{i + 1}")

    for channel_id in id_channel:
        url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
        data = {'content': message}

        response = requests.post(url, headers=headers, json=data)
        print(f"[{channel_id}] Status: {response.status_code} - {response.reason}")

    if i < totalkirim - 1:
        print(f"⏳ Menunggu {delaykirim} detik untuk loop berikutnya...")
        time.sleep(delaykirim)

print("\n✅ Semua pesan berhasil dikirim sebanyak", totalkirim, "kali.")
input("Press ENTER to close...")
