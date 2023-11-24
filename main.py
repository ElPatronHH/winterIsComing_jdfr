#main.py jdfr
from firestore_db import Agenda, Contacto
from users import enviar_invitacion, aceptar_invitacion, Usuario, login_user

current_user = Usuario(user_id='id_del_usuario_actual', email='email_del_usuario_actual')

def guardar_contacto(agenda, contacto):
    try:
        agenda.agregar_contacto(contacto)
        print(f"Contacto '{contacto.nombre}' guardado exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error al guardar el contacto: {e}")

def mostrar_agenda(agenda):
    print("Contactos en la agenda:")
    for contacto in agenda.obtener_contactos():
        print(f"Nombre: {contacto.nombre}")
        print(f"Edad: {contacto.edad}")
        print(f"Calle: {contacto.calle}")
        print(f"Ciudad: {contacto.ciudad}")
        print(f"Código Postal: {contacto.codigo_postal}")
        print(f"Número Exterior: {contacto.numero_exterior}")
        print(f"Número Interior: {contacto.numero_interior}")
        print(f"Colonia: {contacto.colonia}")
        print(f"Número de Teléfono: {contacto.numero}")
        print(f"Correo Electrónico: {contacto.email}")
        print(f"Página Web: {contacto.pagina_web}")
        print("") 

def mostrar_informacion_contacto(contacto):
    print(f"Nombre: {contacto.nombre}")
    print(f"Edad: {contacto.edad}")
    print(f"Calle: {contacto.calle}")
    print(f"Ciudad: {contacto.ciudad}")
    print(f"Código Postal: {contacto.codigo_postal}")
    print(f"Número Exterior: {contacto.numero_exterior}")
    print(f"Número Interior: {contacto.numero_interior}")
    print(f"Colonia: {contacto.colonia}")
    print(f"Número de Teléfono: {contacto.numero}")
    print(f"Correo Electrónico: {contacto.email}")
    print(f"Página Web: {contacto.pagina_web}")
    print("")


# def buscar_contacto_por_nombre(agenda, nombre):
#     for contacto in agenda.obtener_contactos():
#         if contacto.nombre.lower() == nombre.lower():
#             return contacto
#     return None

def borrar_contacto(agenda, contacto):
    agenda.eliminar_contacto(contacto)
    print(f"Contacto '{contacto.nombre}' ha sido borrado.")

def main():
    current_user_id, current_user_email = None, None
    mi_agenda = Agenda(owner_id=current_user_id)
    mi_agenda.cargar_contactos()
    current_user_id, current_user_email = None, None

    
    while True:
        if not current_user_id:
            email = input("Por favor ingrese su email: ")
            password = input("Por favor ingrese su contraseña: ")
            current_user_id, current_user_email = login_user(email, password)
            if current_user_id:
                print(f"Bienvenido {current_user_email}")
            else:
                print("Inicio de sesión fallido, intente de nuevo.")
                continue
        print("")
        print("1. Crear nuevo contacto")
        print("2. Mostrar Agenda")
        print("3. Buscar contacto por nombre")
        print("4. Buscar contacto por teléfono")
        print("5. Borrar contacto")
        print("6. Compartir mi agenda")
        print("7. Responder a una invitación")
        print("8. Salir")
        print("")

        opcion = input("Seleccione una opción: ")
        print("")

        if opcion == "1":
            print("Ingrese los datos del nuevo contacto:")
            nombre = input("Nombre: ")
            edad = int(input("Edad: ")) 
            calle = input("Calle: ")
            ciudad = input("Ciudad: ")
            codigo_postal = input("Código Postal: ")
            numero_exterior = input("Número Exterior: ")
            numero_interior = input("Número Interior: ")
            colonia = input("Colonia: ")
            numero = input("Número de Teléfono: ")
            email = input("Correo Electrónico: ")
            pagina_web = input("Página Web: ")

            nuevo_contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web)
            guardar_contacto(mi_agenda, nuevo_contacto)

        elif opcion == "2":
            mostrar_agenda(mi_agenda)

        elif opcion == "3":
            nombre = input("Ingrese el nombre a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_nombre(nombre)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")

        elif opcion == "4":
            numero = input("Ingrese el número de teléfono a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_telefono(numero)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")                
        elif opcion == "5":
            nombre = input("Ingrese el nombre del contacto a borrar: ")
            contacto_a_borrar = mi_agenda.buscar_contacto_por_nombre(nombre)
            if contacto_a_borrar:
                borrar_contacto(mi_agenda, contacto_a_borrar)
            else:
                print("Contacto no encontrado.")

        elif opcion == "6":
            print("Enviar una invitación para compartir tu agenda.")
            agenda_id = input("ID de la agenda a compartir: ")
            receptor_email = input("Email del usuario con quien compartir: ")
            nivel_de_acceso = input("Nivel de acceso (lectura/escritura): ")
            enviar_invitacion(agenda_id, current_user.user_id, receptor_email, nivel_de_acceso)

        elif opcion == "7":
            print("Responder a invitaciones pendientes.")
            invitacion_id = input("ID de la invitación a responder: ")
            respuesta = input("Aceptas la invitación? (s/n): ")
            if respuesta.lower() == 's':
                aceptar_invitacion(current_user, invitacion_id)
            else:
                print("Invitación declinada o ignorada.")

        elif opcion == "8":
            print("Saliendo...")
            break
        
        elif opcion == "9":
            current_user_id, current_user_email = None, None
            print("Se ha cerrado la sesión.")
    

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()