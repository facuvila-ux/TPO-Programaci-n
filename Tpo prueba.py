"""Implementar un sistema que gestione la reserva de turnos médicos para los profesionales 
de las distintas especialidades que atiende un centro de salud, utilizando matrices, listas
y diccionarios para mantener la información, almacenándola en archivos para permitir su posterior
recuperación. Aplicar recursividad para realizar las busquedas de una manera ágil y flexible."""


# Especialidades y médicos
especialidades = ["Clínica", "Pediatría", "Cardiología", "Dermatología", "Ginecología"]
medicos = [
    [1, "Dr. Martínez", "Clínica"],
    [2, "Dr. López", "Pediatría"],
    [3, "Dr. Sánchez", "Cardiología"],
    [4, "Dr. García", "Dermatología"],
    [5, "Dr. Fernández", "Ginecología"]
]

# Turnos disponibles por cada médico (matrices 5x5)
turnos = [
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)],
    [["Disponible" for _ in range(5)] for _ in range(5)]
]

# Reservas: cada reserva es una lista [dni, nombre, id_medico, dia, hora]
reservas = []

def validar_dni():
    dni = input("DNI del paciente (hasta 8 dígitos): ")
    if dni.isdigit() and len(dni) <= 8:
        return dni
    print("DNI inválido. Debe ser numérico y de hasta 8 dígitos.")
    return validar_dni()

def mostrar_medicos():
    for m in medicos:
        print("ID:", m[0], "| Nombre:", m[1], "| Especialidad:", m[2])

def mostrar_turnos():
    mostrar_medicos()
    id_medico = input("Ingrese ID del médico: ")
    if id_medico.isdigit():
        id_int = int(id_medico)
        if 1 <= id_int <= 5:
            matriz = turnos[id_int - 1]
            for i in range(5):
                fila = ""
                for j in range(5):
                    fila += "[" + matriz[i][j] + "] "
                print("Día", i + 1, ":", fila)
        else:
            print("ID no válido.")
    else:
        print("Entrada inválida.")

def validar_dia():
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    dia_texto = input("Día (Lunes a Viernes): ")
    if dia_texto in dias:
        return dias.index(dia_texto)
    else:
        print("Día inválido.")
        return validar_dia()

def validar_hora():
    hora_texto = input("Hora (1-5): ")
    if hora_texto.isdigit():
        hora = int(hora_texto)
        if 1 <= hora <= 5:
            return hora - 1
    print("Hora inválida.")
    return validar_hora()

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
                reservar_turno()
            else:
                dni = validar_dni()
                nombre = input("Nombre del paciente: ")
                matriz[dia][hora] = "Reservado"
                reservas.append([dni, nombre, id_int, dia + 1, hora + 1])
                print("Turno reservado con éxito.")
        else:
            print("ID de médico inválido.")
    else:
        print("Entrada inválida.")

def cancelar_turno():
    dni = validar_dni()
    encontrados = [r for r in reservas if r[0] == dni]
    if len(encontrados) > 0:
        for turno in encontrados:
            print(f"Turno de {turno[1]} con el Dr. {turno[2]} | Día: {turno[3]} | Hora: {turno[4]}")
            confirmacion = input("¿Desea cancelar este turno? (si/no): ")
            if confirmacion.lower() == "si":
                turnos[turno[2] - 1][turno[3] - 1][turno[4] - 1] = "Disponible"
                reservas.remove(turno)
                print("Turno cancelado.")
    else:
        print("No se encontraron turnos con ese DNI.")

def buscar_reservas_por_dni(dni, lista, i=0):
    if i < len(lista):
        actual = lista[i]
        resto = buscar_reservas_por_dni(dni, lista, i + 1)
        if actual[0] == dni:
            return [actual] + resto
        return resto
    return []

def buscar_turnos_por_dni():
    dni = validar_dni()
    resultados = buscar_reservas_por_dni(dni, reservas)
    total = 0
    for r in resultados:
        for m in medicos:
            if m[0] == r[2]:
                print("Paciente:", r[1], "| Médico:", m[1], "| Especialidad:", m[2], "| Día:", r[3], "| Hora:", r[4])
                total += 1
    if total == 0:
        print("No se encontraron turnos.")

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

menu()
