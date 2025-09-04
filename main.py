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
        self.fechaPublicacion = fechaPublicacion

    def conteoPalabras(self):
        #devuelve la cantidad de palabras en el cuerpo de la noticia
        return self.cuerpo.conteoPalabras()

class Cuerpo:
    def __init__(self, elementos):
        self.elementos = elementos
    
    def contienePalabra(self, p: str) -> bool:
      """  for e in self.elementos:
            if p in e.textoExtraible():
                return True
        return False"""
      return any(p.lower() in e.textoExtraible().lower() for e in self.elementos)  # ✅ CAMBIO: más compacto y seguro

    def contieneTodas(self, ps: list[str]) -> bool:
        """for e in self.elementos:
            texto = e.textoExtraible()
            for p in ps:
                if p in texto:
                    ps.remove(p)
        return not ps"""""
        return all(self.contienePalabra(p) for p in ps)  # ✅ CAMBIO: evitamos modificar la lista original
    
    def conteoPalabras(self) -> int:
        """palabras = 0
        for e in self.elementos:
            palabras = len(e.textoExtraible().split())
        return palabras"""
        return sum(len(e.textoExtraible().split()) for e in self.elementos)  # ✅ CAMBIO: ahora acumula correctamente

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
    """contador_id = 0

    def __init__(self, nombre):
        self.id = self.__class__.id
        self.nombre = nombre
        self.suscripciones = []

        self.__class__.incrementarId()
        
    def agregarSuscripcion(self, Suscripcion):
        self.suscripciones.append(Suscripcion)

    @classmethod
    def incrementarId(cls):
        cls.id += 1"""
    contador_id = 0  # ✅ CAMBIO: renombrado, antes usabas "id" como variable de clase

    def __init__(self, nombre):
        Usuario.contador_id += 1          # ✅ CAMBIO: incrementamos primero
        self.id = Usuario.contador_id     # ✅ CAMBIO: asignamos después
        self.nombre = nombre
        self.suscripciones = []
        
    def agregarSuscripcion(self, suscripcion):
        self.suscripciones.append(suscripcion)
        if self not in suscripcion.usuarios:      # ✅ CAMBIO: mantenemos bidireccionalidad
            suscripcion.usuarios.append(self)


class Suscripcion:
    def __init__(self, usuarios, filtros):
        """self.usuarios = usuarios""" 
        self.usuarios = []   # ✅ CAMBIO: siempre empieza vacío 
        self.filtros = filtros

    def aplicaANoticia(self, noticia: Noticia):
       """ for filtro in self.filtros:
            if filtro.satisfechoPor(noticia):
                return True
        return False"""
       return all(f.satisfechoPor(noticia) for f in self.filtros)  # ✅ CAMBIO: antes era OR, ahora es AND


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

class OFiltro(Filtro):
    def __init__(self, filtros: list[Filtro]):
        self.filtros = filtros

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return any(p.satisfechoPor(noticia) for p in self.filtros)

class NoFiltro(Filtro):
    def __init__(self, filtro: Filtro):
        self.filtro = filtro

    def satisfechoPor(self, noticia: Noticia) -> bool:
        return not self.filtro.satisfechoPor(noticia)

class ServidorNoticias:
    """ def __init__(self, usuarios=[], noticias=[], suscripciones=[]):
        self.usuarios = usuarios
        self.noticias = noticias
        self.suscripciones = suscripciones"""
    def __init__(self):  # ✅ CAMBIO: evitamos listas mutables en parámetros
        self.usuarios = []
        self.noticias = []
        self.suscripciones = []


    def nuevoUsuario(self, nombre):
        """self.usuarios.append(Usuario(nombre))"""
        u = Usuario(nombre)  # ✅ CAMBIO: ahora devuelve el usuario creado
        self.usuarios.append(u)
        return u
#agregado por chat creo:
    def agregarSuscripcion(self, suscripcion):
        self.suscripciones.append(suscripcion)

    def publicarNoticia(self, noticia: Noticia):  # ✅ CAMBIO: nuevo método
        self.noticias.append(noticia)
        print(f"\nNueva noticia publicada: {noticia.titulo}")
        for s in self.suscripciones:
            if s.aplicaANoticia(noticia):
                for u in s.usuarios:
                    print(f"[{u.nombre}] recibió la noticia: {noticia.titulo}")
