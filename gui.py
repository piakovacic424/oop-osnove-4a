import tkinter as tk
lista_imena=[]
def klik_na_gumb():
    ime=unos_imena.get()
    lista_imena.append(ime)
    pozdravna=f"Pozdrav, {ime}!"
    for i in lista_imena:
        pozdravna=pozdravna+f"\nPozdrav, {ime}! "
     pozdrav.config(text=pozdravna)
    
#kreiranje novog prozora
prozor = tk.Tk()

#atribut tittle - naslov prozora
prozor.title("Moj prvi GUI program")
prozor.geometry("400x300")

#statični widget
pozdravna_poruka=tk.Label(prozor,text="Pozdrav 4.a!")
pozdravna_poruka.pack()

uputa=tk.Label(prozor,text="Upiši svoje ime:")
uputa.pack()

unos_imena=tk.Entry(prozor)
unos_imena.pack()

pozdrav=tk.Label(prozor,text="")
pozdrav.pack()

#interaktivni widget
gumb=tk.Button(prozor,text="Pozdravi me!",command=klik_na_gumb)

gumb.pack()
prozor.mainloop()