import json
import re
import time
import itertools
import sys
from tqdm import tqdm
from urllib.parse import urlparse
from colorama import Fore

# Fungsi untuk mengambil URL dari teks
def extract_urls(text):
    url_pattern = r'https?://\S+'  # Regex untuk URL
    return re.findall(url_pattern, text)

# Fungsi untuk mengambil hanya domain dari URL
def extract_domains(urls):
    domains = set()
    for url in urls:
        parsed_url = urlparse(url)
        domains.add(parsed_url.netloc)
    return domains

# Menampilkan banner
print(Fore.GREEN + """

▓█████▒██   ██▄▄▄█████▓██▀███  ▄▄▄      ▄████▄ ▒██   ██▓██   ██▓
▓█   ▀▒▒ █ █ ▒▓  ██▒ ▓▓██ ▒ ██▒████▄   ▒██▀ ▀█ ▒▒ █ █ ▒░▒██  ██▒
▒███  ░░  █   ▒ ▓██░ ▒▓██ ░▄█ ▒██  ▀█▄ ▒▓█    ▄░░  █   ░ ▒██ ██░
▒▓█  ▄ ░ █ █ ▒░ ▓██▓ ░▒██▀▀█▄ ░██▄▄▄▄██▒▓▓▄ ▄██▒░ █ █ ▒  ░ ▐██▓░
░▒████▒██▒ ▒██▒ ▒██▒ ░░██▓ ▒██▒▓█   ▓██▒ ▓███▀ ▒██▒ ▒██▒ ░ ██▒▓░
░░ ▒░ ▒▒ ░ ░▓ ░ ▒ ░░  ░ ▒▓ ░▒▓░▒▒   ▓▒█░ ░▒ ▒  ▒▒ ░ ░▓ ░  ██▒▒▒ 
 ░ ░  ░░   ░▒ ░   ░     ░▒ ░ ▒░ ▒   ▒▒ ░ ░  ▒  ░░   ░▒ ░▓██ ░▒░ 
   ░   ░    ░   ░       ░░   ░  ░   ▒  ░        ░    ░  ▒ ▒ ░░  
   ░  ░░    ░            ░          ░  ░ ░      ░    ░  ░ ░     
                                       ░                ░ ░  
""") 
print(Fore.RED + "\nFileExtracxy : Domain JsonFile Extract tool")

# Meminta input nama file dari pengguna
input_file = input(Fore.CYAN + "Masukkan nama file JSON (misalnya file.json): ")
output_file = input(Fore.CYAN + "Masukkan nama file output (misalnya output.txt): ")

# Memilih mode ekstraksi
print(Fore.YELLOW + "\nPilih mode ekstraksi:")
print("1. URL lengkap (termasuk parameter)")
print("2. Hanya domain")
choice = input(Fore.CYAN + "Masukkan 1 atau 2: ")

# Menampilkan loading
print(Fore.CYAN + "\nMemulai ekstraksi...")
for _ in tqdm(range(100), desc="Extracting...", ncols=100, ascii=True, colour='yellow'):
    time.sleep(0.01)

# Menyimpan URL yang ditemukan dalam set untuk menghindari duplikat
unique_urls = set()

# Membaca dan memproses file JSON
try:
    with open(input_file, 'r') as f:
        data = json.load(f)  # Menganggap data JSON adalah dictionary

        # Loop untuk mencari URL di dalam data JSON
        def search_json(data):
            if isinstance(data, dict):
                for value in data.values():
                    search_json(value)
            elif isinstance(data, list):
                for item in data:
                    search_json(item)
            elif isinstance(data, str):
                urls = extract_urls(data)
                unique_urls.update(urls)

        search_json(data)

    # Menentukan output berdasarkan pilihan pengguna
    if choice == "2":
        result = extract_domains(unique_urls)
    else:
        result = unique_urls

    # Menampilkan spinner saat menyimpan hasil
    print(Fore.CYAN + "\nMenyimpan hasil...")

    spinner = itertools.cycle(['|', '/', '-', '\\'])
    for _ in range(20):
        sys.stdout.write(Fore.YELLOW + '\r' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)

    # Menulis hasil ke file teks (menggunakan mode 'a' untuk menambahkan hasil)
    with open(output_file, 'a') as f:  # Mode 'a' untuk append
        for item in result:
            f.write(item + '\n')

    print(Fore.GREEN + f'\nEkstraksi selesai! Hasil disimpan dalam {output_file} ✅')

except FileNotFoundError:
    print(Fore.RED + f"File '{input_file}' tidak ditemukan. Pastikan nama file benar.")
except json.JSONDecodeError:
    print(Fore.RED + f"File '{input_file}' bukan file JSON yang valid.")
