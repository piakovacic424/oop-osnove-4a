from tkinter import*
import tkinter as tk

class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.ime} {self.prezime}, Razred: {self.razred}"
    
ucenik1=Ucenik("Ivan", "Ivić", 5)
print(ucenik1)

class EvidencijaApp:
    def __init__(self,root):
        self.root=root

        #naslov
        self.root.title("Evidencija učenika")
        self.root.geometry("600x400")

        root.columnconfigure(0,weight=1)
        root.rowconfigure(0,weight=1)

        #frame
        frame= tk.Frame=Frame(root,padx=10,pady=10)
        frame.grid(row=0,column=0,sticky="nsew")

        frame.columnconfigure(1,weight=1)

        tk.Label(frame,text="Ime:").grid(row=0,column=0,sticky="w")
        ime_entry=tk.Entry(frame)
        ime_entry.grid(row=0,column=1,sticky="ew",pady=2)
        Ucenik.ime=ime_entry.get()

        tk.Label(frame,text="Prezime:").grid(row=1,column=0,sticky="w")
        prezime_entry=tk.Entry(frame)
        prezime_entry.grid(row=1,column=1,sticky="ew",pady=2)
        Ucenik.prezime=prezime_entry.get()

        tk.Label(frame,text="Razred:").grid(row=2,column=0,sticky="w")
        razred_entry=tk.Entry(frame)
        razred_entry.grid(row=2,column=1,sticky="ew",pady=2)
        Ucenik.razred=razred_entry.get()
        
        tk.Label(frame,text="E-mail:").grid(row=3,column=0,sticky="w")  
        mail_entry=tk.Entry(frame)
        mail_entry.grid(row=3,column=1,sticky="ew",pady=2)

        spremi_gumb=tk.Button(frame,text="Spremi")
        spremi_gumb=spremi_gumb.grid(row=4,column=0,columnspan=2,sticky="ew",pady=5,command=dodaj_ucenika)

        self.ucenici=[]
        self.listbox=tk.Listbox(frame)
        self.listbox.grid(row=5,column=0,columnspan=2,sticky="nsew",pady=5)

def azuriraj_listbox(self):
    self.listbox.delete(0,tk.END)
    for ucenik in self.ucenici:
        self.listbox.insert(tk.END,str(ucenik))

def dodaj_ucenika():
    ime=ime_entry.get()
    prezime=prezime_entry.get()
    razred=razred_entry.get()
    novi_ucenik=Ucenik(ime,prezime,razred)
    self.ucenici.append(novi_ucenik)
    self.azuriraj_listbox()
    self.ucenici.append(novi_ucenik)
        
    

if __name__=="__main__":
    root=Tk()
    app=EvidencijaApp(root)
    root.mainloop()






