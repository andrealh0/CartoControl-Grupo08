import datos_cartocontrol as datos


def pedir_codigo_orden():
    cod = datos.pedir_texto("Ingrese el codigo de la orden: ").upper()
    orden = datos.buscar_orden(cod)
    while orden is None:
        print("Orden inexistente. Intente nuevamente.")
        cod = datos.pedir_texto("Ingrese el codigo de la orden: ").upper()
        orden = datos.buscar_orden(cod)
    return cod


def mostrar_orden(cod):
    orden = datos.buscar_orden(cod)
    print("Etapa actual:", orden[6])
    print("Estado actual:", orden[7])


def puede_producir(orden):
    if orden[5] != "si":
        print("No puede producirse una orden cuyo pedido esta pendiente de aprobacion.")
        return False
    reserva = datos.buscar_reserva(orden[0], orden[9])
    if reserva is None or int(reserva[2]) < int(orden[10]):
        print("Falta reservar todo el material necesario para esta orden.")
        return False
    if orden[13] != "si":
        print("El arte aun no esta aprobado.")
        decision = datos.pedir_si_no("¿Se autorizo continuar? (si/no): ")
        if decision == "no":
            return False
        autoriza = datos.pedir_texto("Nombre de quien autorizo la excepcion: ")
        datos.registrar_historial(orden[0], "Arte pendiente: autorizo continuar " + autoriza)
        datos.agregar_registro_extra("EXCEPCION_ARTE", orden[0], [autoriza])
    return True


def excepcion_arte_vigente(codigo):
    for registro in datos.registros_extra:
        if registro[0] == "EXCEPCION_ARTE" and registro[1] == codigo:
            return True
    return False


def actualizar_etapa_estado():
    print("\n--- ACTUALIZAR ETAPA Y ESTADO ---")
    if len(datos.ordenes) == 0:
        print("No hay ordenes registradas. Cree una en Gestion de ordenes.")
        return
    cod = pedir_codigo_orden()
    orden = datos.buscar_orden(cod)
    mostrar_orden(cod)
    netapa = datos.pedir_texto("Ingrese la nueva etapa: ").title()
    nest = datos.pedir_texto("Ingrese el nuevo estado: ").title()

    etapas = ["Planificacion", "Produccion", "Empaque", "Despacho"]
    estados = ["Pendiente", "En Proceso", "Detenida", "Terminada"]
    if netapa not in etapas or nest not in estados:
        print("Etapa valida: Planificacion, Produccion, Empaque o Despacho.")
        print("Estado valido: Pendiente, En Proceso, Detenida o Terminada.")
        return
    etapa = orden[6]
    est = orden[7]
    if netapa == etapa and nest == est:
        print("No se realizaron cambios.")
        return
    if netapa == "Produccion" and etapa != "Produccion":
        if not puede_producir(orden):
            return
    resp = datos.pedir_texto("Ingrese el nombre del responsable: ").title()
    fecha = datos.fecha_hora_actual()
    orden[6] = netapa
    orden[7] = nest
    cambio = "Cambio de " + etapa + " - " + est
    cambio = cambio + " a " + netapa + " - " + nest
    cambio = cambio + ". Responsable: " + resp
    datos.registrar_historial(cod, cambio)
    print("Etapa y estado actualizados correctamente.")
    print("Nueva etapa:", netapa)
    print("Nuevo estado:", nest)
    print("Fecha y hora:", fecha)


def registrar_produccion_rechazos_paros():
    print("\n--- REGISTRAR PRODUCCION, RECHAZOS Y PAROS ---")
    if len(datos.ordenes) == 0:
        print("No hay ordenes registradas. Cree una en Gestion de ordenes.")
        return
    cod = pedir_codigo_orden()
    orden = datos.buscar_orden(cod)
    mostrar_orden(cod)
    if orden[6] != "Produccion":
        print("Primero actualice la etapa de la orden a Produccion.")
        return
    if orden[13] != "si" and not excepcion_arte_vigente(cod):
        print("Primero se debe aprobar el arte o registrar la autorizacion para continuar.")
        return
    hIni = datos.pedir_hora("Ingrese la hora de inicio (HH:MM): ")
    hFin = datos.pedir_hora("Ingrese la hora de finalizacion (HH:MM): ")
    while hFin <= hIni:
        print("La hora de finalizacion debe ser posterior a la hora de inicio.")
        hFin = datos.pedir_hora("Ingrese la hora de finalizacion (HH:MM): ")
    cantB = datos.pedir_cantidad("Ingrese la cantidad buena: ")
    cantR = datos.pedir_cantidad("Ingrese la cantidad rechazada: ")
    cantP = datos.pedir_cantidad("Ingrese la cantidad de prueba: ")
    paro = datos.pedir_si_no("¿Hubo algun paro? (si/no): ")
    mot = "No hubo paro"
    if paro == "si":
        mot = datos.pedir_texto("Ingrese el motivo del paro: ")
    if cantB + cantR + cantP == 0 and paro == "no":
        print("No hay cantidades ni paro para registrar.")
        return
    resp = datos.pedir_texto("Ingrese el nombre del responsable: ").title()
    fecha = datos.fecha_hora_actual()
    datos.producciones.append([cod, hIni, hFin, str(cantB), str(cantR),
                               str(cantP), mot, resp, fecha])
    datos.registrar_historial(cod, "Produccion: buena " + str(cantB)
                             + ", rechazada " + str(cantR) + ", prueba "
                             + str(cantP) + ". Paro: " + mot + ". Responsable: " + resp)
    print("Registro de produccion guardado correctamente.")
    print("Cantidad buena:", cantB)
    print("Cantidad rechazada:", cantR)
    print("Cantidad de prueba:", cantP)
    print("Paro:", mot)
    print("Fecha y hora del registro:", fecha)


def menu_seguimiento():
    opcion = ""
    while opcion != "3":
        print("\n========================================")
        print("MODULO DE SEGUIMIENTO DE PRODUCCION")
        print("========================================")
        print("1. Actualizar etapa y estado")
        print("2. Registrar produccion, rechazos y paros")
        print("3. Regresar al menu principal")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            actualizar_etapa_estado()
        elif opcion == "2":
            registrar_produccion_rechazos_paros()
        elif opcion == "3":
            print("Regresando al menu principal...")
        else:
            print("Opcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    menu_seguimiento()