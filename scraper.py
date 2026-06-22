import requests
import time

def save_keys_to_file():
    # Example logic: GitHub se keys nikalna
    # Yahan tumhara real scraping logic aayega
    new_keys = ["sk_live_12345", "sk_live_67890"] 
    with open("keys.txt", "w") as f:
        for key in new_keys:
            f.write(key + "\n")

# Har 30 minute mein keys update karega
while True:
    save_keys_to_file()
    time.sleep(1800)
