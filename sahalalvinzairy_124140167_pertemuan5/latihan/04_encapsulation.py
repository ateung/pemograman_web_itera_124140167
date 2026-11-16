class Rekening:
    def __init__(self, pemilik, saldo):
        self.pemilik = pemilik
        self.__saldo = saldo

    @property
    def saldo(self):
        """Saldo bisa dibaca melalui property."""
        return self.__saldo

    def setor(self, jumlah):
        if jumlah > 0:
            self.__saldo += jumlah


rekening = Rekening("Sahal", 50000)
rekening.setor(10000)
print(f"Saldo {rekening.pemilik}: Rp{rekening.saldo}")
