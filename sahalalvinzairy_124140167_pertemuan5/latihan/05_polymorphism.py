class Kucing:
    def bersuara(self):
        print("Meong")


class Anjing:
    def bersuara(self):
        print("Guk guk")


# Method sama, tetapi hasilnya mengikuti object yang digunakan.
for hewan in [Kucing(), Anjing()]:
    hewan.bersuara()
