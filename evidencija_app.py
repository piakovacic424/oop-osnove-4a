import tkinter as tk

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.prezime} {self.ime} ({self.razred})"

class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija Učenika")

       
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.ucenici = []
        self.odabrani_ucenik_index = None

       
        self.unos_frame = tk.Frame(self.root, padx=10, pady=10)
        self.unos_frame.grid(row=0, column=0, sticky="NSEW")

 
        self.unos_frame.columnconfigure(0, weight=0)
        self.unos_frame.columnconfigure(1, weight=1)

        tk.Label(self.unos_frame, text="Ime:").grid(row=0, column=0, sticky="W", pady=5)
        self.ime_entry = tk.Entry(self.unos_frame)
        self.ime_entry.grid(row=0, column=1, sticky="EW", pady=5)

        tk.Label(self.unos_frame, text="Prezime:").grid(row=1, column=0, sticky="W", pady=5)
        self.prezime_entry = tk.Entry(self.unos_frame)
        self.prezime_entry.grid(row=1, column=1, sticky="EW", pady=5)

        tk.Label(self.unos_frame, text="Razred:").grid(row=2, column=0, sticky="W", pady=5)
        self.razred_entry = tk.Entry(self.unos_frame)
        self.razred_entry.grid(row=2, column=1, sticky="EW", pady=5)

        self.dodaj_gumb = tk.Button(self.unos_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=3, column=1, sticky="E", pady=10)

        self.spremi_gumb = tk.Button(self.unos_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=4, column=1, sticky="E", pady=5)

        self.prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        self.prikaz_frame.grid(row=1, column=0, sticky="NSEW")

        self.prikaz_frame.columnconfigure(0, weight=1)
        self.prikaz_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(self.prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW", pady=10)

        scrollbar = tk.Scrollbar(self.prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)

    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()

        
        novi_ucenik = Ucenik(ime, prezime, razred)
        self.ucenici.append(novi_ucenik)
        self.osvjezi_prikaz()
        self.ocisti_unos()
        

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for ucenik in self.ucenici:
            self.listbox.insert(tk.END, str(ucenik))

    def odaberi_ucenika(self, event):
        odabrani = self.listbox.curselection()
        if not odabrani:
            return

        self.odabrani_ucenik_index = odabrani[0]
        ucenik = self.ucenici[self.odabrani_ucenik_index]

        self.ime_entry.delete(0, tk.END)
        self.ime_entry.insert(0, ucenik.ime)

        self.prezime_entry.delete(0, tk.END)
        self.prezime_entry.insert(0, ucenik.prezime)

        self.razred_entry.delete(0, tk.END)
        self.razred_entry.insert(0, ucenik.razred)

    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is None:
            return

        ucenik = self.ucenici[self.odabrani_ucenik_index]

        ucenik.ime = self.ime_entry.get().strip()
        ucenik.prezime = self.prezime_entry.get().strip()
        ucenik.razred = self.razred_entry.get().strip()

        self.osvjezi_prikaz()
        self.ocisti_unos()
        self.odabrani_ucenik_index = None

    def ocisti_unos(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")  
    app = EvidencijaApp(root)
    root.mainloop()
