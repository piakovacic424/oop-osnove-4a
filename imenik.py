import tkinter as tk

class Kontakt:
    def __init__(self,ime,email,telefon):
        self.ime=ime
        self.email=email
        self.telefon=telefon
    
    def __str__(self):
        return f"{self.ime}--{self.email}--{self.telefon}"
    
class Imenikapp:
    def __init__(self, root):
        self.root = root
        self.root.title("Imenik")

        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="NSEW")

        tk.Label(self.frame, text="Ime:").grid(row=0, column=0, sticky="W", pady=5)
        self.ime_entry = tk.Entry(self.frame)
        self.ime_entry.grid(row=0, column=1, sticky="EW", pady=5)

        tk.Label(self.frame, text="Email:").grid(row=1, column=0, sticky="W", pady=5)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=1, column=1, sticky="EW", pady=5)

        tk.Label(self.frame, text="Telefon:").grid(row=2, column=0, sticky="W", pady=5)
        self.telefon_entry = tk.Entry(self.frame)
        self.telefon_entry.grid(row=2, column=1, sticky="EW", pady=5)


        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  
    app = Imenikapp(root)
    root.mainloop()