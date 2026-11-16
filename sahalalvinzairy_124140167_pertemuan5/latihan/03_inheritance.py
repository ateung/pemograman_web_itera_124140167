class Kendaraan:
    def __init__(self, merek):
        self.merek = merek

    def bergerak(self):
        print(f"{self.merek} sedang bergerak.")


class Sepeda(Kendaraan):
    def bunyikan_bel(self):
        print("Kring kring!")


sepeda = Sepeda("Sepeda lipat")
sepeda.bergerak()
sepeda.bunyikan_bel()
