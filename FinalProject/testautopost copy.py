from cryptography.fernet import Fernet
import requests, time, sys

def exit_with_message(msg):
    print(f"\n❌ {msg}")
    input("Klik ENTER untuk keluar...")
    sys.exit()

# ========== KUNCI TERSIMPAN DI DALAM KODE (EMBEDDED) ==========
key = b'FROmOZbfxr0RfdRh4nH2ixp_PZyzxZzvPjO1O4xOCdo='  # Ganti dengan milikmu

def decrypt_data(filename):
    try:
        fernet = Fernet(key)
        with open(filename, 'rb') as ef:
            encrypted_data = ef.read()

        decrypted = fernet.decrypt(encrypted_data).decode('utf-8')

        if 'CHANNELS:' not in decrypted or 'MESSAGE:' not in decrypted:
            raise ValueError("Format data terenkripsi salah.")

        parts = decrypted.split('MESSAGE:')
        channel_part = parts[0].replace('CHANNELS:', '').strip()
        message_part = parts[1].strip()

        channel_ids = [line.strip() for line in channel_part.splitlines() if line.strip()]
        if not channel_ids or not message_part:
            raise ValueError("Data terenkripsi tidak lengkap.")

        return channel_ids, message_part

    except Exception as e:
        exit_with_message(f"❌ Gagal mendekripsi: {e}")

# ========== INPUT DARI PENGGUNA ==========

token_user = input("🔑 Masukkan Token Anda: ").strip()

try:
    delaykirim = int(input("⏳ Jeda antar pengulangan (detik): ").strip())
    totalkirim = int(input("🔁 Jumlah pengulangan kirim: ").strip())
except ValueError:
    exit_with_message("Input angka tidak valid!")

# ========== CEK VALIDITAS TOKEN ==========

check_token = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': token_user})
if check_token.status_code != 200:
    exit_with_message("Token user tidak valid!")

# ========== DEKRIPSI DATA ==========

id_channel, message = decrypt_data('data_encrypted.txt')

# ========== SIAPKAN HEADER DAN KIRIM ==========

headers = { 'Authorization': token_user }

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