import os
import time
import json

class Pet:
    interval = 20  # 20 detik = 1 "putaran"

    def __init__(self, name):
        self.name = name
        self.umur = 0
        self.bosan = 0
        self.kenyang = 100
        self.capek = 0
        self.hidup = True
        self.putaran_terakhir = time.time() # ini variable untuk putaran terakhir. pakai waktu sekarang pas programnya baru mulai

    def activity_makan(self):
        if self.kenyang <= 100:
            self.kenyang += 10
            return "Makan bang...", 3.5
        else:
            return "Dah kenyang", 1.5

    def activity_minum(self):
        if self.kenyang <= 100:
            self.kenyang += 0.5
            return "Lagi minum...", 2.5
        else:
            return "Dah kenyang", 1.5

    def activity_olahraga(self):
        if self.capek <= 35:
            self.kenyang -= 5
            self.bosan -= 10
            self.capek += 20
            return "Lagi olahraga...", 6
        else:
            return "Capek woy", 1.5
        
    def activity_main(self):
        if self.capek <= 50:
            self.kenyang -= 2
            self.bosan -= 20
            self.capek += 10
            return "Lagi asik main...", 4
        else:
            return "Capek woy", 1.5

    def activity_tidur(self):
        if self.capek >= 30:
            self.umur += 0.5
            self.capek = 0
            self.kenyang = 20
            return "Bobok...", 10
        else:
            return "Belum capek", 1.5

    # sistem waktu. `elapsed_time` didapat dari ngitung waktu sekarang dikurang putaran terakhir
    def pass_time(self, elapsed_time):
        self.umur += (elapsed_time / self.interval) * 0.2 # tiap 20 detik nambah 0.2
        self.bosan += (elapsed_time / self.interval) * 2.5
        self.kenyang -= (elapsed_time / self.interval) * 1
        self.capek += (elapsed_time / self.interval) * 0.5

        # kalau terlalu lapar/capek ya mati
        if self.kenyang < -20 or self.capek >= 100:
            self.hidup = False


    def status(self):
        return f"""
Nama: {self.name}
Umur: {round(self.umur)}
Kenyang: {self.kenyang:.2f}
Bosan: {self.bosan:.2f}
Capek: {self.capek:.2f}
-----------
"""

    def to_dict(self):
        return {
            "name": self.name,
            "umur": self.umur,
            "bosan": self.bosan,
            "kenyang": self.kenyang,
            "capek": self.capek,
            "hidup": self.hidup,
            "putaran_terakhir": self.putaran_terakhir
        }

    @classmethod
    def from_dict(cls, data):
        pet = cls(data["name"])
        pet.umur = data["umur"]
        pet.bosan = data["bosan"]
        pet.kenyang = data["kenyang"]
        pet.capek = data["capek"]
        pet.hidup = data["hidup"]
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
    name = input("Siapa nama peliharaanmu? ")
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
            print("  [6] Pilih/tambah peliharaan lain")
            choice = input()

            activities = {
                "1": pet.activity_makan,
                "2": pet.activity_minum,
                "3": pet.activity_olahraga,
                "4": pet.activity_main,
                "5": pet.activity_tidur,
                "6": start
            }

            activity = activities.get(choice)
            if activity:
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
