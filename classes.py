from firebase_admin import firestore

db = firestore.client()

class Contacto:
    # ... tus métodos y propiedades existentes ...

    def to_dict(self):
        # Convierte el objeto Contacto en un diccionario para Firestore
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            # ... otros campos ...
        }

    @staticmethod
    def from_dict(source):
        # Crea un objeto Contacto a partir de un diccionario (por ejemplo, de Firestore)
        contacto = Contacto(
            nombre=source['nombre'],
            edad=source['edad'],
            # ... otros campos ...
        )
        return contacto

class Agenda:
    # ... tus métodos y propiedades existentes ...

    def cargar_contactos(self):
        # Carga contactos de Firestore
        contactos_ref = db.collection('contactos')
        docs = contactos_ref.stream()
        for doc in docs:
            contacto = Contacto.from_dict(doc.to_dict())
            self.agregar_contacto(contacto)

    def guardar_contacto(self, contacto):
        # Guarda un contacto en Firestore
        contactos_ref = db.collection('contactos').document()
        contactos_ref.set(contacto.to_dict())

