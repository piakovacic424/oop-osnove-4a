class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"

if __name__ == "__main__":
    # Testiramo kreiranje objekta
    ucenik = Ucenik("Pero", "Perić", "4.a")
    print(ucenik)

import tkinter as tk

class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija Učenika")
        
        # Listu učenika ćemo držati u ovoj varijabli
        self.ucenici = []
        
        # Glavni okvir (root)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Unosni okvir (Frame)
        self.unos_frame = tk.Frame(self.root, padx=10, pady=10)
        self.unos_frame.grid(row=0, column=0, sticky="NSEW")

        # Konfiguracija stupaca
        self.unos_frame.columnconfigure(1, weight=1)

        # Polja za unos (ime, prezime, razred)
        tk.Label(self.unos_frame, text="Ime:").grid(row=0, column=0, sticky="W", pady=5)
        self.ime_entry = tk.Entry(self.unos_frame)
        self.ime_entry.grid(row=0, column=1, sticky="EW", pady=5)

        tk.Label(self.unos_frame, text="Prezime:").grid(row=1, column=0, sticky="W", pady=5)
        self.prezime_entry = tk.Entry(self.unos_frame)
        self.prezime_entry.grid(row=1, column=1, sticky="EW", pady=5)

        tk.Label(self.unos_frame, text="Razred:").grid(row=2, column=0, sticky="W", pady=5)
        self.razred_entry = tk.Entry(self.unos_frame)
        self.razred_entry.grid(row=2, column=1, sticky="EW", pady=5)

        # Gumb za unos učenika
        self.dodaj_gumb = tk.Button(self.unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3, column=1, sticky="E", pady=10)

        # Okvir za prikaz liste učenika
        self.prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        self.prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        self.prikaz_frame.columnconfigure(0, weight=1)

        # Listbox za prikaz učenika
        self.listbox = tk.Listbox(self.prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW", pady=10)

        # Scrollbar za listbox
        scrollbar = tk.Scrollbar(self.prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Povezivanje događaja za selekciju učenika
        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)

    def dodaj_ucenika(self):
        ime = self.ime_entry.get()
        prezime = self.prezime_entry.get()
        razred = self.razred_entry.get()
        
        # Stvoriti novog učenika i dodati ga u listu
        novi_ucenik = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi_ucenik)
        
        # Osvježiti prikaz liste
        self.osvjezi_prikaz()

    def osvjezi_prikaz(self):
        # Očistiti postojeće stavke u listbox-u
        self.listbox.delete(0, tk.END)
        
        # Dodati nove stavke iz liste učenika
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))

    def odaberi_ucenika(self, event):
        # Dohvatiti indeks odabranog učenika
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return
        odabrani_index = odabrani_indeksi[0]
        odabrani_ucenik = self.ucenici[odabrani_index]
        
        # Popuniti polja za unos s podacima odabranog učenika
        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, odabrani_ucenik.ime)
        
        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, odabrani_ucenik.prezime)
        
        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, odabrani_ucenik.razred)



    def spremi_izmjene(self):
        # Dohvatiti selektirani indeks i odabrani učenik
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return
        odabrani_index = odabrani_indeksi[0]
        odabrani_ucenik = self.ucenici[odabrani_index]
        
        # Ažurirati podatke učenika
        odabrani_ucenik.ime = self.ime_entry.get()
        odabrani_ucenik.prezime = self.prezime_entry.get()
        odabrani_ucenik.razred = self.razred_entry.get()
        
        # Osvježiti prikaz
        self.osvjezi_prikaz()

        self.spremi_gumb = tk.Button(self.unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=4, column=1, sticky="E", pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()







