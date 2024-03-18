import os
import time
import json
import random
import math
from prettytable import PrettyTable

class Shop:
    items ={
        "1": {"nama": "Jamu kuat", "harga": 100, "deskripsi": "Jamu biar makin seterong", "efek": {"kenyang": 10, "bosan": -20, "capek": -20}},
        "2": {"nama": "Trofi", "harga": 1000, "deskripsi": "Sekedar pajangan", "efek": {}},
        "3": {"nama": "Penua instan", "harga": 500, "deskripsi": "Ya biar makin tua", "efek": {"umur": 10}},
        "4": {"nama": "Kopi", "harga": 100, "deskripsi": "Biar ngejreng", "efek": {"capek": -50}},
        "5": {"nama": "Ransum TNI", "harga": 300, "deskripsi": "Kenyang seharian. Jangan tanya dapat dari mana", "efek": {"kenyang": 100}},
        "6": {"nama": "Jamu Awet Muda Madura", "harga": 500, "deskripsi": "Katanya sih manjur", "efek": {"umur": -10}},
        "7": {"nama": "Yamaha Mio Gear 125 S", "harga": 5000, "deskripsi": "y.", "efek": {}}
    }

    def quicksort(arr, key, ascending=True):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2][key]
        left = [x for x in arr if x[key] < pivot]
        middle = [x for x in arr if x[key] == pivot]
        right = [x for x in arr if x[key] > pivot]
        if ascending:
            return Shop.quicksort(left, key, ascending) + middle + Shop.quicksort(right, key, ascending)
        else:
            return Shop.quicksort(right, key, ascending) + middle + Shop.quicksort(left, key, ascending)

    def jump_search(arr, key, value):
        sorted_items = Shop.quicksort(arr, key)
        n = len(sorted_items)
        step = int(math.sqrt(n)) 
        
        prev = 0
        while sorted_items[min(step, n) - 1][key] < value:
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                return None  
        
        while sorted_items[prev][key] < value:
            prev += 1
            if prev == min(step, n):
                return None
            
        if sorted_items[prev][key] == value:
            return sorted_items[prev]
        return None  

class Pet:
    interval = 20  # 20 detik = 1 "putaran"

    def __init__(self, name):
        self.name = name
        self.koin = 50
        self.umur = 0
        self.bosan = 0
        self.kenyang = 100
        self.capek = 0
        self.hidup = True
        self.barang = []
        self.putaran_terakhir = time.time() # ini variable untuk putaran terakhir. pakai waktu sekarang pas programnya baru mulai

        
    def activity_makan(self):
        if self.kenyang <= 100:
            if self.koin >= 10:
                self.kenyang += 10
                self.bosan -= 2
                self.koin -= 10
                return "Makan bang...", 3.5
            else:
                return "Koin gak cukup. Perlu 10 koin", 1.5
        else:
            return "Dah kenyang", 1.5

    def activity_minum(self):
        if self.kenyang <= 100:
            if self.koin >= 10:
                self.kenyang += 0.5
                self.bosan -= 1
                self.koin -= 5
                return "Lagi minum...", 2.5
            else:
                return "Koin gak cukup. Perlu 5 koin", 1.5
        else:
            return "Dah kenyang", 1.5

    def activity_olahraga(self):
        if self.capek <= 50:
            self.kenyang -= 5
            self.bosan -= 10
            self.capek += 20
            return "Lagi olahraga...", 6
        else:
            return "Capek woy", 1.5
        
    def activity_main(self):
        if self.capek <= 75:
            self.kenyang -= 2
            self.bosan -= 20
            self.capek += 10
            koin_didapat = random.randint(10,35)
            self.koin += koin_didapat
            print ("Lagi asik main...")
            time.sleep(4)
            return f"Hore, dapet {koin_didapat} koin", 1.5
        else:
            return "Capek woy", 1.5

    def activity_tidur(self):
        if self.capek >= 30:
            self.umur += 0.5
            self.capek = 0
            self.kenyang = 20
            self.bosan = 50
            return "Bobok...", 10
        else:
            return "Belum capek", 1.5

    # sistem waktu. `elapsed_time` didapat dari ngitung waktu sekarang dikurang putaran terakhir
    def pass_time(self, elapsed_time):
        self.umur += (elapsed_time / self.interval) * 0.02 # tiap 20 detik nambah 0.02
        self.bosan += (elapsed_time / self.interval) * 0.1
        self.kenyang -= (elapsed_time / self.interval) * 0.05
        self.capek += (elapsed_time / self.interval) * 0.05

        # kalau terlalu lapar/capek ya mati
        if self.kenyang < -20 or self.capek >= 100:
            self.hidup = False


    def status(self):
        return f"""
Nama: {self.name}
Koin: {self.koin}
Umur: {round(self.umur)}
Kenyang: {self.kenyang:.2f}
Bosan: {self.bosan:.2f}
Capek: {self.capek:.2f}
-----------
"""
    
    def activity_shop(self):
        while True:
            os.system("cls")
            table = PrettyTable()
            table.clear()
            table.field_names = ["ID", "Barang", "Harga"]

            try:
                for item in sorted_items:
                    for item_id, item_info in Shop.items.items():
                        if item_info == item:
                            table.add_row([item_id, item_info['nama'], item_info['harga']])
                            break
            except:
                for item_id, item_info in Shop.items.items():
                    table.add_row([item_id, item_info['nama'], item_info['harga']])

            print("Selamat datang di toko!")
            print("Barang-barang yang tersedia:")
            print(table)

            print("\n[1] Beli barang")
            print("[2] Lihat info barang")
            print("[3] Urutkan barang")
            print("[4] Cari barang")
            print("[5] Kembali")
            choice = input("Masukkan pilihan anda: ")

            if choice == "1":
                item_id = input("Masukkan ID barang yang mau kamu beli (atau 'exit' untuk keluar): ")
                if item_id == 'exit':
                    break
                chosen_item = Shop.items.get(item_id)
                if chosen_item:
                    amount = int(input("Masukkan jumlah yang mau dibeli: "))
                    print(self.beli_barang(item_id, amount))
                    input("Tekan Enter untuk lanjut...")
                else:
                    print("ID barang gak valid")
                    input("Tekan Enter untuk lanjut...")
            elif choice == "2":
                item_id = input("Masukkan ID barang yang mau kamu lihat (atau 'exit' untuk keluar): ")
                if item_id == 'exit':
                    break
                chosen_item = Shop.items.get(item_id)
                if chosen_item:
                    print(f"\nNama barang: {chosen_item['nama']}")
                    print(f"Harga: {chosen_item['harga']} koin")
                    print(f"Deskripsi: {chosen_item['deskripsi']}")
                    print("Efek:")
                    for effect, value in chosen_item['efek'].items():
                        print(f"- {effect.capitalize()}: {value}")
                else:
                    print("ID barang gak valid")
                input("\nTekan Enter untuk lanjut...")
            elif choice == "3":
                print("Urut Berdasarkan:")
                print("[1] Harga")
                print("[2] Nama")
                sort_option = input()
                print("\nMetode:")
                print("[1] Ascending")
                print("[2] Descending")
                sort_order = input()

                if sort_option == "1":
                    # parameter ascendingnya langsung ngembaliin boolean berdasar apakah sort_order == '1'
                    sorted_items = Shop.quicksort(list(Shop.items.values()), 'harga', ascending = sort_order == "1")
                elif sort_option == "2":
                    sorted_items = Shop.quicksort(list(Shop.items.values()), 'nama', ascending = sort_order == "1")
                
                else:
                    print("Opsi tidak valid")
                    input("Tekan Enter untuk lanjut...")
                    continue
            
            elif choice == "4":
                print("Cari berdasarkan:")
                print("[1] Harga")
                print("[2] Nama")
                option = input()
                
                if option == "1":
                    key = "harga"
                    value = int(input("Masukkan harga yang mau dicari: "))
                elif option == "2":
                    key = "nama"
                    value = input("Masukkan nama yang mau dicari: ")
                else:
                    print("Opsi tidak valid")
                    input("Tekan Enter untuk lanjut...")
                    break
                    
                item = Shop.jump_search(list(Shop.items.values()), key, value)
                if item:
                    print("\nBarang ketemu")
                    print(f"Nama barang: {item['nama']}")
                    print(f"Harga: {item['harga']} koin")
                    print(f"Deskripsi: {item['deskripsi']}")
                    print("Efek:")
                    for effect, value in item['efek'].items():
                        print(f"- {effect.capitalize()}: {value}")
                else:
                    print("Item tidak ditemukan.")
                input("\nTekan Enter untuk lanjut...")

            elif choice == "5":
                break
            else:
                print("Pilihan gak valid")
                input("Tekan Enter untuk lanjut...")


    def beli_barang(self, item_id, amount=1):
        chosen_item = Shop.items.get(item_id)
        if chosen_item:
            if self.koin >= chosen_item["harga"] * amount:
                total_price = chosen_item["harga"] * amount
                self.koin -= total_price
                # Cek barang ada di inventory atau nggak
                for item in self.barang:
                    if item['id'] == item_id:
                        item['jumlah'] += amount
                        break
                else:
                    self.barang.append({"id": item_id, "nama": chosen_item['nama'], "harga": chosen_item['harga'], "jumlah": amount})
                self.save_to("pets.json")
                return f"Kamu membeli {amount} {chosen_item['nama']}!"
            else:
                return "Koin gak cukup"
        else:
            return "Pilihan gak valid"
    

    def activity_inventory(self):
        while True:
            os.system("cls")
            
            table = PrettyTable()
            table.clear()
            table.field_names = ["Index", "Barang", "Harga", "Jumlah"]

            try:
                for item in sorted_items:
                    for i, item_info in enumerate(self.barang):
                        if item_info['nama'] == item['nama']:
                            table.add_row([i+1, item_info['nama'], item_info['harga'], item_info['jumlah']])
                            break
            except:
                for i, item in enumerate(self.barang, start=1):
                    table.add_row([i, item['nama'], item['harga'], item['jumlah']])

            print("Barang-barangmu:")
            print(table)

            print("\n[1] Pakai barang")
            print("[2] Lihat info barang")
            print("[3] Urutkan barang")
            print("[4] Cari barang")
            print("[5] Kembali")
            choice = input("Masukkan pilihanmu: ")

            if choice == "1":
                item_index = int(input("Masukkan index barang yang mau kamu pakai (atau 'exit' untuk keluar): "))
                if item_index == 'exit':
                    break
                if 1 <= item_index <= len(self.barang):
                    chosen_item = self.barang[item_index - 1]
                    if Shop.items.get(chosen_item['id'])['efek']:
                        amount_to_use = int(input("Masukkan jumlah yang mau dipakai: "))
                        if amount_to_use > chosen_item['jumlah']:
                            print("Kamu gak punya segitu")
                        else:
                            for attr, value in Shop.items.get(chosen_item['id'])['efek'].items():
                                setattr(self, attr, getattr(self, attr) + value * amount_to_use)
                            chosen_item['jumlah'] -= amount_to_use
                            if chosen_item['jumlah'] == 0:
                                self.barang.pop(item_index - 1)  
                            print(f"Kamu memakai {amount_to_use} {chosen_item['nama']}!")
                        input("Tekan Enter untuk lanjut...")
                else:
                    print("Index tidak valid!")
                    input("Tekan Enter untuk lanjut...")
            elif choice == "2":
                item_index = int(input("Masukkan index barang yang mau kamu lihat (atau 'exit' untuk keluar): "))
                if item_index == 'exit':
                    break
                if 1 <= item_index <= len(self.barang):
                    chosen_item = self.barang[item_index - 1]
                    print(f"\nNama barang: {chosen_item['nama']}")
                    print(f"Harga: {chosen_item['harga']} koin")
                    print(f"Jumlah: {chosen_item['jumlah']}")
                    print(f"Deskripsi: {Shop.items.get(chosen_item['id'])['deskripsi']}")
                    print("Efek:")
                    if Shop.items.get(chosen_item['id'])['efek']:
                        for effect, value in Shop.items.get(chosen_item['id'])['efek'].items():
                            print(f"- {effect.capitalize()}: {value}")
                    else:
                        print("Tidak ada")
                    input("\nTekan Enter untuk lanjut...")
                else:
                    print("Index tidak valid!")
                    input("Tekan Enter untuk lanjut...")
            elif choice == "3":
                print("Urut Berdasarkan:")
                print("[1] Harga")
                print("[2] Nama")
                print("[3] Jumlah")
                sort_option = input()
                print("\nMetode:")
                print("[1] Ascending")
                print("[2] Descending")
                sort_order = input()

                if sort_option == "1":
                    # parameter ascendingnya langsung ngembaliin boolean berdasar apakah sort_order == '1'
                    sorted_items = Shop.quicksort(self.barang, 'harga', ascending = sort_order == "1")
                elif sort_option == "2":
                    sorted_items = Shop.quicksort(self.barang, 'nama', ascending = sort_order == "1")
                elif sort_option == "3":
                    sorted_items = Shop.quicksort(self.barang, 'jumlah', ascending = sort_order == "1")
                else:
                    print("Opsi tidak valid")
                    input("Tekan Enter untuk lanjut...")
                    continue

            elif choice == "4":
                print("Cari berdasarkan:")
                print("[1] Harga")
                print("[2] Nama")
                print("[3] Jumlah")
                option = input()
                
                if option == "1":
                    key = "harga"
                    value = int(input("Masukkan harga yang mau dicari: "))
                elif option == "2":
                    key = "nama"
                    value = input("Masukkan nama yang mau dicari: ")
                elif option == "3":
                    key = "jumlah"
                    value = int(input("Masukkan jumlah yang mau dicari: "))
                else:
                    print("Opsi tidak valid")
                    input("Tekan Enter untuk lanjut...")
                    break
                    
                item = Shop.jump_search(self.barang, key, value)
                if item:
                    print("\nBarang ketemu")
                    print(f"Nama barang: {item['nama']}")
                    print(f"Harga: {item['harga']} koin")
                    print(f"Deskripsi: {Shop.items[item['id']]['deskripsi']}")
                    print("Efek:")
                    for effect, value in Shop.items[item['id']]['efek'].items():
                        print(f"- {effect.capitalize()}: {value}")
                else:
                    print("Item tidak ditemukan.")
                input("\nTekan Enter untuk lanjut...")

            elif choice == "5":
                break
            else:
                print("Opsi tidak valid!")
                input("Tekan Enter untuk lanjut...")

    def to_dict(self):
        return {
            "name": self.name,
            "koin": self.koin,
            "umur": self.umur,
            "bosan": self.bosan,
            "kenyang": self.kenyang,
            "capek": self.capek,
            "hidup": self.hidup,
            "barang": self.barang,
            "putaran_terakhir": self.putaran_terakhir
        }

    @classmethod
    def from_dict(cls, data):
        pet = cls(data["name"])
        pet.koin = data.get("koin",0)
        pet.umur = data["umur"]
        pet.bosan = data["bosan"]
        pet.kenyang = data["kenyang"]
        pet.capek = data["capek"]
        pet.hidup = data["hidup"]
        pet.barang = data.get("barang", [])
        pet.putaran_terakhir = data["putaran_terakhir"]
        return pet

    @staticmethod
    def load_from(file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data = json.load(file)
                return {name: Pet.from_dict(pet_data) for name, pet_data in data.items()}
        else:
            with open(file_name, "w") as file:
                file.write("{}")
            return {}

    def save_to(self, file_name):
        pet_data = self.to_dict()
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data = json.load(file)
        else:
            data = {}
        data[self.name] = pet_data
        with open(file_name, "w") as file:
            json.dump(data, file)
    
    def delete_from(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                data = json.load(file)
                if self.name in data:
                    del data[self.name]
                    with open(file_name, "w") as file:
                        json.dump(data, file)


def start():
    os.system("cls")
    pets = Pet.load_from("pets.json")

    # anggap aja ini sistem "login"-nya. Kalau nama petnya udah ada di file, datanya pakai yang udah ada juga
    name = input("Siapa nama peliharaanmu?\n(Gunakan nama peliharaan yang sudah ada untuk melanjutkan progress)\n")
    if name in pets:
        pet = pets[name]
    else:
        pet = Pet(name)

    pet.pass_time(time.time() - pet.putaran_terakhir) # buat refresh status hidup
    while pet.hidup:
        os.system("cls")
        current_time = time.time()
        elapsed_time = current_time - pet.putaran_terakhir # nih bagian yang ngitung waktu sudah berapa lama jalan
        pet.pass_time(elapsed_time)
        pet.putaran_terakhir = current_time
        pet.save_to("pets.json")
        print(pet.status())

        while True:
            print("[?] Ngapain ya?")
            print("  [1] Makan")
            print("  [2] Minum")
            print("  [3] Olahraga")
            print("  [4] Main")
            print("  [5] Tidur")
            print("  [6] Belanja")
            print("  [7] Lihat barang")
            print("  [8] Pilih/tambah peliharaan lain")
            choice = input()

            activities = {
                "1": pet.activity_makan,
                "2": pet.activity_minum,
                "3": pet.activity_olahraga,
                "4": pet.activity_main,
                "5": pet.activity_tidur,
                "6": pet.activity_shop,
                "7": pet.activity_inventory,
                "8": start
            }

            activity = activities.get(choice)
            if activity:
                if choice in ["6", "7"]:
                    activity()
                    break
                else:
                    status, sleep = activity()
                    print(status)
                    time.sleep(sleep)
                    break
            else:
                print("Pilihan tidak valid. Silahkan pilih angka 1-6")
                time.sleep(1.5)
                os.system("cls")
                pet.pass_time(1.5)
                print(pet.status())

    os.system("cls")
    print(f"{pet.name} mati :((((((((")
    print("-----------")
    print(f"Stats terakhir:\n{pet.status()}")
    pet.delete_from("pets.json") # hapus dari file kalau mati


start()
