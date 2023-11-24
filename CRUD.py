import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la aplicación de Firebase con las credenciales
cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)

# Ahora que la app está inicializada, obtenemos el cliente de Firestore
db = firestore.client()
# Crear un nuevo documento en la colección 'contacts'
new_contact_ref = db.collection('contacts').document()
new_contact_ref.set({
    'name': 'John Doe',
    'phone': '123456789',
    'email': 'johndoe@example.com',
})

# Leer un documento por su ID
contact_ref = db.collection('contacts').document('contact_id')
contact = contact_ref.get()
if contact.exists:
    print(contact.to_dict())

# Actualizar un documento
contact_ref.update({
    'phone': '987654321'
})

# Eliminar un documento
contact_ref.delete()
