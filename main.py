from enum import Enum

Class Categoria(Enum):
    DEPORTES = 0
    SOCIALES = 1
    POLICIALES = 2
    ESPECTACULOS = 3
    ECONOMIA = 4
    INTERNACIONALES = 5
    CHIMENTERO = 6

class Noticia:
    def __init__(self, id, titulo, categoria, cuerpo, fechaPublicacion):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.cuerpo = cuerpo
        self.fechaPublicación = fechaPublicacion

    def conteoPalabras(self):
        #devuelve la cantidad de palabras en el cuerpo de la noticia
        return self.cuerpo.conteoPalabras()

Class Cuerpo:
    def __init__(self, elementos):
        self.elementos = elementos
    
    def contienePalabra(self, p: str) -> bool:
        for e in self.elementos:
            if isinstance(e, str) and p in e:
                return True
        
        return False

    def contieneTodas(self, ps: List[str]) -> bool:
        # hay que hacer j
        return False
    
    def conteoPalabras(self) -> int:
        palabras = 0

        for e in self.elementos:
            if isinstance(e, str):
                palabras = len(e.split())
        
        return palabras

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre