import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print(f"Key generated and saved to '{KEY_FILE}'. Keep it safe!")

def load_key():
    if not os.path.exists(KEY_FILE):
        print("Key file not found! Please generate a key first (Option 1).")
        return None
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file(filename):
    key = load_key()
    if not key or not os.path.exists(filename):
        print("Error: Missing key or target file.")
        return

    cipher = Fernet(key)
    with open(filename, "rb") as f:
        data = f.read()

    encrypted_data = cipher.encrypt(data)
    enc_filename = filename + ".enc"
    with open(enc_filename, "wb") as f:
        f.write(encrypted_data)
    print(f"Success! Encrypted file saved as '{enc_filename}'.")

def decrypt_file(enc_filename):
    key = load_key()
    if not key or not os.path.exists(enc_filename):
        print("Error: Missing key or encrypted file.")
        return

    cipher = Fernet(key)
    with open(enc_filename, "rb") as f:
        encrypted_data = f.read()

    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        orig_filename = enc_filename.replace(".enc", "") if enc_filename.endswith(".enc") else "decrypted_" + enc_filename
        with open(orig_filename, "wb") as f:
            f.write(decrypted_data)
        print(f"Success! Decrypted file restored as '{orig_filename}'.")
    except Exception:
        print("Decryption failed! Invalid key or corrupted file.")

def main():
    while True:
        print("\n--- File Encryption & Decryption Tool ---")
        print("1. Generate Secret Key")
        print("2. Encrypt a File")
        print("3. Decrypt a File")
        print("4. Exit")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            generate_key()
        elif choice == "2":
            file_path = input("Enter the filename/path to encrypt: ").strip()
            encrypt_file(file_path)
        elif choice == "3":
            file_path = input("Enter the .enc filename/path to decrypt: ").strip()
            decrypt_file(file_path)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()