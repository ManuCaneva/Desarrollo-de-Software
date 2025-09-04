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
      return any(p.lower() in e.textoExtraible().lower() for e in self.elementos) 

    def contieneTodas(self, ps: list[str]) -> bool:
        """for e in self.elementos:
            texto = e.textoExtraible()
            for p in ps:
                if p in texto:
                    ps.remove(p)
        return not ps"""""
        return all(self.contienePalabra(p) for p in ps) 
    
    def conteoPalabras(self) -> int:
        """palabras = 0
        for e in self.elementos:
            palabras = len(e.textoExtraible().split())
        return palabras"""
        return sum(len(e.textoExtraible().split()) for e in self.elementos) 

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
    contador_id = 0 

    def __init__(self, nombre):
        Usuario.contador_id += 1    
        self.id = Usuario.contador_id
        self.nombre = nombre
        self.suscripciones = []
        
    def agregarSuscripcion(self, suscripcion):
        self.suscripciones.append(suscripcion)
        if self not in suscripcion.usuarios:  
            suscripcion.usuarios.append(self)


class Suscripcion:
    def __init__(self, filtros):
        """self.usuarios = usuarios""" 
        self.usuarios = []
        self.filtros = filtros

    def aplicaANoticia(self, noticia: Noticia):
       """ for filtro in self.filtros:
            if filtro.satisfechoPor(noticia):
                return True
        return False"""
       return all(f.satisfechoPor(noticia) for f in self.filtros)


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
    def __init__(self):
        self.usuarios = []
        self.noticias = []
        self.suscripciones = []


    def nuevoUsuario(self, nombre):
        """self.usuarios.append(Usuario(nombre))"""
        u = Usuario(nombre)  
        self.usuarios.append(u)
        return u
#agregado por chat creo:
    def agregarSuscripcion(self, suscripcion):
        self.suscripciones.append(suscripcion)

    def publicarNoticia(self, noticia: Noticia):
        self.noticias.append(noticia)
        print(f"\nNueva noticia publicada: {noticia.titulo}")
        for s in self.suscripciones:
            if s.aplicaANoticia(noticia):
                for u in s.usuarios:
                    print(f"[{u.nombre}] recibió la noticia: {noticia.titulo}")


if __name__ == "__main__":
    # 1. Crear el servidor de noticias
    servidor = ServidorNoticias()

    # 2. Crear usuarios
    user_juan = servidor.nuevoUsuario("Juan")
    user_maria = servidor.nuevoUsuario("Maria")
    user_pedro = servidor.nuevoUsuario("Pedro")

    print("\n--- Usuarios Creados ---")
    for u in servidor.usuarios:
        print(f"ID: {u.id}, Nombre: {u.nombre}")

    # 3. Definir filtros
    filtro_deportes = FiltroCategoria(Categoria.DEPORTES)
    filtro_chimentos = FiltroCategoria(Categoria.CHIMENTERO)
    filtro_de_paul = FiltroPalabraClave("De Paul")
    filtro_river_boca = FiltroContieneTodas(["River", "Boca"])
    filtro_max_50_palabras = FiltroMaxPalabras(50)
    filtro_no_economia = NoFiltro(FiltroCategoria(Categoria.ECONOMIA))
    filtro_titulo_clima = FiltroTitulo("El Clima")


    # 4. Crear suscripciones
    # Suscripción de Juan: Noticias de Deportes Y que hablen de "De Paul"
    suscripcion_juan_depaul = Suscripcion(filtros=[YFiltro([filtro_deportes, filtro_de_paul])])
    user_juan.agregarSuscripcion(suscripcion_juan_depaul)
    servidor.agregarSuscripcion(suscripcion_juan_depaul)

    # Suscripción de Maria: Noticias de "River" O "Boca" Y que no sean de Economía
    suscripcion_maria_futbol = Suscripcion(filtros=[YFiltro([OFiltro([filtro_river_boca, FiltroPalabraClave("fútbol")]), filtro_no_economia])])
    user_maria.agregarSuscripcion(suscripcion_maria_futbol)
    servidor.agregarSuscripcion(suscripcion_maria_futbol)

    # Suscripción de Pedro: Noticias de cualquier categoría pero con menos de 50 palabras
    suscripcion_pedro_cortas = Suscripcion(filtros=[filtro_max_50_palabras])
    user_pedro.agregarSuscripcion(suscripcion_pedro_cortas)
    servidor.agregarSuscripcion(suscripcion_pedro_cortas)
    
    # Suscripción de Juan (otra): Noticias de espectáculos O chimentero
    suscripcion_juan_farandula = Suscripcion(filtros=[OFiltro([FiltroCategoria(Categoria.ESPECTACULOS), FiltroCategoria(Categoria.CHIMENTERO)])])
    user_juan.agregarSuscripcion(suscripcion_juan_farandula)
    servidor.agregarSuscripcion(suscripcion_juan_farandula)

    print("\n--- Suscripciones Creadas y Asociadas ---")
    print(f"Juan tiene {len(user_juan.suscripciones)} suscripciones.")
    print(f"Maria tiene {len(user_maria.suscripciones)} suscripciones.")
    print(f"Pedro tiene {len(user_pedro.suscripciones)} suscripciones.")


    # 5. Publicar noticias y observar las notificaciones
    # Noticia 1: Deporte con De Paul (Debería notificar a Juan)
    cuerpo1 = Cuerpo([Texto("El jugador De Paul tuvo una destacada actuación en el partido de la selección de fútbol.")])
    noticia1 = Noticia(1, "Gran partido de la Selección", Categoria.DEPORTES, cuerpo1, "2025-09-01")
    servidor.publicarNoticia(noticia1)

    # Noticia 2: Chimentos con De Paul (No debería notificar a Juan por la primera suscripción, pero sí por la segunda)
    cuerpo2 = Cuerpo([Texto("De Paul y su nueva pareja fueron vistos en un evento social, generando rumores.")])
    noticia2 = Noticia(2, "De Paul en el ojo de la tormenta", Categoria.CHIMENTERO, cuerpo2, "2025-09-02")
    servidor.publicarNoticia(noticia2)

    # Noticia 3: Deporte sin De Paul (No debería notificar a Juan)
    cuerpo3 = Cuerpo([Texto("River y Boca empataron en un emocionante superclásico. El partido estuvo lleno de goles y polémica.")])
    noticia3 = Noticia(3, "Superclásico vibrante: River y Boca no se sacaron ventajas", Categoria.DEPORTES, cuerpo3, "2025-09-03")
    servidor.publicarNoticia(noticia3) # Debería notificar a Maria

    # Noticia 4: Economía (No debería notificar a Maria)
    cuerpo4 = Cuerpo([Texto("La bolsa de valores tuvo una jornada agitada, con subas y bajas inesperadas.")])
    noticia4 = Noticia(4, "Mercados en vilo por nueva política económica", Categoria.ECONOMIA, cuerpo4, "2025-09-04")
    servidor.publicarNoticia(noticia4)

    # Noticia 5: Noticia corta (Debería notificar a Pedro)
    cuerpo5 = Cuerpo([Texto("Breve informe meteorológico. Se esperan lluvias fuertes para el fin de semana en la capital.")])
    noticia5 = Noticia(5, "Pronóstico del tiempo", Categoria.SOCIALES, cuerpo5, "2025-09-05")
    servidor.publicarNoticia(noticia5)

    # Noticia 6: Espectáculos (Debería notificar a Juan por la segunda suscripción)
    cuerpo6 = Cuerpo([Texto("La nueva película de ciencia ficción rompe récords de taquilla en su primer fin de semana de estreno.")])
    noticia6 = Noticia(6, "Éxito rotundo en la taquilla", Categoria.ESPECTACULOS, cuerpo6, "2025-09-06")
    servidor.publicarNoticia(noticia6)

    # Noticia 7: Noticia larga que nadie suscribe
    cuerpo7 = Cuerpo([Texto("Este es un artículo muy largo sobre la historia de la programación orientada a objetos, abarcando muchísimos detalles, ejemplos y conceptos avanzados. La extensión de este texto supera ampliamente las cincuenta palabras, haciendo que no sea apto para suscripciones que busquen contenido conciso. Exploramos la evolución desde Smalltalk hasta los paradigmas modernos de Python y Java, sus ventajas y desventajas en el desarrollo de software. Analizamos patrones de diseño comunes, principios SOLID y la importancia de la abstracción y el encapsulamiento para construir sistemas robustos y mantenibles.")])
    noticia7 = Noticia(7, "Un largo tratado de POO", Categoria.ECONOMIA, cuerpo7, "2025-09-07")
    servidor.publicarNoticia(noticia7)