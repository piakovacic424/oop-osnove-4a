class Knjiga:
    def __init__(self, naslov, autor, godina_izdanja):
        self.naslov = naslov
        self.autor = autor
        self.godina_izdanja = godina_izdanja

knjiga1=Knjiga("Hamlet","William Shakespeare",1603)
knjiga2=Knjiga("Gospodar prstenova","J.R.R. Tolkien",1954)

print(f"Naslov:{knjiga1.naslov}, Autor:{knjiga1.autor}, Godina izdanja:{knjiga1.godina_izdanja}")