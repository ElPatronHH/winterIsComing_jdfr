#firestore_db.py
import firebase_admin
from firebase_admin import credentials, firestore
import warnings


# Inicializa Firebase Admin
cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)

# Referencia al cliente de Firestore
db = firestore.client()

class Usuario:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.agendas_compartidas = []  # IDs de agendas a las que tienen acceso

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'agendas_compartidas': self.agendas_compartidas,
        }

class Direccion:
    def __init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia

    def to_dict(self):
        return vars(self)

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def to_dict(self):
        return vars(self)

class Telefono:
    def __init__(self, numero):
        self.numero = numero

    def to_dict(self):
        return vars(self)

class CorreoElectronico:
    def __init__(self, email, pagina_web):
        self.email = email
        self.pagina_web = pagina_web

    def to_dict(self):
        return vars(self)

class Contacto(Persona, Direccion, Telefono, CorreoElectronico):
    def __init__(self, nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web, doc_id=None):
        Persona.__init__(self, nombre, edad)
        Direccion.__init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia)
        Telefono.__init__(self, numero)
        CorreoElectronico.__init__(self, email, pagina_web)
        self.doc_id = doc_id  # Agregar un atributo para almacenar el ID del documento

    def to_dict(self):
        # Aquí combinamos todos los atributos de las clases heredadas en un solo diccionario
        data = {}
        for base_class in self.__class__.__bases__:
            data.update(base_class.to_dict(self))
        return data

    def merge(self, otro_contacto):
        # Suponiendo que 'timestamp' es un atributo de instancia de Contacto
        if otro_contacto.timestamp > self.timestamp:
            # Fusiona cada atributo, eligiendo el más reciente
            for attr, value in vars(otro_contacto).items():
                setattr(self, attr, value)

    @staticmethod
    def from_dict(source):
        # Aquí creamos una instancia de Contacto a partir de un diccionario
        contacto = Contacto(
            nombre=source['nombre'],
            edad=source['edad'],
            calle=source['calle'],
            ciudad=source['ciudad'],
            codigo_postal=source['codigo_postal'],
            numero_exterior=source['numero_exterior'],
            numero_interior=source['numero_interior'],
            colonia=source['colonia'],
            numero=source['numero'],
            email=source['email'],
            pagina_web=source['pagina_web']
        )
        return contacto

class Agenda:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.lista_de_contactos = []
        self.usuarios_con_acceso = {}  
        self.lista_de_contactos = []

    def agregar_contacto(self, contacto):
        # Agrega el contacto a la lista local y a Firestore
        self.lista_de_contactos.append(contacto)
        if contacto.doc_id is None:
            # Si es un nuevo contacto, crea un nuevo documento
            new_doc_ref = db.collection('contactos').document()
            new_doc_ref.set(contacto.to_dict())
            contacto.doc_id = new_doc_ref.id  # Almacena el ID del documento creado
        else:
            # Si el contacto ya tiene un ID, actualiza el documento existente
            db.collection('contactos').document(contacto.doc_id).set(contacto.to_dict())

    def cargar_contactos(self):
        # Carga los contactos de Firestore
        self.lista_de_contactos = []
        contactos_ref = db.collection('contactos')
        docs = contactos_ref.stream()
        for doc in docs:
            contacto = Contacto.from_dict(doc.to_dict())
            self.lista_de_contactos.append(contacto)

    def obtener_contactos(self):
        # Retorna la lista local de contactos
        return self.lista_de_contactos

    def eliminar_contacto(self, contacto):
        if contacto.doc_id:
            db.collection('contactos').document(contacto.doc_id).delete()
            self.lista_de_contactos.remove(contacto)

    def buscar_contacto_por_telefono(self, numero):
        for contacto in self.lista_de_contactos:
            if contacto.numero == numero:
                return contacto
        return None

    def buscar_contacto_por_nombre(self, nombre):
        warnings.filterwarnings("ignore", category=UserWarning, module='google.cloud.firestore')
        try:
            contactos_ref = db.collection('contactos')
            # Actualización para usar argumentos con nombre
            query = contactos_ref.where('nombre', '==', nombre).limit(1)
            results = query.stream()
            for result in results:
                return Contacto.from_dict(result.to_dict())
            return None
        except Exception as e:
            print(f"Error al buscar contacto: {e}")
            return None
        
    def merge_contactos(self, otro_contacto):
        # Encuentra un contacto existente que coincida con otro_contacto
        for contacto in self.lista_de_contactos:
            if contacto.nombre == otro_contacto.nombre and contacto.numero == otro_contacto.numero:
                contacto.merge(otro_contacto)
                return contacto
        # Si no se encuentra un contacto coincidente, simplemente agrega otro_contacto
        self.agregar_contacto(otro_contacto)
        return otro_contacto
    
    def compartir_agenda(self, user_id, nivel_de_acceso):
        self.usuarios_con_acceso[user_id] = nivel_de_acceso