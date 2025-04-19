"""Implementar un sistema que gestione la reserva de turnos médicos para los profesionales 
de las distintas especialidades que atiende un centro de salud, utilizando matrices, listas
y diccionarios para mantener la información, almacenándola en archivos para permitir su posterior
recuperación. Aplicar recursividad para realizar las busquedas de una manera ágil y flexible."""

# Lista de especialidades médicas
especialidades = ["Clínica", "Pediatría", "Cardiología", "Dermatología", "Ginecología"]

# Lista de médicos: cada uno tiene un ID, un nombre y una especialidad
medicos = [
    [1, "Dr. Martínez", "Clínica"],
    [2, "Dr. López", "Pediatría"],
    [3, "Dr. Sánchez", "Cardiología"],
    [4, "Dr. García", "Dermatología"],
    [5, "Dr. Fernández", "Ginecología"]
]

# Lista de turnos: una matriz 5x5 para cada médico, indicando disponibilidad (5 días x 5 horarios)
turnos = [
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)]
]

# Lista de reservas realizadas: cada una es [dni, nombre paciente, id_medico, día, hora]
reservas = []

# Muestra por pantalla todos los médicos con su ID y especialidad
def mostrar_medicos():
    for m in medicos:
        print("ID:", m[0], "| Nombre:", m[1], "| Especialidad:", m[2])

# Muestra los turnos disponibles para un médico elegido por el usuario
def mostrar_turnos():
    mostrar_medicos()
    id_medico = input("Ingrese ID del médico: ")
    if id_medico.isdigit():  # Verifica que sea un número
        id_int = int(id_medico)
        if 1 <= id_int <= 5:  # Verifica que el ID esté en el rango válido
            matriz = turnos[id_int - 1]
            for i in range(5):  # Días (filas)
                fila = ""
                for j in range(5):  # Horarios (columnas)
                    fila += "[" + matriz[i][j] + "] "
                print("Día", i + 1, ":", fila)
        else:
            print("ID no válido.")
    else:
        print("Entrada inválida.")

# Pide y valida el día (como texto) que ingresa el usuario
def validar_dia():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    dia_texto = input("Día (Lunes a Viernes): ")
    if dia_texto in dias:
        return dias.index(dia_texto)  # Devuelve el índice (0 a 4)
    else:
        print("Día inválido.")
        return validar_dia()  # Vuelve a pedir si está mal

# Pide y valida la hora (1 a 5), devolviendo índice (0 a 4)
def validar_hora():
    hora_texto = input("Hora (1-5): ")
    if hora_texto.isdigit():
        hora = int(hora_texto)
        if 1 <= hora <= 5:
            return hora - 1
    print("Hora inválida.")
    return validar_hora()  # Repite si está mal

# Reserva un turno con validaciones
def reservar_turno():
    mostrar_medicos()
    id_medico = input("ID del médico: ")
    if id_medico.isdigit():
        id_int = int(id_medico)
        if 1 <= id_int <= 5:
            dia = validar_dia()
            hora = validar_hora()
            matriz = turnos[id_int - 1]
            if matriz[dia][hora] == "Reservado":
                print("Turno ya reservado. Elija otro.")
                reservar_turno()  # Vuelve a empezar si el turno ya está ocupado
            else:
                dni = input("DNI del paciente: ")
                if not dni.isdigit() or len(dni) > 8:
                    print("DNI inválido. Debe contener hasta 8 dígitos.")
                    return reservar_turno()
                nombre = input("Nombre del paciente: ")
                matriz[dia][hora] = "Reservado"  # Marca turno como reservado
                reservas.append([dni, nombre, id_int, dia + 1, hora + 1])  # Guarda la reserva
                print("Turno reservado con éxito.")
        else:
            print("ID de médico inválido.")
    else:
        print("Entrada inválida.")

# Cancela los turnos asociados a un DNI
def cancelar_turno():
    dni = input("Ingrese DNI del paciente para cancelar turno: ")
    encontrados = [r for r in reservas if r[0] == dni]
    if len(encontrados) > 0:
        for turno in encontrados:
            print(f"Turno de {turno[1]} con el Dr. {turno[2]} | Día: {turno[3]} | Hora: {turno[4]}")
            confirmacion = input("¿Desea cancelar este turno? (si/no): ")
            if confirmacion.lower() == "si":
                turnos[turno[2] - 1][turno[3] - 1][turno[4] - 1] = "Disponible"  # Libera turno
                reservas.remove(turno)  # Quita la reserva
                print("Turno cancelado.")
    else:
        print("No se encontraron turnos con ese DNI.")

# Función recursiva para buscar reservas por DNI
def buscar_reservas_por_dni(dni, lista, i=0):
    if i < len(lista):
        actual = lista[i]
        resto = buscar_reservas_por_dni(dni, lista, i + 1)
        if actual[0] == dni:
            return [actual] + resto
        return resto
    return []

# Imprime las reservas encontradas para un DNI
def buscar_turnos_por_dni():
    dni = input("Ingrese DNI: ")
    resultados = buscar_reservas_por_dni(dni, reservas)
    total = 0
    for r in resultados:
        for m in medicos:
            if m[0] == r[2]:  # Busca el médico correspondiente
                print("Paciente:", r[1], "| Médico:", m[1], "| Especialidad:", m[2], "| Día:", r[3], "| Hora:", r[4])
                total += 1
    if total == 0:
        print("No se encontraron turnos.")

# Menú principal del sistema
def menu():
    print("\nSISTEMA DE TURNOS MÉDICOS")
    print("1. Mostrar médicos")
    print("2. Mostrar turnos")
    print("3. Reservar turno")
    print("4. Cancelar turno")
    print("5. Buscar turnos por DNI")
    print("6. Salir")
    opcion = input("Seleccione opción: ")

    if opcion == "1":
        mostrar_medicos()
        menu()
    elif opcion == "2":
        mostrar_turnos()
        menu()
    elif opcion == "3":
        reservar_turno()
        menu()
    elif opcion == "4":
        cancelar_turno()
        menu()
    elif opcion == "5":
        buscar_turnos_por_dni()
        menu()
    elif opcion == "6":
        print("Fin del programa.")
    else:
        print("Opción inválida.")
        menu()

# Llama al menú para iniciar el programa
menu()
