import tkinter as tk
from tkinter import messagebox
import csv

class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime} - {self.email} - {self.telefon}"

class ImenikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jednostavni digitalni imenik")
        self.kontakti = []

        # Omogući rastezanje glavnog prozora
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Glavni frame
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="NSEW")

        # Konfiguracija kolona i redova za rastezanje
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=0)
        self.frame.rowconfigure(4, weight=1)  # Listbox

        # Unos podataka
        tk.Label(self.frame, text="Ime:").grid(row=0, column=0, sticky="W")
        self.ime_entry = tk.Entry(self.frame)
        self.ime_entry.grid(row=0, column=1, columnspan=2, sticky="EW")

        tk.Label(self.frame, text="Email:").grid(row=1, column=0, sticky="W")
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=1, column=1, columnspan=2, sticky="EW")

        tk.Label(self.frame, text="Telefon:").grid(row=2, column=0, sticky="W")
        self.telefon_entry = tk.Entry(self.frame)
        self.telefon_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

        # Gumb za dodavanje
        self.dodaj_button = tk.Button(self.frame, text="Dodaj kontakt", command=self.dodaj_kontakt)
        self.dodaj_button.grid(row=3, column=0, columnspan=3, pady=10, sticky="EW")

        # Listbox i Scrollbar
        self.listbox = tk.Listbox(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.grid(row=4, column=0, columnspan=2, sticky="NSEW")
        self.scrollbar.grid(row=4, column=2, sticky="NS")

        # Gumbi na dnu
        self.spremi_button = tk.Button(self.frame, text="Spremi kontakte", command=self.spremi_kontakte)
        self.spremi_button.grid(row=5, column=0, pady=10, sticky="EW")

        self.ucitaj_button = tk.Button(self.frame, text="Učitaj kontakte", command=self.ucitaj_kontakte)
        self.ucitaj_button.grid(row=5, column=1, pady=10, sticky="EW")

        # BONUS: Obriši kontakt
        self.obrisi_button = tk.Button(self.frame, text="Obriši odabrani kontakt", command=self.obrisi_kontakt)
        self.obrisi_button.grid(row=6, column=0, columnspan=3, sticky="EW", pady=5)

        # Automatski učitaj kontakte pri pokretanju
        self.ucitaj_kontakte()

    def dodaj_kontakt(self):
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.telefon_entry.get().strip()

        if ime and email and telefon:
            kontakt = Kontakt(ime, email, telefon)
            self.kontakti.append(kontakt)
            self.osvjezi_listbox()

            # Očisti polja
            self.ime_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.telefon_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena!")

    def osvjezi_listbox(self):
        self.listbox.delete(0, tk.END)
        for kontakt in self.kontakti:
            self.listbox.insert(tk.END, str(kontakt))

    def spremi_kontakte(self):
        with open("kontakti.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for k in self.kontakti:
                writer.writerow([k.ime, k.email, k.telefon])
        messagebox.showinfo("Spremanje", "Kontakti su uspješno spremljeni.")

    def ucitaj_kontakte(self):
        self.kontakti = []
        try:
            with open("kontakti.csv", "r", newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        kontakt = Kontakt(row[0], row[1], row[2])
                        self.kontakti.append(kontakt)
        except FileNotFoundError:
            pass
        self.osvjezi_listbox()

    def obrisi_kontakt(self):
        selekcija = self.listbox.curselection()
        if selekcija:
            index = selekcija[0]
            potvrda = messagebox.askyesno("Brisanje", "Jeste li sigurni da želite obrisati ovaj kontakt?")
            if potvrda:
                self.kontakti.pop(index)
                self.osvjezi_listbox()
        else:
            messagebox.showwarning("Upozorenje", "Niste odabrali kontakt za brisanje!")

# Pokretanje aplikacije
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")  # Početna veličina
    app = ImenikApp(root)
    root.mainloop()
