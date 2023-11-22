class Direccion:
    def __init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia

    def get_calle(self):
        return self.calle

    def get_ciudad(self):
        return self.ciudad

    def get_codigo_postal(self):
        return self.codigo_postal

    def get_numero_exterior(self):
        return self.numero_exterior

    def get_numero_interior(self):
        return self.numero_interior

    def get_colonia(self):
        return self.colonia

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def get_nombre(self):
        return self.nombre

    def get_edad(self):
        return self.edad

class Telefono:
    def __init__(self, numero):
        self.numero = numero

    def get_numero(self):
        return self.numero

class CorreoElectronico:
    def __init__(self, email, pagina_web):
        self.email = email
        self.pagina_web = pagina_web

    def get_email(self):
        return self.email

    def get_pagina_web(self):
        return self.pagina_web

class Contacto(Persona, Direccion, Telefono, CorreoElectronico):
    def __init__(self, nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web):
        Persona.__init__(self, nombre, edad)
        Direccion.__init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia)
        Telefono.__init__(self, numero)
        CorreoElectronico.__init__(self, email, pagina_web)

class Agenda:
    def __init__(self):
        self.lista_de_contactos = []

    def agregar_contacto(self, contacto):
        self.lista_de_contactos.append(contacto)

    def obtener_contactos(self):
        return self.lista_de_contactos
