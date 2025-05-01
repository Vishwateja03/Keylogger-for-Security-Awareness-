from cryptography.fernet import Fernet


def load_key():
    return open("encryption_key.key", "rb").read()


def decrypt_file(file_path):
    skey = load_key()
    fernet = Fernet(skey)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path, "wb") as file:
        file.write(decrypted_data)
    print(f"{file_path} decrypted successfully.")


files_to_decrypt = ["sysinfo.txt", "clipboard.txt"]


file_paths = "V:\\GURU\\projects\\Developing a keylogger for sec-analysis\\code\\"  


for file_name in files_to_decrypt:
    file_path = file_paths + file_name
    decrypt_file(file_path)
