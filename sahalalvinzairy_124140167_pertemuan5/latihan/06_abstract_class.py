from abc import ABC, abstractmethod


class Bentuk(ABC):
    @abstractmethod
    def luas(self):
        """Subclass harus menyediakan cara menghitung luas."""
        raise NotImplementedError


class Persegi(Bentuk):
    def __init__(self, sisi):
        self.sisi = sisi

    def luas(self):
        return self.sisi * self.sisi


persegi = Persegi(4)
print("Luas persegi:", persegi.luas())
