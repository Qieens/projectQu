from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
import pwinput
import os
import requests
import time
import threading
import sys
import json

console = Console()

APP_VERSION = "2.0"
LOG_FILE = "autoposter_config.json"

def menunggu_loop(detik):
    for sisa in range(detik, -1, -1):
        print(f"\r⏳ Menunggu {sisa // 60} menit {sisa % 60} detik sebelum loop berikutnya", end="", flush=True)
        time.sleep(1)
    print()

# ========== BANNER ==========
def banner():
    console.print(Panel(Text(f"🚀 Auto Poster Discord v{APP_VERSION}", justify="center", style="bold cyan")))
    console.print("[bold yellow]📌 Dibuat oleh @qieen[/bold yellow]\n")

# ========== ANIMASI TITIK ==========
def animasi_titik(teks="🔄 Memulai mengirimkan pesan", durasi=3, jeda=0.5):
    loop = int(durasi / jeda)
    for i in range(loop):
        titik = '.' * ((i % 3) + 1)
        sys.stdout.write(f"\r{teks}{titik}{' ' * (3 - len(titik))}")
        sys.stdout.flush()
        time.sleep(jeda)
    print()

# ========== VALIDASI TOKEN ==========
def get_valid_token():
    while True:
        token = pwinput.pwinput(prompt="🔑 Masukkan Token Anda (tersembunyi): ", mask="*")
        response = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': token})
        if response.status_code == 200:
            return token
        console.print("[red]❌ Token tidak valid! Silakan coba lagi.[/red]\n")

# ========== VALIDASI WEBHOOK ==========
def get_webhook_url():
    use_webhook = Confirm.ask("📣 Apakah Anda ingin mengirim log ke Webhook?")
    if use_webhook:
        while True:
            webhook_url = Prompt.ask("🔔 Masukkan Webhook URL")
            try:
                test = requests.post(webhook_url, json={"content": "✅ Webhook berhasil dihubungi!"})
                if test.status_code in [200, 204]:
                    console.print("[green]✔ Webhook valid![/green]\n")
                    return webhook_url
            except:
                pass
            console.print("[red]❌ Webhook tidak valid! Silakan coba lagi.[/red]\n")
    return ""

# ========== INPUT CHANNEL ==========
def get_channel_ids():
    console.print("📥 [bold]Masukkan ID Channel[/bold] (pisahkan per baris, akhiri dengan ENTER 2x):")
    result = [] 
    while True:
        line = input("> ").strip()
        if line == "":
            break
        if not line.isdigit():
            console.print(f"[red]❌ ID tidak valid: {line} (hanya angka diperbolehkan)[/red]")
            continue
        result.append(line)
    if not result:
        console.print("[red]❌ Minimal masukkan satu ID channel![/red]")
        return get_channel_ids()
    return result

# ========== INPUT PESAN ==========
def get_multiline_message():
    console.print("✉️ [bold]Masukkan pesan (boleh multi-baris, ENTER 2x untuk selesai)[/bold]:")
    lines = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        lines.append(line)
    message = "\n".join(lines).strip()
    if not message:
        console.print("[red]❌ Pesan tidak boleh kosong![/red]")
        return get_multiline_message()
    return message

# ========== INPUT DELAY ==========
def get_delay():
    while True:
        try:
            delay_minutes = int(Prompt.ask("⏳ Jeda antar pengulangan (menit)", default="1"))
            if delay_minutes <= 0:
                console.print("[red]❌ Nilai harus lebih dari 0 menit![/red]")
                continue
            return delay_minutes * 60
        except ValueError:
            console.print("[red]❌ Input angka tidak valid! Harus berupa bilangan bulat.[/red]")

# ========== KIRIM LOG ==========
def send_log_to_webhook(msg, webhook_url):
    if webhook_url:
        try:
            for i in range(3):
                console.print(f"[yellow]📡 Mengirimkan log ke webhook{'.' * (i + 1)}[/yellow]", end="\r")
                time.sleep(0.5)
            requests.post(webhook_url, json={"content": msg})
            console.print("\n[green]✅ Log berhasil dikirim ke webhook.[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️ Gagal mengirim log ke webhook: {e}[/yellow]")

# ========== SIMPAN KONFIGURASI ==========
def simpan_konfigurasi(token, webhook, channels, message, delay):
    config = {
        "token": token,
        "webhook": webhook,
        "channels": channels,
        "message": message,
        "delay": delay
    }
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)

# ========== MUAT KONFIGURASI ==========
def muat_konfigurasi():
    if os.path.exists(LOG_FILE):
        gunakan = Confirm.ask("📂 Konfigurasi sebelumnya ditemukan. Gunakan kembali?")
        if gunakan:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    return None

# ========== MAIN ==========
def main():
    banner()
    config = muat_konfigurasi()
    if config:
        token = config["token"]
        webhook = config["webhook"]
        channels = config["channels"]
        message = config["message"]
        delay = config["delay"]
    else:
        token = get_valid_token()
        webhook = get_webhook_url()
        channels = get_channel_ids()
        message = get_multiline_message()
        delay = get_delay()
        simpan_konfigurasi(token, webhook, channels, message, delay)

    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    animasi_titik()

    headers = {'Authorization': token}
    loop_count = 1
    try:
        while True:
            log_text = f"🔀 Loop ke-{loop_count}\n"
            console.print(f"\n[bold cyan]🔀 Loop ke-{loop_count}[/bold cyan]")

            for ch in channels:
                url = f"https://discord.com/api/v10/channels/{ch}/messages"
                try:
                    response = requests.post(url, headers=headers, json={'content': message})
                    status = f"[{ch}] Status: {response.status_code} - {response.reason}"
                except Exception as e:
                    status = f"[{ch}] Gagal mengirim: {e}"
                console.print(status)
                log_text += status + "\n"
                time.sleep(0.3)

            send_log_to_webhook(f"📢 Log Kirim:\n{log_text}", webhook)
            loop_count += 1
            menunggu_loop(delay)

    except KeyboardInterrupt:
        console.print("\n[bold red]⏹️ Dihentikan oleh pengguna.[/bold red]")
        send_log_to_webhook("⏹️ Dihentikan oleh pengguna.", webhook)

    exit_flag = False
    def animate_exit():
        dots = 0
        while not exit_flag:
            print(f"\rTekan ENTER untuk keluar{'.' * dots}{' ' * (3 - dots)}", end="", flush=True)
            dots = (dots + 1) % 4
            time.sleep(0.5)

    thread = threading.Thread(target=animate_exit)
    thread.start()
    try:
        input()
    finally:
        exit_flag = True
        thread.join()

# ========== RUN ==========
if __name__ == "__main__":
    main()
