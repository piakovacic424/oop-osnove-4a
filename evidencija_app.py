import tkinter as tk
from tkinter import messagebox
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
 
 
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
 
        self.gumbi_frame = tk.Frame(self.root, pady=10)
        self.gumbi_frame.grid(row=2, column=0)
 
        tk.Button(self.gumbi_frame, text="Spremi CSV", command=self.spremi_u_csv).grid(row=0, column=0, padx=5)
        tk.Button(self.gumbi_frame, text="Učitaj CSV", command=self.ucitaj_iz_csv).grid(row=0, column=1, padx=5)
        tk.Button(self.gumbi_frame, text="Spremi XML", command=self.spremi_u_xml).grid(row=0, column=2, padx=5)
        tk.Button(self.gumbi_frame, text="Učitaj XML", command=self.ucitaj_iz_xml).grid(row=0, column=3, padx=5)
 
  
    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
 
        if not (ime and prezime and razred):
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti ispunjena!")
            return
 
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
 
   
    def spremi_u_csv(self):
        try:
            with open("ucenici.csv", mode='w', newline='', encoding='utf-8') as datoteka:
                polja = ['ime', 'prezime', 'razred']
                writer = csv.DictWriter(datoteka, fieldnames=polja)
                writer.writeheader()
                for u in self.ucenici:
                    writer.writerow({'ime': u.ime, 'prezime': u.prezime, 'razred': u.razred})
            messagebox.showinfo("Uspjeh", "Podaci su spremljeni u 'ucenici.csv'")
        except Exception as e:
            messagebox.showerror("Greška", f"Dogodila se greška pri spremanju: {e}")
 
    def ucitaj_iz_csv(self):
        try:
            with open("ucenici.csv", mode='r', encoding='utf-8') as datoteka:
                reader = csv.DictReader(datoteka)
                self.ucenici = []
                for red in reader:
                    self.ucenici.append(Ucenik(red['ime'], red['prezime'], red['razred']))
            self.osvjezi_prikaz()
            messagebox.showinfo("Uspjeh", "Podaci su učitani iz 'ucenici.csv'")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka 'ucenici.csv' ne postoji.")
        except Exception as e:
            messagebox.showerror("Greška", f"Dogodila se greška pri učitavanju: {e}")
 
   
    def spremi_u_xml(self):
        try:
            root = ET.Element("evidencija")
            for u in self.ucenici:
                ucenik_el = ET.SubElement(root, "ucenik")
                ET.SubElement(ucenik_el, "ime").text = u.ime
                ET.SubElement(ucenik_el, "prezime").text = u.prezime
                ET.SubElement(ucenik_el, "razred").text = u.razred
 
            xml_string = ET.tostring(root, 'utf-8')
            dom = minidom.parseString(xml_string)
            lijepi_xml = dom.toprettyxml(indent="  ")
 
            with open("ucenici.xml", "w", encoding="utf-8") as f:
                f.write(lijepi_xml)
 
            messagebox.showinfo("Uspjeh", "Podaci su spremljeni u 'ucenici.xml'")
        except Exception as e:
            messagebox.showerror("Greška", f"Dogodila se greška pri spremanju XML-a: {e}")
 
    def ucitaj_iz_xml(self):
        try:
            tree = ET.parse("ucenici.xml")
            root = tree.getroot()
            self.ucenici = []
 
            for ucenik_el in root.findall("ucenik"):
                ime = ucenik_el.find("ime").text
                prezime = ucenik_el.find("prezime").text
                razred = ucenik_el.find("razred").text
                self.ucenici.append(Ucenik(ime, prezime, razred))
 
            self.osvjezi_prikaz()
            messagebox.showinfo("Uspjeh", "Podaci su učitani iz 'ucenici.xml'")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka 'ucenici.xml' ne postoji.")
        except Exception as e:
            messagebox.showerror("Greška", f"Dogodila se greška pri učitavanju XML-a: {e}")
 
 
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = EvidencijaApp(root)
    root.mainloop()
 

