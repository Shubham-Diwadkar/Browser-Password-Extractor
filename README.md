# Browser-Password-Extractor

This script allows you to decrypt and retrieve saved passwords from the Google Chrome browser on Windows. It utilizes the Chrome SQLite database and encryption key to decrypt the passwords.

## Prerequisites

- [Python 3.8.0](https://www.python.org/downloads/release/python-380/)
- Cryptodome library 
```
pip install pycryptodomex
```
- Cryptography library
```
pip install cryptography
```

## Functionality
The functionality of the provided script can be summarized as follows:

1. Retrieves the encryption key used by Google Chrome to encrypt the saved passwords.
2. Copies the Chrome SQLite database containing the saved passwords to a temporary location.
3. Connects to the temporary database and executes a query to fetch the relevant data, including the website URLs, action URLs, usernames, encrypted passwords, creation dates, and last used dates.
4. Decrypts the passwords using the retrieved encryption key and displays the decrypted passwords along with other information.
5. Converts the timestamp values used by Chrome into human-readable date and time format.
6. Handles exceptions and errors gracefully, printing error messages when necessary.
7. Deletes the temporary database file after execution.

Essentially, the script allows you to decrypt and view saved passwords from the Google Chrome browser on a Windows system. It provides a convenient way to access passwords that are otherwise stored in an encrypted format.

[NOTE: Encryption Key can be updated by Google any time so it is possible that encryption and decryption may cause error]

## Usage

1. Install the required libraries by running the following commands:
```
pip install pycryptodomex
```
```
pip install cryptography
```
2. Save the script in a file with a `.py` extension (e.g., `Password_Extractor.py`).
3. Run the script using Python:
```
python Password_Extractor.py
```
4. The script will prompt for the Chrome profile name. Enter the profile name where the passwords are stored (e.g., `Profile 1`, `Profile 2`, etc.).
5. The script will decrypt and display the saved passwords from the Chrome browser, along with other relevant information like the website URL, username, and creation/last used dates.

## Explaination
The provided code is a tool that allows you to decrypt and retrieve saved passwords from the Google Chrome browser on a Windows system.

When you save passwords in Chrome, they are encrypted and stored in a SQLite database on your computer. This script utilizes the encryption key and SQLite database to decrypt the passwords and display them in plain text.

Here's how the script works:

1. It reads the Chrome local state file to obtain the encryption key used by Chrome to encrypt the passwords.
2. The script then constructs the path to the Chrome SQLite database file that contains the saved passwords.
3. It creates a temporary copy of the database file to work with, ensuring the original data remains intact.
4. The script connects to the temporary database and executes a query to retrieve the necessary information, including website URLs, action URLs, usernames, encrypted passwords, creation dates, and last used dates.
5. The encrypted passwords are decrypted using the encryption key obtained earlier, employing the AES encryption algorithm.
6. The decrypted passwords, along with the other relevant information, are displayed on the console output.
7. Timestamps used by Chrome for the creation and last used dates are converted to human-readable date and time format.
8. Exception handling is implemented to catch and display any errors that may occur during the execution of the script.
9. Finally, the temporary database file is deleted to maintain cleanliness.

By running this script, you can conveniently access and view your saved passwords from the Chrome browser, which can be helpful for password recovery or managing your credentials.

## Notes

- This script is specifically designed for Windows operating system and Chrome browser.
- The Chrome profile name is case-sensitive, so make sure to enter it correctly.
- The decrypted passwords will be displayed in the console output.
- The script creates a temporary copy of the Chrome SQLite database for decryption, which is deleted after execution.

## Disclaimer

Please note that extracting passwords without proper authorization may violate privacy and security laws. Ensure you have the necessary permissions and legal rights before using this script. This script is provided for educational purposes only.

## Ouput
![WhatsApp Image 2023-05-31 at 18 28 14](https://github.com/Shubham-Diwadkar/Browser-Password-Extractor/assets/125255910/fdd1f579-d8e8-4276-85b6-3e6d2f94beb5)

## License

This project is licensed under the [MIT License](LICENSE).

![Thankyou](https://github.com/Shubham-Diwadkar/Browser-Password-Extractor/assets/125255910/0f1cf481-13ab-4675-9066-0281cbf848e9)
