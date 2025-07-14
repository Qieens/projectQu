import os
import re

# Baca versi dari main.py
with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Cari APP_VERSION
match = re.search(r'APP_VERSION\s*=\s*"([\d\.]+)"', content)
version = match.group(1) if match else "0.0.1"

exe_name = f"AutoPoster-v{version}"
command = f"pyinstaller --onefile --strip --clean --name \"{exe_name}\" main.py"

print(f"[🔧] Membuat .exe dengan nama: {exe_name}.exe")
os.system(command)