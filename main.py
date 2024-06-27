import random

import request_data_server

if __name__ == '__main__':
    request_data_server.post_new_user("TELEGRAMID" + str(random.randint(0, 999999)))



# def decrypt_string(encrypted_text: str, key: bytes) -> str:
#     encrypted_data = base64.b64decode(encrypted_text)
#     iv = encrypted_data[:16]
#     encrypted_data = encrypted_data[16:]
#
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
#     decryptor = cipher.decryptor()
#
#     decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
#
#     unpadder = PKCS7(algorithms.AES.block_size).unpadder()
#     decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
#
#     return decrypted_data.decode()


# password = "your_password"
# salt = os.urandom(16)  # Save this salt for decryption
# key = generate_key_from_password(password, salt)
#
# plain_text = "This is a secret message."
# encrypted_text = encrypt_string(plain_text, key)
#
# print("Salt (base64):", base64.b64encode(salt).decode())
# print("Encrypted text:", encrypted_text)
#
# # Decryption
# decoded_salt = base64.b64decode(base64.b64encode(salt).decode())  # Simulating the saved salt retrieval
# key_for_decryption = generate_key_from_password(password, decoded_salt)
# decrypted_text = decrypt_string(encrypted_text, key_for_decryption)

# print("Decrypted text:", decrypted_text)
