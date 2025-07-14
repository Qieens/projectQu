from cryptography.fernet import Fernet

# Key harus sama dengan yang ada di .exe
key = b'FROmOZbfxr0RfdRh4nH2ixp_PZyzxZzvPjO1O4xOCdo='  
fernet = Fernet(key)

with open('data.txt', 'rb') as file:
    original = file.read()

encrypted = fernet.encrypt(original)

with open('data_encrypted.txt', 'wb') as enc_file:
    enc_file.write(encrypted)

print("✅ Enkripsi selesai. File tersimpan sebagai 'data_encrypted.txt'")