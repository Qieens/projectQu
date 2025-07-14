import requests
import time
from jnius import autoclass

# ====== WakeLock ======
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
PowerManager = autoclass('android.os.PowerManager')
power = PythonActivity.mActivity.getSystemService(Context.POWER_SERVICE)
wake_lock = power.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, 'MyApp::WakeLock')
wake_lock.acquire()

# ====== Foreground Service Notification ======
Service = autoclass('org.kivy.android.PythonService')
service = Service.mService
if service is not None:
    notification = autoclass('android.app.Notification')
    notification_builder = autoclass('android.app.Notification$Builder')
    builder = notification_builder(PythonActivity.mActivity)
    builder.setContentTitle("AutoPost Discord")
    builder.setContentText("Layanan aktif dan berjalan di background.")
    builder.setSmallIcon(17301514)  # icon default Android
    service.startForeground(1, builder.build())

# ====== Load Config & Jalankan ======
with open("config.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

if len(lines) < 5:
    print("Konfigurasi tidak lengkap.")
    wake_lock.release()
    exit()

token_user, channel_list, message, total, delay = lines
id_channel = [c.strip() for c in channel_list.split(",") if c.strip()]
headers = {'Authorization': token_user}

for i in range(int(total)):
    print(f"Loop ke-{i+1}")
    for ch in id_channel:
        res = requests.post(f"https://discord.com/api/v10/channels/{ch}/messages",
                            headers=headers,
                            json={"content": message})
        print(f"Channel {ch} => {res.status_code}")
    time.sleep(int(delay))

wake_lock.release()
