class BankovniRačun:
    def __init__(self,ime_vlasnika,broj_računa):
        self.ima_vlasnika=ime_vlasnika
        self.broj_računa=broj_računa
        self.stanje=0.0
    
    def uplati(self,iznos):
        if iznos>0:
            self.stanje+=iznos
            print(f"Uplata od {iznos:.2f} je uspiješna. Stanje računa je {self.stanje}")
        else:
            print("Iznos mora biti pozitivan broj.")
    
    def isplati(self,iznos):
        if iznos<=0:
            print("Iznos mora biti pozitivan broj.")
        elif self.stanje>=iznos:
            self.stanje-=iznos
            print(f"Isplata od {iznos:.2f} je uspiješna. Stanje računa je {self.stanje:.2f}")   
        else:
            print(f"Greška pri isplati. Nedovoljno sredstava.")

    def info(self):
        print(f"Vlasnik računa: {self.ima_vlasnika}")
        print(f"Broj računa: {self.broj_računa}")
        print(f"Stanje računa: {self.stanje:.2f}")

račun1=BankovniRačun("Agata Galant","HR1234567890123456789")
račun2=BankovniRačun("Pia Kovačić","HR9876543210987654321")

račun1.stanje=10000.0
račun2.stanje=5000.0
račun1.isplati(1500.0)
račun1.info()
račun2.uplati(2000.0)
račun2.info()
    
    