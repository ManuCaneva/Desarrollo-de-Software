categorias = tuple("DEPORTES", "SOCIALES", "POLICIALES", "ESPECTACULOS", "ECONOMÍA", "INTERNACIONALES", "CHIMENTERO")

class Noticia:
    def __init__(self, id, titulo, categoria, cuerpo, fechaPublicacion):
        self.id = id
        self.titulo = titulo
        self.categoria = categoria
        self.cuerpo = cuerpo
        self.fechaPublicación = fechaPublicacion

    def conteoPalabras(self):
        #devuelve la cantidad de palabras en el cuerpo de la noticia
        return len(self.cuerpo.split())

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre