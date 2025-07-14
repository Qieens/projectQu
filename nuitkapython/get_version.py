import re

MAINFILE = "main.py"

try:
    with open(MAINFILE, encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("0.0.1")  # fallback versi default jika file tidak ditemukan
    exit(0)

m = re.search(r'APP_VERSION\s*=\s*[\'"]([\w\.\-]+)[\'"]', content)

print(m.group(1) if m else "0.0.1")
