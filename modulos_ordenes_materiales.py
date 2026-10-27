import time
import datos_cartocontrol as datos


def clave_fecha(fecha):
    return fecha[6:10] + fecha[3:5] + fecha[0:2]


def registrar_actualizar_orden():
    print("\n--- REGISTRAR Y ACTUALIZAR UNA ORDEN ---")
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)

    if orden is None:
        cliente = datos.pedir_texto("Cliente: ")
        producto = datos.pedir_texto("Producto: ")
        cantidad = datos.pedir_positivo("Cantidad solicitada: ")
        entrega = datos.pedir_fecha("Fecha de entrega (DD/MM/AAAA): ")
        aprobado = datos.pedir_si_no("¿El pedido ya fue aprobado? (si/no): ")
        material = datos.pedir_texto("Codigo del material necesario: ").upper()
        cant_material = datos.pedir_positivo("Cantidad de material necesaria: ")
        orden = [codigo, cliente, producto, str(cantidad), entrega, aprobado,
                 "Planificacion", "Pendiente", "Media", material,
                 str(cant_material), "", "", "no", "Pendiente", "", ""]
        datos.ordenes.append(orden)
        datos.registrar_historial(codigo, "Orden registrada. Pedido aprobado: " + aprobado)
        print("Orden", codigo, "registrada correctamente.")
        return

    print("La orden ya existe. Cliente:", orden[1], "Producto:", orden[2])
    opcion = ""
    while opcion != "7":
        print("1. Cambiar cliente")
        print("2. Cambiar producto")
        print("3. Cambiar cantidad solicitada")
        print("4. Cambiar fecha de entrega")
        print("5. Cambiar aprobacion del pedido")
        print("6. Cambiar material y cantidad necesaria")
        print("7. Terminar actualizacion")
        opcion = input("Opcion: ").strip()
        cambio = ""
        if opcion == "1":
            orden[1] = datos.pedir_texto("Cliente nuevo: ")
            cambio = "Cliente actualizado"
        elif opcion == "2":
            orden[2] = datos.pedir_texto("Producto nuevo: ")
            cambio = "Producto actualizado"
        elif opcion == "3":
            orden[3] = str(datos.pedir_positivo("Cantidad nueva: "))
            cambio = "Cantidad solicitada actualizada"
        elif opcion == "4":
            orden[4] = datos.pedir_fecha("Fecha nueva (DD/MM/AAAA): ")
            cambio = "Fecha de entrega actualizada"
        elif opcion == "5":
            aprobado = datos.pedir_si_no("¿Pedido aprobado? (si/no): ")
            reserva = datos.buscar_reserva(codigo, orden[9])
            if aprobado == "no" and reserva is not None and int(reserva[2]) > 0:
                print("No puede quitar la aprobacion si hay material reservado.")
            else:
                orden[5] = aprobado
                cambio = "Aprobacion del pedido: " + aprobado
        elif opcion == "6":
            reserva = datos.buscar_reserva(codigo, orden[9])
            if reserva is not None and int(reserva[2]) > 0:
                print("Esta orden ya tiene material reservado; primero debe resolverse la reserva.")
            else:
                orden[9] = datos.pedir_texto("Nuevo codigo de material: ").upper()
                orden[10] = str(datos.pedir_positivo("Nueva cantidad necesaria: "))
                cambio = "Material requerido actualizado"
        elif opcion != "7":
            print("Opcion invalida.")
        if cambio != "":
            responsable = datos.pedir_texto("Responsable del cambio: ")
            datos.registrar_historial(codigo, cambio + ". Responsable: " + responsable)
            print("Cambio guardado.")


def organizar_secuencia_diaria():
    print("\n--- ORGANIZAR LA SECUENCIA DEL DIA SIGUIENTE ---")
    ahora = time.localtime()
    if ahora.tm_hour >= 17:
        print("La secuencia del dia siguiente debe liberarse antes de las 5:00 p. m.")
        return
    manana = time.localtime(time.time() + 86400)
    fecha = time.strftime("%d/%m/%Y", manana)
    opciones = []
    for orden in datos.ordenes:
        if orden[5] == "si" and orden[7].lower() != "terminada":
            if orden[6].lower() != "despacho":
                reserva = datos.buscar_reserva(orden[0], orden[9])
                if reserva is not None and int(reserva[2]) >= int(orden[10]):
                    valor = 2
                    if orden[8] == "Alta":
                        valor = 1
                    elif orden[8] == "Baja":
                        valor = 3
                    opciones.append([valor, clave_fecha(orden[4]), orden[0]])
    if len(opciones) == 0:
        print("No hay ordenes aprobadas con el material necesario reservado.")
        return
    opciones.sort()
    print("Ordenes por prioridad y fecha de entrega para", fecha)
    for i in range(len(opciones)):
        codigo = opciones[i][2]
        orden = datos.buscar_orden(codigo)
        print(i + 1, codigo, "-", orden[8], "- Entrega:", orden[4])
    print("Turno 1: 06:00 a 14:00. Turno 2: 14:00 a 21:00.")
    turnos = []
    for opcion in opciones:
        codigo = opcion[2]
        turno = input("Turno para " + codigo + " (1/2): ").strip()
        while turno != "1" and turno != "2":
            print("Seleccione turno 1 o 2.")
            turno = input("Turno para " + codigo + " (1/2): ").strip()
        turnos.append(turno)
    liberar = datos.pedir_si_no("¿Liberar esta secuencia para manana? (si/no): ")
    if liberar == "no":
        print("La secuencia no se guardo.")
        return
    responsable = datos.pedir_texto("Planificador responsable: ")
    for i in range(len(opciones)):
        orden = datos.buscar_orden(opciones[i][2])
        orden[11] = fecha
        orden[12] = turnos[i]
        texto = "Secuencia para " + fecha + ", puesto " + str(i + 1)
        texto = texto + ", turno " + turnos[i] + ". Planificador: " + responsable
        datos.registrar_historial(orden[0], texto)
    print("Secuencia del", fecha, "liberada. Hora:", datos.fecha_hora_actual())


def registrar_cambio_prioridad():
    print("\n--- REGISTRAR CAMBIO DE PRIORIDAD ---")
    codigo = datos.pedir_texto("Codigo de orden: ").upper()
    orden = datos.buscar_orden(codigo)
    if orden is None:
        print("La orden no existe.")
        return
    anterior = orden[8]
    print("Prioridad actual:", anterior)
    nueva = input("Nueva prioridad (1 Alta, 2 Media, 3 Baja): ").strip()
    while nueva != "1" and nueva != "2" and nueva != "3":
        print("Elija 1, 2 o 3.")
        nueva = input("Nueva prioridad (1 Alta, 2 Media, 3 Baja): ").strip()
    prioridades = ["Alta", "Media", "Baja"]
    prioridad = prioridades[int(nueva) - 1]
    if prioridad == anterior:
        print("La prioridad sigue igual.")
        return
    motivo = datos.pedir_texto("Motivo del cambio: ")
    solicitante = datos.pedir_texto("Quien lo solicito: ")
    autorizador = datos.pedir_texto("Quien lo autorizo: ")
    orden[8] = prioridad
    texto = "Prioridad: " + anterior + " a " + prioridad
    texto = texto + ". Motivo: " + motivo
    texto = texto + ". Solicito: " + solicitante + ". Autorizo: " + autorizador
    datos.registrar_historial(codigo, texto)
    print("Prioridad actualizada. Fecha y hora:", datos.fecha_hora_actual())


def consultar_reservar_materia_prima():
    print("\n--- CONSULTAR Y RESERVAR MATERIA PRIMA ---")
    print("1. Consultar o registrar existencias reales")
    print("2. Reservar material para una orden")
    opcion = input("Seleccione una opcion: ").strip()
    if opcion == "1":
        codigo = datos.pedir_texto("Codigo del material: ").upper()
        material = datos.buscar_material(codigo)
        if material is None:
            descripcion = datos.pedir_texto("Descripcion del material: ")
            existencia = datos.pedir_cantidad("Existencia fisica real: ")
            datos.materiales.append([codigo, descripcion, str(existencia)])
            datos.guardar_datos()
            print("Material registrado:", codigo, "Existencia:", existencia)
        else:
            reservado = datos.total_reservado(codigo)
            print("Material:", material[1], "Fisico:", material[2])
            print("Reservado:", reservado, "Disponible:", int(material[2]) - reservado)
            corregir = datos.pedir_si_no("¿Actualizar existencia fisica? (si/no): ")
            if corregir == "si":
                nueva = datos.pedir_cantidad("Nueva existencia fisica: ")
                if nueva < reservado:
                    print("No se puede bajar de la cantidad ya reservada:", reservado)
                    return
                responsable = datos.pedir_texto("Responsable del ajuste: ")
                anterior = material[2]
                material[2] = str(nueva)
                datos.agregar_registro_extra("EXISTENCIA", "", [codigo, anterior,
                                           str(nueva), responsable, datos.fecha_hora_actual()])
                print("Existencia actualizada.")
    elif opcion == "2":
        codigo = datos.pedir_texto("Codigo de la orden: ").upper()
        orden = datos.buscar_orden(codigo)
        if orden is None:
            print("La orden no existe.")
            return
        if orden[5] != "si":
            print("Primero se debe aprobar el pedido.")
            return
        material = datos.buscar_material(orden[9])
        if material is None:
            print("El material", orden[9], "no tiene existencia registrada.")
            return
        reserva = datos.buscar_reserva(codigo, material[0])
        ya_reservado = 0
        if reserva is not None:
            ya_reservado = int(reserva[2])
        falta = int(orden[10]) - ya_reservado
        disponible = int(material[2]) - datos.total_reservado(material[0])
        print("Material:", material[0], "Requerido:", orden[10])
        print("Ya reservado:", ya_reservado, "Falta:", falta,
              "Disponible real:", disponible)
        if falta <= 0:
            print("La orden ya tiene todo el material reservado.")
            return
        cantidad = datos.pedir_positivo("Cantidad a reservar: ")
        if cantidad > falta or cantidad > disponible:
            print("No se puede reservar mas de lo requerido ni de lo disponible.")
            return
        responsable = datos.pedir_texto("Encargado de bodega: ")
        if reserva is None:
            datos.reservas.append([codigo, material[0], str(cantidad)])
        else:
            reserva[2] = str(ya_reservado + cantidad)
        datos.registrar_historial(codigo, "Reserva de " + str(cantidad) + " unidades de "
                                 + material[0] + ". Bodega: " + responsable)
        print("Reserva guardada. Disponible ahora:", disponible - cantidad)
    else:
        print("Opcion invalida.")


def registrar_movimiento_material():
    print("\n--- MOVIMIENTO DE MATERIAL ENTRE ORDENES ---")
    origen = datos.pedir_texto("Orden de origen: ").upper()
    destino = datos.pedir_texto("Orden de destino: ").upper()
    o1 = datos.buscar_orden(origen)
    o2 = datos.buscar_orden(destino)
    if o1 is None or o2 is None or origen == destino:
        print("Revise que existan dos ordenes distintas.")
        return
    if o2[5] != "si":
        print("El pedido de destino debe estar aprobado.")
        return
    if o1[9] != o2[9]:
        print("Las dos ordenes deben requerir el mismo material.")
        return
    reserva_origen = datos.buscar_reserva(origen, o1[9])
    if reserva_origen is None or int(reserva_origen[2]) == 0:
        print("La orden de origen no tiene material reservado.")
        return
    reserva_destino = datos.buscar_reserva(destino, o2[9])
    ya_reservado = 0
    if reserva_destino is not None:
        ya_reservado = int(reserva_destino[2])
    pendiente_destino = int(o2[10]) - ya_reservado
    print("Material:", o1[9], "Reservado en origen:", reserva_origen[2])
    print("Pendiente de reservar en destino:", pendiente_destino)
    if pendiente_destino <= 0:
        print("La orden de destino ya tiene todo el material.")
        return
    cantidad = datos.pedir_positivo("Cantidad a trasladar: ")
    if cantidad > int(reserva_origen[2]) or cantidad > pendiente_destino:
        print("La cantidad excede la reserva de origen o lo necesario en destino.")
        return
    planificador = datos.pedir_texto("Quien autoriza en planificacion: ")
    bodega = datos.pedir_texto("Quien autoriza en bodega: ")
    reserva_origen[2] = str(int(reserva_origen[2]) - cantidad)
    if reserva_destino is None:
        datos.reservas.append([destino, o2[9], str(cantidad)])
    else:
        reserva_destino[2] = str(ya_reservado + cantidad)
    momento = datos.fecha_hora_actual()
    datos.movimientos.append([o1[9], str(cantidad), origen, destino,
                              planificador, bodega, momento])
    texto = "Material " + o1[9] + ": " + str(cantidad) + " unidades de "
    texto = texto + origen + " a " + destino + ". Reponer a " + origen
    texto = texto + ". Autorizaron: " + planificador + " y " + bodega
    datos.registrar_historial(origen, texto)
    datos.registrar_historial(destino, texto)
    print("Movimiento registrado. Debe reponerse material a", origen)


def menu_gestion_planificacion():
    opcion = ""
    while opcion != "4":
        print("\nGESTION Y PLANIFICACION DE ORDENES")
        print("1. Registrar y actualizar una orden")
        print("2. Organizar la secuencia diaria")
        print("3. Registrar cambios de prioridad")
        print("4. Volver")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            registrar_actualizar_orden()
        elif opcion == "2":
            organizar_secuencia_diaria()
        elif opcion == "3":
            registrar_cambio_prioridad()
        elif opcion != "4":
            print("Opcion invalida.")


def menu_materia_prima():
    opcion = ""
    while opcion != "3":
        print("\nCONTROL DE MATERIA PRIMA")
        print("1. Consultar y reservar materia prima")
        print("2. Registrar movimientos de material")
        print("3. Volver")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            consultar_reservar_materia_prima()
        elif opcion == "2":
            registrar_movimiento_material()
        elif opcion != "3":
            print("Opcion invalida.")


if __name__ == "__main__":
    opcion = ""
    while opcion != "3":
        print("\nCARTOCONTROL - MODULOS 1 Y 2")
        print("1. Gestion y planificacion de ordenes")
        print("2. Control de materia prima")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "1":
            menu_gestion_planificacion()
        elif opcion == "2":
            menu_materia_prima()
        elif opcion != "3":
            print("Opcion invalida.")