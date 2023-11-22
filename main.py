from agenda import Agenda, Contacto

def cargar_contactos(agenda):
    try:
        with open("contactos.txt", "r") as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                datos = linea.strip().split(',')
                nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web = datos
                contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior,
                                    colonia, numero, email, pagina_web)
                agenda.agregar_contacto(contacto)
        print("Contactos cargados exitosamente.")
    except FileNotFoundError:
        print("El archivo de contactos no existe. No se pudo cargar ningún contacto.")


def guardar_contacto(agenda, contacto):
    agenda.agregar_contacto(contacto)
    with open("contactos.txt", "a") as archivo:
        linea = f"{contacto.get_nombre()},{contacto.get_edad()},{contacto.get_calle()},{contacto.get_ciudad()},{contacto.get_codigo_postal()},{contacto.get_numero_exterior()},{contacto.get_numero_interior()},{contacto.get_colonia()},{contacto.get_numero()},{contacto.get_email()},{contacto.get_pagina_web()}\n"
        archivo.write(linea)
        print(f"Contacto '{contacto.get_nombre()}' guardado exitosamente.")


def mostrar_agenda(agenda):
    print("Contactos en la agenda:")
    for contacto in agenda.obtener_contactos():
        print(f"Nombre: {contacto.get_nombre()}")
        print(f"Calle: {contacto.get_calle()}")
        print(f"Ciudad: {contacto.get_ciudad()}")
        print(f"Código Postal: {contacto.get_codigo_postal()}")
        print(f"Número Exterior: {contacto.get_numero_exterior()}")
        print(f"Número Interior: {contacto.get_numero_interior()}")
        print(f"Colonia: {contacto.get_colonia()}")
        print(f"Número de Teléfono: {contacto.get_numero()}")
        print(f"Correo Electrónico: {contacto.get_email()}")
        print(f"Página Web: {contacto.get_pagina_web()}")
        print("")

def buscar_contacto_por_nombre(agenda, nombre):
    for contacto in agenda.obtener_contactos():
        if contacto.get_nombre().lower() == nombre.lower():
            return contacto
    return None

def buscar_contacto_por_telefono(agenda, numero):
    for contacto in agenda.obtener_contactos():
        if contacto.get_numero() == numero:
            return contacto
    return None

def borrar_contacto(agenda, contacto):
    if contacto in agenda.obtener_contactos():
        agenda.obtener_contactos().remove(contacto)
        with open("contactos.txt", "w") as archivo:
            for c in agenda.obtener_contactos():
                linea = f"{c.get_nombre()},{c.get_edad()},{c.get_calle()},{c.get_ciudad()},{c.get_codigo_postal()},{c.get_numero_exterior()},{c.get_numero_interior()},{c.get_colonia()},{c.get_numero()},{c.get_email()},{c.get_pagina_web()}\n"
                archivo.write(linea)
        print(f"Contacto '{contacto.get_nombre()}' ha sido borrado.")

def verificar_archivo_contactos():
    try:
        with open("contactos.txt", "r"):
            pass
    except FileNotFoundError:
        with open("contactos.txt", "w"):
            pass

if __name__ == "__main__":
    verificar_archivo_contactos()
    mi_agenda = Agenda()
    cargar_contactos(mi_agenda)

    while True:
        print("1. Crear nuevo contacto")
        print("2. Mostrar Agenda")
        print("3. Buscar contacto por nombre")
        print("4. Buscar contacto por teléfono")
        print("5. Borrar contacto")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Ingrese los datos del nuevo contacto:")
            nombre = input("Nombre: ")
            edad = input("Edad: ")
            calle = input("Calle: ")
            ciudad = input("Ciudad: ")
            codigo_postal = input("Código Postal: ")
            numero_exterior = input("Número Exterior: ")
            numero_interior = input("Número Interior: ")
            colonia = input("Colonia: ")
            numero = input("Número de Teléfono: ")
            email = input("Correo Electrónico: ")
            pagina_web = input("Página Web: ")

            contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia,
                                numero, email, pagina_web)
            guardar_contacto(mi_agenda, contacto)
        elif opcion == "2":
            mostrar_agenda(mi_agenda)
        elif opcion == "3":
            nombre = input("Ingrese el nombre a buscar: ")
            contacto_encontrado = buscar_contacto_por_nombre(mi_agenda, nombre)
            if contacto_encontrado:
                print("Contacto encontrado:")
                print(f"Nombre: {contacto_encontrado.get_nombre()}")
                print(f"Calle: {contacto_encontrado.get_calle()}")
            else:
                print("Contacto no encontrado.")
        elif opcion == "4":
            numero = input("Ingrese el número de teléfono a buscar: ")
            contacto_encontrado = buscar_contacto_por_telefono(mi_agenda, numero)
            if contacto_encontrado:
                print("Contacto encontrado:")
                print(f"Nombre: {contacto_encontrado.get_nombre()}")
                print(f"Número de Teléfono: {contacto_encontrado.get_numero()}")
            else:
                print("Contacto no encontrado.")
        elif opcion == "5":
            nombre = input("Ingrese el nombre del contacto a borrar: ")
            contacto_a_borrar = buscar_contacto_por_nombre(mi_agenda, nombre)
            if contacto_a_borrar:
                borrar_contacto(mi_agenda, contacto_a_borrar)
            else:
                print("Contacto no encontrado.")
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")