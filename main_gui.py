import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import requests
import time

APP_VERSION = "1.62"

def start_posting():
    token = token_entry.get().strip()
    webhook_url = webhook_entry.get().strip()
    channel_ids = channels_text.get("1.0", tk.END).strip().splitlines()
    message = message_text.get("1.0", tk.END).strip()
    try:
        delay = int(delay_entry.get())
        repeat = int(repeat_entry.get())
    except:
        messagebox.showerror("Error", "Delay dan repeat harus berupa angka!")
        return

    if not token or not channel_ids or not message:
        messagebox.showwarning("Input Salah", "Pastikan semua field terisi!")
        return

    headers = {'Authorization': token}

    def posting():
        for i in range(repeat):
            log_area.insert(tk.END, f"\n🌀 Loop ke-{i+1}\n")
            for ch in channel_ids:
                try:
                    response = requests.post(f"https://discord.com/api/v10/channels/{ch}/messages",
                                             headers=headers, json={'content': message})
                    status = f"[{ch}] Status: {response.status_code} - {response.reason}"
                except Exception as e:
                    status = f"[{ch}] Gagal mengirim: {e}"
                log_area.insert(tk.END, status + "\n")
                log_area.see(tk.END)
                time.sleep(1)
            if i < repeat - 1:
                log_area.insert(tk.END, f"⏳ Menunggu {delay} detik sebelum loop berikutnya...\n")
                time.sleep(delay)

        if webhook_url:
            try:
                requests.post(webhook_url, json={"content": f"✅ Semua pesan terkirim {repeat}x."})
                log_area.insert(tk.END, "\n✅ Log dikirim ke webhook.\n")
            except Exception as e:
                log_area.insert(tk.END, f"⚠️ Gagal kirim webhook: {e}\n")
        messagebox.showinfo("Selesai", "Pengiriman selesai!")

    threading.Thread(target=posting).start()

# === GUI Setup ===
root = tk.Tk()
root.title(f"Auto Poster Discord v{APP_VERSION}")

# Token
tk.Label(root, text="🔑 Token:").pack()
token_entry = tk.Entry(root, show="*", width=60)
token_entry.pack()

# Webhook (opsional)
tk.Label(root, text="🔔 Webhook URL (opsional):").pack()
webhook_entry = tk.Entry(root, width=60)
webhook_entry.pack()

# Channel ID
tk.Label(root, text="📥 ID Channel (satu per baris):").pack()
channels_text = scrolledtext.ScrolledText(root, height=4)
channels_text.pack()

# Pesan
tk.Label(root, text="✉️ Pesan:").pack()
message_text = scrolledtext.ScrolledText(root, height=6)
message_text.pack()

# Delay & Repeat
tk.Label(root, text="⏳ Delay (detik):").pack()
delay_entry = tk.Entry(root)
delay_entry.insert(0, "5")
delay_entry.pack()

tk.Label(root, text="🔁 Jumlah Kirim:").pack()
repeat_entry = tk.Entry(root)
repeat_entry.insert(0, "3")
repeat_entry.pack()

# Tombol kirim
tk.Button(root, text="🚀 Mulai Kirim", command=start_posting, bg="green", fg="white").pack(pady=10)

# Log Area
log_area = scrolledtext.ScrolledText(root, height=10)
log_area.pack()

# Jalankan
root.mainloop()
