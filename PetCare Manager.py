

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import xml.etree.ElementTree as ET
import os
from datetime import datetime

# ======== MODEL ========

class Dogadjaj:
    def __init__(self, datum, opis):
        self.datum = datum
        self.opis = opis

    def __str__(self):
        return f"{self.datum} - {self.opis}"


class Ljubimac:
    def __init__(self, ime, vrsta, dob, putanja_slike=""):
        self.ime = ime
        self.vrsta = vrsta
        self.dob = dob
        self.putanja_slike = putanja_slike
        self.dogadjaji = []

    def dodaj_dogadjaj(self, dogadjaj):
        self.dogadjaji.append(dogadjaj)

    def ukloni_dogadjaj(self, indeks):
        if 0 <= indeks < len(self.dogadjaji):
            del self.dogadjaji[indeks]

    def __str__(self):
        return f"{self.vrsta}: {self.ime}"


# ======== APLIKACIJA ========

class PetCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 PetCare Manager v1.3")
        self.root.geometry("1000x700")
        self.root.configure(bg="#e6f0ff")  # svjetloplava pozadina

        self.ljubimci = []
        self.selektiran = None
        self.xml_datoteka = "ljubimci.xml"

        self.kreiraj_stil()
        self.kreiraj_menu()
        self.kreiraj_status()
        self.kreiraj_sucelje()

        self.ucitaj_podatke()
        self.provjeri_podsjetnike()

    # ====== ESTETIKA ======
    def kreiraj_stil(self):
        stil = ttk.Style()
        stil.theme_use("clam")

        # Blage pastelne boje i moderni font
        stil.configure("TButton", background="#b3d9ff", foreground="black", font=("Segoe UI", 10, "bold"), padding=5)
        stil.map("TButton",
                 background=[("active", "#99ccff")],
                 relief=[("pressed", "sunken")])
        stil.configure("TLabel", background="#e6f0ff", font=("Segoe UI", 10))
        stil.configure("TCombobox", padding=5)

    # ====== GUI ELEMENTI ======

    def kreiraj_menu(self):
        menu_bar = tk.Menu(self.root, bg="#b3d9ff", fg="black", tearoff=0)
        datoteka_menu = tk.Menu(menu_bar, tearoff=0, bg="#e6f2ff")
        datoteka_menu.add_command(label="Spremi", command=self.spremi_podatke)
        datoteka_menu.add_command(label="Učitaj", command=self.ucitaj_podatke)
        datoteka_menu.add_separator()
        datoteka_menu.add_command(label="Izlaz", command=self.root.quit)
        menu_bar.add_cascade(label="Datoteka", menu=datoteka_menu)

        pomoc_menu = tk.Menu(menu_bar, tearoff=0, bg="#e6f2ff")
        pomoc_menu.add_command(label="O aplikaciji", command=self.o_aplikaciji)
        menu_bar.add_cascade(label="Pomoć", menu=pomoc_menu)

        self.root.config(menu=menu_bar)

    def kreiraj_status(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Dobrodošli u PetCare Manager 🐾")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              bg="#b3d9ff", font=("Segoe UI", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def kreiraj_sucelje(self):
        frame = tk.Frame(self.root, bg="#e6f0ff")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.rowconfigure(0, weight=1)

        # Lijevi okvir - lista ljubimaca
        lijevi_okvir = tk.Frame(frame, bg="#cce0ff", relief=tk.RIDGE, bd=2)
        lijevi_okvir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        lijevi_okvir.rowconfigure(1, weight=1)

        tk.Label(lijevi_okvir, text="Ljubimci", font=("Segoe UI", 12, "bold"), bg="#cce0ff").pack(pady=5)
        self.lista = tk.Listbox(lijevi_okvir, font=("Segoe UI", 10), bg="white", bd=1, relief=tk.GROOVE)
        self.lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.lista.bind("<<ListboxSelect>>", self.prikazi_detalje)

        gumbi_okvir = tk.Frame(lijevi_okvir, bg="#cce0ff")
        gumbi_okvir.pack(fill=tk.X, pady=5)
        ttk.Button(gumbi_okvir, text="➕ Dodaj", command=self.dodaj_ljubimca).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(gumbi_okvir, text="✏️ Uredi", command=self.uredi_ljubimca).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(gumbi_okvir, text="❌ Obriši", command=self.ukloni_ljubimca).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # Desni okvir - detalji ljubimca
        desni_okvir = tk.Frame(frame, bg="#f2f7ff", relief=tk.RIDGE, bd=2)
        desni_okvir.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        desni_okvir.rowconfigure(3, weight=1)
        desni_okvir.columnconfigure(0, weight=1)
        tk.Label(desni_okvir, text="Događaji", font=("Segoe UI", 12, "bold")).pack(pady=5)

        self.lbl_slike = tk.Label(desni_okvir, bg="#f2f7ff")
        self.lbl_slike.pack(pady=10)

        self.lbl_info = tk.Label(desni_okvir, text="", font=("Segoe UI", 11, "bold"), bg="#f2f7ff", justify="center")
        self.lbl_info.pack(pady=10)

        self.dogadjaj_lista = tk.Listbox(desni_okvir, height=10, bg="white", font=("Segoe UI", 10))
        self.dogadjaj_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        dog_gumbi = tk.Frame(desni_okvir, bg="#f2f7ff")
        dog_gumbi.pack(fill=tk.X, pady=5)
        ttk.Button(dog_gumbi, text="📅 Dodaj", command=self.dodaj_dogadjaj).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        ttk.Button(dog_gumbi, text="✏️ Uredi", command=self.uredi_dogadjaj).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
        ttk.Button(dog_gumbi, text="🗑️ Obriši", command=self.ukloni_dogadjaj).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

    # ====== LOGIKA ======

    def dodaj_ljubimca(self):
        self._prozor_ljubimac("Dodaj ljubimca")

    def uredi_ljubimca(self):
        idx = self.lista.curselection()
        if not idx:
            return messagebox.showwarning("Upozorenje", "Odaberi ljubimca!")
        self._prozor_ljubimac("Uredi ljubimca", self.ljubimci[idx[0]])

    def _prozor_ljubimac(self, naslov, ljubimac=None):
        prozor = tk.Toplevel(self.root)
        prozor.title(naslov)
        prozor.geometry("400x250")

        prozor.columnconfigure(1, weight=1)

        tk.Label(prozor, text="Ime:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ime = tk.Entry(prozor)
        ime.grid(row=0, column=1, sticky="ew")

        tk.Label(prozor, text="Vrsta:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        vrsta = ttk.Combobox(prozor, values=["Pas", "Mačka", "Ptica"])
        vrsta.grid(row=1, column=1, sticky="ew")

        tk.Label(prozor, text="Dob:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        dob = tk.Entry(prozor)
        dob.grid(row=2, column=1, sticky="ew")

        putanja_slike = tk.StringVar()

        def odaberi_sliku():
            dat = filedialog.askopenfilename(filetypes=[("Slike", "*.jpg *.png *.jpeg")])
            if dat:
                putanja_slike.set(dat)

        tk.Button(prozor, text="📷 Odaberi sliku", command=odaberi_sliku).grid(row=3, column=0, columnspan=2, pady=5)

        if ljubimac:
            ime.insert(0, ljubimac.ime)
            vrsta.set(ljubimac.vrsta)
            dob.insert(0, ljubimac.dob)
            putanja_slike.set(ljubimac.putanja_slike)

        def spremi():
            try:
                if ljubimac:
                    ljubimac.ime = ime.get()
                    ljubimac.vrsta = vrsta.get()
                    ljubimac.dob = int(dob.get())
                    ljubimac.putanja_slike = putanja_slike.get()
                else:
                    novi = Ljubimac(ime.get(), vrsta.get(), int(dob.get()), putanja_slike.get())
                    self.ljubimci.append(novi)
                self.osvjezi_listu()
                prozor.destroy()
            except ValueError:
                messagebox.showerror("Greška", "Dob mora biti broj!")

        tk.Button(prozor, text="💾 Spremi", command=spremi).grid(row=4, column=0, columnspan=2, pady=10)

    def ukloni_ljubimca(self):
        idx = self.lista.curselection()
        if not idx:
            return
        ljubimac = self.ljubimci[idx[0]]
        if messagebox.askyesno("Brisanje", f"Želiš li izbrisati {ljubimac.ime}?"):
            del self.ljubimci[idx[0]]
            self.osvjezi_listu()
            self.lbl_info.config(text="")
            self.lbl_slike.config(image="")
            self.dogadjaj_lista.delete(0, tk.END)

    def dodaj_dogadjaj(self):
        if self.selektiran is None:
            return messagebox.showwarning("Upozorenje", "Odaberi ljubimca!")
        self._prozor_dogadjaj("Dodaj događaj")

    def uredi_dogadjaj(self):
        if self.selektiran is None:
            return messagebox.showwarning("Upozorenje", "Odaberi ljubimca!")
        idx = self.dogadjaj_lista.curselection()
        if not idx:
            return messagebox.showwarning("Upozorenje", "Odaberi događaj!")
        self._prozor_dogadjaj("Uredi događaj", self.selektiran.dogadjaji[idx[0]])

    def _prozor_dogadjaj(self, naslov, dogadjaj=None):
        prozor = tk.Toplevel(self.root)
        prozor.title(naslov)
        prozor.geometry("350x150")

        tk.Label(prozor, text="Datum (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        datum = tk.Entry(prozor)
        datum.grid(row=0, column=1)

        tk.Label(prozor, text="Opis:").grid(row=1, column=0, padx=5, pady=5)
        opis = tk.Entry(prozor)
        opis.grid(row=1, column=1)

        if dogadjaj:
            datum.insert(0, dogadjaj.datum)
            opis.insert(0, dogadjaj.opis)

        def spremi():
            if dogadjaj:
                dogadjaj.datum = datum.get()
                dogadjaj.opis = opis.get()
            else:
                d = Dogadjaj(datum.get(), opis.get())
                self.selektiran.dodaj_dogadjaj(d)
            self.prikazi_detalje()
            prozor.destroy()

        tk.Button(prozor, text="💾 Spremi", command=spremi).grid(row=2, column=0, columnspan=2, pady=10)

    def ukloni_dogadjaj(self):
        if self.selektiran is None:
            return messagebox.showwarning("Upozorenje", "Odaberi ljubimca!")
        idx = self.dogadjaj_lista.curselection()
        if not idx:
            return messagebox.showwarning("Upozorenje", "Odaberi događaj za brisanje!")
        d = self.selektiran.dogadjaji[idx[0]]
        if messagebox.askyesno("Brisanje događaja", f"Želiš li izbrisati događaj:\n{d}?"):
            self.selektiran.ukloni_dogadjaj(idx[0])
            self.prikazi_detalje()

    def prikazi_detalje(self, event=None):
        idx = self.lista.curselection()
        if not idx:
            return
        self.selektiran = self.ljubimci[idx[0]]
        ljub = self.selektiran
        self.lbl_info.config(text=f"Ime: {ljub.ime}\nVrsta: {ljub.vrsta}\nDob: {ljub.dob} god.")

        if ljub.putanja_slike and os.path.exists(ljub.putanja_slike):
            img = Image.open(ljub.putanja_slike)
            img = img.resize((200, 200))
            self.tk_img = ImageTk.PhotoImage(img)
            self.lbl_slike.config(image=self.tk_img)
        else:
            self.lbl_slike.config(image="")

        self.dogadjaj_lista.delete(0, tk.END)
        for d in ljub.dogadjaji:
            self.dogadjaj_lista.insert(tk.END, str(d))

    def osvjezi_listu(self):
        self.lista.delete(0, tk.END)
        for l in self.ljubimci:
            self.lista.insert(tk.END, str(l))

    # ====== PODACI ======
    def spremi_podatke(self):
        root = ET.Element("Ljubimci")
        for l in self.ljubimci:
            ljub_el = ET.SubElement(root, "Ljubimac", attrib={"vrsta": l.vrsta})
            ET.SubElement(ljub_el, "Ime").text = l.ime
            ET.SubElement(ljub_el, "Dob").text = str(l.dob)
            ET.SubElement(ljub_el, "Slika").text = l.putanja_slike

            dog_el = ET.SubElement(ljub_el, "Dogadjaji")
            for d in l.dogadjaji:
                d_el = ET.SubElement(dog_el, "Dogadjaj")
                ET.SubElement(d_el, "Datum").text = d.datum
                ET.SubElement(d_el, "Opis").text = d.opis

        tree = ET.ElementTree(root)
        tree.write(self.xml_datoteka)
        self.status_var.set("Podaci su spremljeni.")

    def ucitaj_podatke(self):
        if not os.path.exists(self.xml_datoteka):
            return
        try:
            tree = ET.parse(self.xml_datoteka)
            root = tree.getroot()
            self.ljubimci.clear()
            for l_el in root.findall("Ljubimac"):
                l = Ljubimac(
                    l_el.find("Ime").text,
                    l_el.attrib.get("vrsta", ""),
                    int(l_el.find("Dob").text),
                    l_el.find("Slika").text
                )
                for d_el in l_el.find("Dogadjaji").findall("Dogadjaj"):
                    datum = d_el.find("Datum").text
                    opis = d_el.find("Opis").text
                    l.dodaj_dogadjaj(Dogadjaj(datum, opis))
                self.ljubimci.append(l)
            self.osvjezi_listu()
            self.status_var.set("Podaci učitani.")
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati podatke: {e}")

    def provjeri_podsjetnike(self):
        danas = datetime.today()
        blizu = []
        for l in self.ljubimci:
            for d in l.dogadjaji:
                try:
                    dat = datetime.strptime(d.datum, "%Y-%m-%d")
                    if 0 <= (dat - danas).days <= 7:
                        blizu.append(f"{l.ime}: {d.opis} ({d.datum})")
                except:
                    continue
        if blizu:
            messagebox.showinfo("Podsjetnik", "Uskoro događaji:\n" + "\n".join(blizu))

    def o_aplikaciji(self):
        messagebox.showinfo("O aplikaciji", 
                            "🐾 PetCare Manager v1.2\n"
                            "Autor: Tvoje Ime\n"
                            "Aplikacija za evidenciju kućnih ljubimaca\n"
                            "© 2025")


# ======== GLAVNI PROGRAM ========

if __name__ == "__main__":
    root = tk.Tk()
    app = PetCareApp(root)
    root.mainloop()
