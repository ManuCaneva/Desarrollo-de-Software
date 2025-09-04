from enum import Enum
from abc import ABC, abstractmethod

class Categoria(Enum):
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

class Cuerpo:
    def __init__(self, elementos):
        self.elementos = elementos
    
    def contienePalabra(self, p: str) -> bool:
        for e in self.elementos:
            if p in e.textoExtraible():
                return True
        return False

    def contieneTodas(self, ps: list[str]) -> bool:
        for e in self.elementos:
            texto = e.textoExtraible()
            for p in ps:
                if p in texto:
                    ps.remove(p)
        return not ps
    
    def conteoPalabras(self) -> int:
        palabras = 0
        for e in self.elementos:
            palabras = len(e.textoExtraible().split())
        return palabras

class Contenido(ABC):
    @abstractmethod
    def textoExtraible(self) -> str:
        """
        Método abstracto que obliga a las subclases a definir
        cómo extraen el texto de sí mismas.
        """
        pass

class Texto(Contenido):
    def __init__(self, contenido: str):
        self.contenido = contenido

    def textoExtraible(self) -> str:
        return self.contenido

class Imagen(Contenido):
    def __init__(self, descripcion: str):
        self.descripcion = descripcion

    def textoExtraible(self) -> str:
        # simplificamos: devolvemos descripción como "texto extraíble"
        return self.descripcion

class Video(Contenido):
    def __init__(self, url: str, descripcion: str = ""):
        self.url = url
        self.descripcion = descripcion

    def textoExtraible(self) -> str:
        return self.descripcion

class Usuario:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.suscripciones = []
        
    def agregarSuscripcion(self, Suscripcion):
        self.suscripciones.append(Suscripcion)

class Suscripcion:
    total_subs = 0

    def __init__(self, usuarios, filtros, total_subs):
        self.id = total_subs
        self.usuarios = usuarios
        self.filtros = filtros

        self.__class__.incremental_id()

    def aplicaANoticia(self, noticia: Noticia):
        for filtro in self.filtros:
            if filtro.satisfechoPor(noticia):
                return True
        return False

    @classmethod
    def incrementarId(cls):
        cls.total_subs += 1

class Filtro(ABC):
    @abstractmethod
    def satisfechoPor(self, noticia: Noticia) -> bool:
        pass

class FiltroCategoria(Filtro):
    def __init__(self, categoria):
        self.categoria = categoria

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return noticia.categoria == self.categoria

class FiltroTitulo(Filtro):
    def __init__(self, frase: str):
        self.frase = frase

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return self.frase == noticia.titulo

class FiltroPalabraClave(Filtro):
    def __init__(self, palabra: str):
        self.palabra = palabra

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return noticia.cuerpo.contienePalabra(self.palabra)
    
class FiltroContieneTodas(Filtro):
    def __init__(self, palabras: list[str]):
        self.palabras = palabras

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return noticia.cuerpo.contieneTodas(self.palabras)
    
class FiltroMaxPalabras(Filtro):
    def __init__(self, max_palabras: int):
        self.max_palabras = max_palabras

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return noticia.conteoPalabras() <= self.max_palabras
    
class YFiltro(Filtro):
    #se le pasa una lista de Filtros
    def __init__(self, filtros: list[Filtro]):
        self.filtros = filtros

    #el all() devuelve true si todos los valores son true
    def satisfechoPor(self, noticia: Noticia) -> bool:
        return all(p.satisfechoPor(noticia) for p in self.filtros)

class ServidorNoticias:
    def __init__(self, noticias, suscripciones):
        self.noticias = []
        self.suscripciones = []
