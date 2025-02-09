
#users.py jdfr
from firebase_admin import auth, firestore, exceptions
from firestore_db import db 
import requests
import json

class Usuario:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.agendas_compartidas = []  

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'agendas_compartidas': self.agendas_compartidas,
        }
        
    def cargar_agenda(self, email):
        print("Esto entra y sirve.")
        coleccion = db.collection(email);
        documentos = coleccion.limit(1).get()
        if documentos:
            print(f'La agenda de "{email}" ya existe.')
        else:
            print(f'La agenda de "{email}" no existe, se creará.')
            campos_documento = {
            'nombre': '',
            'edad': '',
            'calle': '',
            'ciudad': '',
            'codigo_postal': '',
            'numero_exterior': '',
            'numero_interior': '',
            'colonia': '',
            'numero': '',
            'email': '',
            'pagina_web': ''
            }
            settings = {
                'escritura':'0'
            }
            coleccion.add(campos_documento)
            coleccion.add(settings)

    def visualizar_agendas_disponibles():
        colecciones = [coleccion.id for coleccion in db.collections()]
        print('Colecciones en la base de datos:')
        for nombre_coleccion in colecciones:
            print(nombre_coleccion)

def register_user(email, password):
    user = auth.create_user(
        email=email,
        password=password
    )
    return user.uid  

def verify_user(token):
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token.get('uid')
    return uid  

def enviar_invitacion(agenda_id, emisor_user_id, receptor_email, nivel_de_acceso):
    receptor_user_id = buscar_usuario_por_email(receptor_email)
    if receptor_user_id:
        db.collection('invitaciones').add({
            'agenda_id': agenda_id,
            'emisor_user_id': emisor_user_id,
            'receptor_user_id': receptor_user_id,
            'nivel_de_acceso': nivel_de_acceso,
            'estado': 'pendiente'
        })
        print(f"Invitación enviada a {receptor_email}")
    else:
        print("Usuario no encontrado.")

def buscar_usuario_por_email(email):
    usuarios_ref = db.collection('usuarios')
    query = usuarios_ref.where('email', '==', email).limit(1)
    results = query.stream()
    for result in results:
        return result.id 
    return None  

def aceptar_invitacion(usuario, invitacion_id):
    invitacion_ref = db.collection('invitaciones').document(invitacion_id)
    invitacion = invitacion_ref.get()
    if invitacion.exists:
        invitacion_data = invitacion.to_dict()
        usuario.agendas_compartidas.append(invitacion_data['agenda_id'])
        invitacion_ref.update({'estado': 'aceptada'})
        agenda_ref = db.collection('agendas').document(invitacion_data['agenda_id'])
        agenda_ref.update({
            'usuarios_compartidos': firestore.ArrayUnion([usuario.user_id])
        })
        print("Invitación aceptada.")
    else:
        print("La invitación no existe o ya fue procesada.")
        
# def login_user(email, password):
#     try:
#         user = auth.get_user_by_email(email)
#         return user.uid, user.email
#     except exceptions.FirebaseError as e:
#         print(f"Error de Firebase: {e}")
#         return None, None
#     except ValueError as e:
#         print(f"Error de valor: {e}")
#         return None, None

def login_user(email, password):
    api_key = 'AIzaSyAfbXWM4PF78u7JkdfXpoBSjy3jKbXEErc'
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        user_data = response.json()
        return user_data['localId'], user_data['email']
    else:
        print(f"Error de autenticación: {response.json()['error']['message']}")
        return None, None